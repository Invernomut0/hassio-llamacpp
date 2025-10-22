#!/usr/bin/env python3
"""
Home Assistant Service Integration per Llama.cpp addon.
Espone servizi HA per dialogare con il chatbot LLM.
"""

import logging
import os
import sys
import time
from typing import Any, Dict

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

# Importa modulo integrazione HA
from ha_integration import HomeAssistantClient, HAContextBuilder

# Configurazione logging - force flush per visibilità immediata
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout,
    force=True
)
logger = logging.getLogger(__name__)

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

logger.info("=" * 80)
logger.info("🚀 HA Service Starting...")
logger.info("=" * 80)

# Flask app per servizi Home Assistant
app = Flask(__name__)
CORS(app)

# URL del server llama.cpp locale
LLAMA_SERVER_URL = "http://localhost:8080"

# Inizializza client Home Assistant
ha_client = HomeAssistantClient()
ha_context = HAContextBuilder(ha_client)

# Sessioni di conversazione (storage in memoria)
conversations: Dict[str, list] = {}


def wait_for_llama_server(max_retries: int = 30, delay: int = 2) -> bool:
    """
    Attende che il server llama.cpp sia pronto.
    
    Args:
        max_retries: Numero massimo di tentativi
        delay: Secondi tra un tentativo e l'altro
    
    Returns:
        True se il server è pronto, False altrimenti
    """
    logger.info("Attesa avvio server llama.cpp...")
    for i in range(max_retries):
        try:
            response = requests.get(f"{LLAMA_SERVER_URL}/health", timeout=5)
            if response.status_code == 200:
                logger.info("Server llama.cpp pronto!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        if i < max_retries - 1:
            time.sleep(delay)
    
    logger.error("Timeout: server llama.cpp non disponibile")
    return False


def call_llama_api(
    messages: list,
    temperature: float = 0.7,
    max_tokens: int = 512,
    stream: bool = False
) -> Dict[str, Any]:
    """
    Chiama l'API OpenAI-compatible di llama-server.
    
    Args:
        messages: Lista di messaggi nel formato OpenAI
        temperature: Creatività delle risposte (0.0-2.0)
        max_tokens: Numero massimo di token nella risposta
        stream: Se True, restituisce streaming response
    
    Returns:
        Risposta dal modello LLM
    """
    url = f"{LLAMA_SERVER_URL}/v1/chat/completions"
    
    # ✅ VALIDAZIONE: Verifica formato messaggi
    if not isinstance(messages, list) or not messages:
        logger.error(f"❌ Messaggi invalidi: deve essere una lista non vuota, ricevuto: {type(messages)}")
        raise ValueError("messages deve essere una lista non vuota")
    
    for idx, msg in enumerate(messages):
        if not isinstance(msg, dict):
            logger.error(f"❌ Messaggio [{idx}] invalido: deve essere un dict, ricevuto: {type(msg)}")
            raise ValueError(f"Messaggio [{idx}] deve essere un dict")
        if 'role' not in msg or 'content' not in msg:
            logger.error(f"❌ Messaggio [{idx}] incompleto: {msg}")
            raise ValueError(f"Messaggio [{idx}] deve avere 'role' e 'content'")
        if msg['role'] not in ['system', 'user', 'assistant']:
            logger.error(f"❌ Messaggio [{idx}] role invalido: {msg['role']}")
            raise ValueError(f"Role deve essere 'system', 'user' o 'assistant', non '{msg['role']}'")
    
    payload = {
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream
    }
    
    # 🔍 DEBUG: Log dettagliato della richiesta
    logger.info("=" * 80)
    logger.info("📤 CHIAMATA LLAMA API")
    logger.info(f"URL: {url}")
    logger.info(f"Temperature: {temperature}, Max tokens: {max_tokens}, Stream: {stream}")
    logger.info(f"Numero messaggi: {len(messages)}")
    for idx, msg in enumerate(messages):
        content_preview = str(msg.get('content', ''))[:200]
        content_len = len(str(msg.get('content', '')))
        logger.info(f"  [{idx}] role={msg.get('role')}, content_len={content_len}")
        logger.info(f"       preview: {content_preview}{'...' if content_len > 200 else ''}")
    logger.info("=" * 80)
    
    try:
        response = requests.post(url, json=payload, timeout=120)
        
        # 🔍 DEBUG: Log della risposta
        logger.info(f"📥 RISPOSTA LLAMA: status={response.status_code}")
        if response.status_code != 200:
            logger.error(f"❌ Errore HTTP {response.status_code}")
            logger.error(f"Response headers: {dict(response.headers)}")
            logger.error(f"Response body: {response.text}")
        
        response.raise_for_status()
        result = response.json()
        
        # Log successo
        if 'choices' in result and len(result['choices']) > 0:
            response_preview = result['choices'][0].get('message', {}).get('content', '')[:100]
            logger.info(f"✅ Risposta OK: {response_preview}...")
        
        return result
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Errore chiamata API llama.cpp: {e}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Response status: {e.response.status_code}")
            logger.error(f"Response headers: {dict(e.response.headers)}")
            logger.error(f"Response body: {e.response.text}")
        raise


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Endpoint per conversazione singola con il chatbot.
    
    Body JSON:
        {
            "message": "Ciao, come stai?",
            "temperature": 0.7,  # opzionale
            "max_tokens": 512,   # opzionale
            "include_entities": true,  # opzionale, include contesto entità HA
            "include_services": false, # opzionale, include contesto servizi HA
            "entity_domains": ["light", "switch"]  # opzionale, filtra per domini
        }
    
    Returns:
        {
            "response": "Risposta del bot",
            "usage": {...}
        }
    """
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Campo 'message' richiesto"}), 400
        
        user_message = data['message']
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 512)
        include_entities = data.get('include_entities', True)
        include_services = data.get('include_services', False)
        entity_domains = data.get('entity_domains')
        
        # Costruisci contesto Home Assistant
        ha_context_text = ""
        if include_entities or include_services:
            try:
                ha_context_text = ha_context.build_full_context(
                    include_entities=include_entities,
                    include_services=include_services,
                    include_system=True,
                    entity_domains=entity_domains
                )
            except Exception as e:
                logger.warning(f"Impossibile ottenere contesto HA: {e}")
                ha_context_text = ""
        
        # Crea messaggio nel formato OpenAI con contesto HA
        system_prompt = "Sei un assistente virtuale per Home Assistant. "
        if ha_context_text:
            system_prompt += "Hai accesso alle seguenti informazioni sul sistema:\n\n" + ha_context_text
        else:
            system_prompt += "Aiuti gli utenti a gestire la loro casa intelligente."
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        # Chiamata al modello
        result = call_llama_api(messages, temperature, max_tokens)
        
        # Estrai risposta
        response_text = result['choices'][0]['message']['content']
        
        return jsonify({
            "response": response_text,
            "usage": result.get('usage', {})
        })
    
    except Exception as e:
        logger.error(f"Errore in /api/chat: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/conversation/start', methods=['POST'])
def start_conversation():
    """
    Avvia una nuova conversazione con ID univoco.
    
    Body JSON:
        {
            "system_prompt": "Sei un assistente..."  # opzionale
        }
    
    Returns:
        {
            "conversation_id": "abc123",
            "message": "Conversazione avviata"
        }
    """
    try:
        data = request.get_json() or {}
        system_prompt = data.get(
            'system_prompt',
            "Sei un assistente virtuale utile e cortese per Home Assistant."
        )
        
        # Genera ID conversazione
        conversation_id = f"conv_{int(time.time())}_{os.urandom(4).hex()}"
        
        # Inizializza conversazione
        conversations[conversation_id] = [
            {"role": "system", "content": system_prompt}
        ]
        
        logger.info(f"Avviata conversazione {conversation_id}")
        
        return jsonify({
            "conversation_id": conversation_id,
            "message": "Conversazione avviata con successo"
        })
    
    except Exception as e:
        logger.error(f"Errore in /api/conversation/start: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/conversation/<conversation_id>/message', methods=['POST'])
def send_message(conversation_id: str):
    """
    Invia un messaggio in una conversazione esistente.
    
    Args:
        conversation_id: ID della conversazione
    
    Body JSON:
        {
            "message": "Qual è la temperatura in casa?",
            "temperature": 0.7,  # opzionale
            "max_tokens": 512    # opzionale
        }
    
    Returns:
        {
            "response": "Risposta del bot",
            "usage": {...}
        }
    """
    try:
        if conversation_id not in conversations:
            return jsonify({"error": "Conversazione non trovata"}), 404
        
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Campo 'message' richiesto"}), 400
        
        user_message = data['message']
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 512)
        
        # Aggiungi messaggio utente alla conversazione
        conversations[conversation_id].append({
            "role": "user",
            "content": user_message
        })
        
        # Chiamata al modello con storia completa
        result = call_llama_api(
            conversations[conversation_id],
            temperature,
            max_tokens
        )
        
        # Estrai risposta
        response_text = result['choices'][0]['message']['content']
        
        # Aggiungi risposta alla conversazione
        conversations[conversation_id].append({
            "role": "assistant",
            "content": response_text
        })
        
        return jsonify({
            "response": response_text,
            "usage": result.get('usage', {}),
            "message_count": len(conversations[conversation_id]) - 1  # -1 per system prompt
        })
    
    except Exception as e:
        logger.error(f"Errore in /api/conversation/{conversation_id}/message: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/conversation/<conversation_id>/history', methods=['GET'])
def get_conversation_history(conversation_id: str):
    """
    Ottiene la storia di una conversazione.
    
    Args:
        conversation_id: ID della conversazione
    
    Returns:
        {
            "conversation_id": "abc123",
            "messages": [...]
        }
    """
    try:
        if conversation_id not in conversations:
            return jsonify({"error": "Conversazione non trovata"}), 404
        
        return jsonify({
            "conversation_id": conversation_id,
            "messages": conversations[conversation_id]
        })
    
    except Exception as e:
        logger.error(f"Errore in /api/conversation/{conversation_id}/history: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/conversation/<conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id: str):
    """
    Elimina una conversazione.
    
    Args:
        conversation_id: ID della conversazione
    
    Returns:
        {
            "message": "Conversazione eliminata"
        }
    """
    try:
        if conversation_id not in conversations:
            return jsonify({"error": "Conversazione non trovata"}), 404
        
        del conversations[conversation_id]
        logger.info(f"Eliminata conversazione {conversation_id}")
        
        return jsonify({
            "message": "Conversazione eliminata con successo"
        })
    
    except Exception as e:
        logger.error(f"Errore in /api/conversation/{conversation_id}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/conversations', methods=['GET'])
def list_conversations():
    """
    Lista tutte le conversazioni attive.
    
    Returns:
        {
            "conversations": [
                {
                    "id": "abc123",
                    "message_count": 5
                }
            ]
        }
    """
    try:
        conv_list = [
            {
                "id": conv_id,
                "message_count": len(messages) - 1  # -1 per system prompt
            }
            for conv_id, messages in conversations.items()
        ]
        
        return jsonify({"conversations": conv_list})
    
    except Exception as e:
        logger.error(f"Errore in /api/conversations: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """
    Health check endpoint.
    
    Returns:
        {
            "status": "ok",
            "llama_server": "ok"
        }
    """
    try:
        # Verifica stato server llama.cpp
        response = requests.get(f"{LLAMA_SERVER_URL}/health", timeout=5)
        llama_status = "ok" if response.status_code == 200 else "error"
    except Exception:
        llama_status = "error"
    
    return jsonify({
        "status": "ok",
        "llama_server": llama_status,
        "active_conversations": len(conversations)
    })


@app.route('/api/models', methods=['GET'])
def get_models():
    """
    Ottiene informazioni sul modello caricato.
    
    Returns:
        {
            "models": [...]
        }
    """
    try:
        response = requests.get(f"{LLAMA_SERVER_URL}/v1/models", timeout=5)
        response.raise_for_status()
        return jsonify(response.json())
    
    except Exception as e:
        logger.error(f"Errore in /api/models: {e}")
        return jsonify({"error": str(e)}), 500


# ========== ENDPOINTS HOME ASSISTANT INTEGRATION ==========

@app.route('/api/ha/entities', methods=['GET'])
def get_ha_entities():
    """
    Ottiene tutte le entità di Home Assistant.
    
    Query params:
        domain: Filtra per dominio (opzionale)
    
    Returns:
        {
            "entities": [...]
        }
    """
    try:
        domain = request.args.get('domain')
        states = ha_client.get_states()
        
        if not states:
            return jsonify({"error": "Impossibile ottenere entità"}), 500
        
        # Filtra per dominio se richiesto
        if domain:
            states = [s for s in states if s.get('entity_id', '').startswith(f'{domain}.')]
        
        return jsonify({"entities": states})
    
    except Exception as e:
        logger.error(f"Errore in /api/ha/entities: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/ha/entity/<path:entity_id>', methods=['GET'])
def get_ha_entity(entity_id: str):
    """
    Ottiene info su un'entità specifica.
    
    Returns:
        {
            "entity_id": "...",
            "state": "...",
            "attributes": {...}
        }
    """
    try:
        states = ha_client.get_states(entity_id)
        
        if not states or not states[0]:
            return jsonify({"error": f"Entità '{entity_id}' non trovata"}), 404
        
        return jsonify(states[0])
    
    except Exception as e:
        logger.error(f"Errore in /api/ha/entity/{entity_id}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/ha/services', methods=['GET'])
def get_ha_services():
    """
    Ottiene tutti i servizi disponibili in Home Assistant.
    
    Returns:
        {
            "services": {...}
        }
    """
    try:
        services = ha_client.get_services()
        
        if not services:
            return jsonify({"error": "Impossibile ottenere servizi"}), 500
        
        return jsonify({"services": services})
    
    except Exception as e:
        logger.error(f"Errore in /api/ha/services: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/ha/service/call', methods=['POST'])
def call_ha_service():
    """
    Chiama un servizio di Home Assistant.
    
    Body JSON:
        {
            "domain": "light",
            "service": "turn_on",
            "entity_id": "light.living_room",  # opzionale
            "data": {...}  # dati aggiuntivi opzionali
        }
    
    Returns:
        {
            "success": true,
            "result": {...}
        }
    """
    try:
        data = request.get_json()
        if not data or 'domain' not in data or 'service' not in data:
            return jsonify({"error": "Campi 'domain' e 'service' richiesti"}), 400
        
        domain = data['domain']
        service = data['service']
        entity_id = data.get('entity_id')
        service_data = data.get('data', {})
        
        result = ha_client.call_service(domain, service, entity_id, **service_data)
        
        if result is None:
            return jsonify({"error": "Errore chiamata servizio"}), 500
        
        return jsonify({
            "success": True,
            "result": result
        })
    
    except Exception as e:
        logger.error(f"Errore in /api/ha/service/call: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/ha/config', methods=['GET'])
def get_ha_config():
    """
    Ottiene la configurazione di Home Assistant.
    
    Returns:
        {
            "config": {...}
        }
    """
    try:
        config = ha_client.get_config()
        
        if not config:
            return jsonify({"error": "Impossibile ottenere configurazione"}), 500
        
        return jsonify({"config": config})
    
    except Exception as e:
        logger.error(f"Errore in /api/ha/config: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/ha/context', methods=['GET'])
def get_ha_context():
    """
    Ottiene il contesto formattato di Home Assistant per il LLM.
    
    Query params:
        entities: Include entità (default: true)
        services: Include servizi (default: false)
        system: Include info di sistema (default: true)
        domains: Lista domini separati da virgola (es: light,switch)
    
    Returns:
        {
            "context": "..."
        }
    """
    try:
        include_entities = request.args.get('entities', 'true').lower() == 'true'
        include_services = request.args.get('services', 'false').lower() == 'true'
        include_system = request.args.get('system', 'true').lower() == 'true'
        domains_param = request.args.get('domains')
        
        entity_domains = domains_param.split(',') if domains_param else None
        
        context = ha_context.build_full_context(
            include_entities=include_entities,
            include_services=include_services,
            include_system=include_system,
            entity_domains=entity_domains
        )
        
        return jsonify({"context": context})
    
    except Exception as e:
        logger.error(f"Errore in /api/ha/context: {e}")
        return jsonify({"error": str(e)}), 500


def main():
    """Main entry point."""
    logger.info("=" * 80)
    logger.info("🔧 Initializing HA Service...")
    logger.info("=" * 80)
    
    # Attendi che llama-server sia pronto
    logger.info("⏳ Waiting for llama-server...")
    if not wait_for_llama_server():
        logger.error("❌ Impossibile connettersi al server llama.cpp")
        sys.exit(1)
    
    logger.info("✅ Llama-server ready!")
    
    # Avvia Flask app
    logger.info("=" * 80)
    logger.info("🚀 Starting Flask API server on port 5000...")
    logger.info("=" * 80)
    
    # Disable Flask's default logging to avoid duplicates
    import logging as flask_logging
    log = flask_logging.getLogger('werkzeug')
    log.setLevel(flask_logging.WARNING)
    
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)


if __name__ == '__main__':
    main()
