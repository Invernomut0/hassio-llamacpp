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

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Flask app per servizi Home Assistant
app = Flask(__name__)
CORS(app)

# URL del server llama.cpp locale
LLAMA_SERVER_URL = "http://localhost:8080"

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
    
    payload = {
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream
    }
    
    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Errore chiamata API llama.cpp: {e}")
        raise


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Endpoint per conversazione singola con il chatbot.
    
    Body JSON:
        {
            "message": "Ciao, come stai?",
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
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Campo 'message' richiesto"}), 400
        
        user_message = data['message']
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 512)
        
        # Crea messaggio nel formato OpenAI
        messages = [
            {"role": "system", "content": "Sei un assistente virtuale utile e cortese per Home Assistant."},
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


def main():
    """Main entry point."""
    # Attendi che llama-server sia pronto
    if not wait_for_llama_server():
        logger.error("Impossibile connettersi al server llama.cpp")
        sys.exit(1)
    
    # Avvia Flask app
    logger.info("Avvio servizio Home Assistant API su porta 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False)


if __name__ == '__main__':
    main()
