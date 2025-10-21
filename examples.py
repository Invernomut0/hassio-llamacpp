"""
Esempi di utilizzo dell'addon Llama.cpp per Home Assistant.
Questi script dimostrano come interagire con le API.
"""

import requests
from typing import Optional


class LlamaHomeAssistant:
    """Client Python per l'addon Llama.cpp Home Assistant."""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        """
        Inizializza il client.
        
        Args:
            base_url: URL base del servizio (default: http://localhost:5000)
        """
        self.base_url = base_url
    
    def chat(
        self,
        message: str,
        temperature: float = 0.7,
        max_tokens: int = 512
    ) -> dict:
        """
        Invia un messaggio singolo al chatbot.
        
        Args:
            message: Testo del messaggio
            temperature: Creatività della risposta (0.0-2.0)
            max_tokens: Massimo numero di token nella risposta
        
        Returns:
            Dizionario con risposta e usage info
        """
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "message": message,
                "temperature": temperature,
                "max_tokens": max_tokens
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json()
    
    def start_conversation(self, system_prompt: Optional[str] = None) -> str:
        """
        Avvia una nuova conversazione.
        
        Args:
            system_prompt: Prompt di sistema opzionale
        
        Returns:
            ID della conversazione
        """
        data = {}
        if system_prompt:
            data["system_prompt"] = system_prompt
        
        response = requests.post(
            f"{self.base_url}/api/conversation/start",
            json=data,
            timeout=10
        )
        response.raise_for_status()
        return response.json()["conversation_id"]
    
    def send_message(
        self,
        conversation_id: str,
        message: str,
        temperature: float = 0.7,
        max_tokens: int = 512
    ) -> dict:
        """
        Invia un messaggio in una conversazione esistente.
        
        Args:
            conversation_id: ID della conversazione
            message: Testo del messaggio
            temperature: Creatività della risposta
            max_tokens: Massimo numero di token
        
        Returns:
            Dizionario con risposta e usage info
        """
        response = requests.post(
            f"{self.base_url}/api/conversation/{conversation_id}/message",
            json={
                "message": message,
                "temperature": temperature,
                "max_tokens": max_tokens
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json()
    
    def get_history(self, conversation_id: str) -> list:
        """
        Ottiene la storia di una conversazione.
        
        Args:
            conversation_id: ID della conversazione
        
        Returns:
            Lista di messaggi
        """
        response = requests.get(
            f"{self.base_url}/api/conversation/{conversation_id}/history",
            timeout=10
        )
        response.raise_for_status()
        return response.json()["messages"]
    
    def delete_conversation(self, conversation_id: str):
        """
        Elimina una conversazione.
        
        Args:
            conversation_id: ID della conversazione
        """
        response = requests.delete(
            f"{self.base_url}/api/conversation/{conversation_id}",
            timeout=10
        )
        response.raise_for_status()
    
    def list_conversations(self) -> list:
        """
        Lista tutte le conversazioni attive.
        
        Returns:
            Lista di conversazioni
        """
        response = requests.get(
            f"{self.base_url}/api/conversations",
            timeout=10
        )
        response.raise_for_status()
        return response.json()["conversations"]
    
    def health(self) -> dict:
        """
        Verifica lo stato del servizio.
        
        Returns:
            Stato del servizio
        """
        response = requests.get(
            f"{self.base_url}/api/health",
            timeout=10
        )
        response.raise_for_status()
        return response.json()


# Esempi di utilizzo

def example_simple_chat():
    """Esempio 1: Chat singolo."""
    print("\n" + "="*70)
    print("ESEMPIO 1: Chat Singolo")
    print("="*70 + "\n")
    
    client = LlamaHomeAssistant()
    
    # Domanda semplice
    result = client.chat(
        "Ciao! Dimmi 3 consigli per risparmiare energia in casa.",
        temperature=0.8
    )
    
    print("Domanda: Ciao! Dimmi 3 consigli per risparmiare energia in casa.")
    print(f"\nRisposta:\n{result['response']}")
    print(f"\nToken usati: {result['usage']}")


def example_conversation():
    """Esempio 2: Conversazione multi-turno."""
    print("\n" + "="*70)
    print("ESEMPIO 2: Conversazione Multi-Turno")
    print("="*70 + "\n")
    
    client = LlamaHomeAssistant()
    
    # Avvia conversazione con contesto
    conv_id = client.start_conversation(
        system_prompt="Sei un esperto di domotica e automazione domestica."
    )
    print(f"Conversazione avviata: {conv_id}\n")
    
    # Serie di messaggi correlati
    messages = [
        "Come posso automatizzare le luci in base alla presenza?",
        "E se volessi anche considerare la luminosità esterna?",
        "Quali sensori mi servono?"
    ]
    
    for i, msg in enumerate(messages, 1):
        print(f"[{i}] Tu: {msg}")
        result = client.send_message(conv_id, msg)
        print(f"[{i}] Bot: {result['response']}\n")
    
    # Mostra storia completa
    history = client.get_history(conv_id)
    print(f"Storia conversazione: {len(history)} messaggi totali")
    
    # Cleanup
    client.delete_conversation(conv_id)
    print(f"\nConversazione eliminata: {conv_id}")


def example_batch_questions():
    """Esempio 3: Domande multiple indipendenti."""
    print("\n" + "="*70)
    print("ESEMPIO 3: Batch di Domande Indipendenti")
    print("="*70 + "\n")
    
    client = LlamaHomeAssistant()
    
    questions = [
        "Che temperatura dovrei impostare per risparmiare?",
        "Quando è meglio usare la lavatrice?",
        "Come posso monitorare i consumi elettrici?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"[{i}] Domanda: {question}")
        result = client.chat(question, temperature=0.7, max_tokens=200)
        print(f"    Risposta: {result['response'][:100]}...")
        print()


def example_health_check():
    """Esempio 4: Health check e monitoring."""
    print("\n" + "="*70)
    print("ESEMPIO 4: Health Check")
    print("="*70 + "\n")
    
    client = LlamaHomeAssistant()
    
    health = client.health()
    print(f"Stato servizio: {health['status']}")
    print(f"Stato llama.cpp: {health['llama_server']}")
    print(f"Conversazioni attive: {health['active_conversations']}")
    
    conversations = client.list_conversations()
    print(f"\nConversazioni in memoria: {len(conversations)}")
    for conv in conversations:
        print(f"  - {conv['id']}: {conv['message_count']} messaggi")


def example_home_automation():
    """Esempio 5: Integrazione con automazione."""
    print("\n" + "="*70)
    print("ESEMPIO 5: Scenario Automazione Domestica")
    print("="*70 + "\n")
    
    client = LlamaHomeAssistant()
    
    # Simula richiesta da automazione HA
    scenario = """
    L'utente sta uscendo di casa. 
    Temperatura esterna: 15°C
    Ora: 18:30
    Luci accese: Soggiorno, Cucina
    Termostato: 21°C
    
    Suggerisci 3 azioni da automatizzare per ottimizzare energia e sicurezza.
    """
    
    result = client.chat(scenario, temperature=0.5, max_tokens=300)
    
    print("Scenario:")
    print(scenario)
    print("\nSuggerimenti AI:")
    print(result['response'])


if __name__ == "__main__":
    # Esegui tutti gli esempi
    try:
        example_simple_chat()
        example_conversation()
        example_batch_questions()
        example_health_check()
        example_home_automation()
        
        print("\n" + "="*70)
        print("TUTTI GLI ESEMPI COMPLETATI CON SUCCESSO!")
        print("="*70 + "\n")
    
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRORE: Impossibile connettersi al servizio.")
        print("Assicurati che l'addon sia in esecuzione su http://localhost:5000")
    
    except Exception as e:
        print(f"\n❌ ERRORE: {e}")
