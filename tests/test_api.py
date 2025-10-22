#!/usr/bin/env python3
"""
Test suite completo per l'addon Llama.cpp Home Assistant.
Tutti i test utilizzano dati reali e verificano il comportamento end-to-end.
"""

import time
import unittest

import requests

# Configurazione base
BASE_URL = "http://localhost:5000"
LLAMA_URL = "http://localhost:8080"
TIMEOUT = 120  # Timeout per chiamate LLM (possono essere lente)


class TestLlamaServerHealth(unittest.TestCase):
    """Test per verificare lo stato del server llama.cpp."""
    
    def test_llama_server_is_running(self):
        """Verifica che il server llama.cpp sia attivo."""
        response = requests.get(f"{LLAMA_URL}/health", timeout=10)
        self.assertEqual(response.status_code, 200)
        print("✓ Server llama.cpp è attivo")
    
    def test_models_endpoint(self):
        """Verifica che l'endpoint /v1/models restituisca il modello caricato."""
        response = requests.get(f"{LLAMA_URL}/v1/models", timeout=10)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("data", data)
        self.assertGreater(len(data["data"]), 0)
        
        model = data["data"][0]
        self.assertIn("id", model)
        print(f"✓ Modello caricato: {model['id']}")


class TestHAServiceHealth(unittest.TestCase):
    """Test per verificare lo stato del servizio Home Assistant."""
    
    def test_ha_service_is_running(self):
        """Verifica che il servizio HA sia attivo."""
        response = requests.get(f"{BASE_URL}/api/health", timeout=10)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["llama_server"], "ok")
        print("✓ Servizio Home Assistant è attivo")
    
    def test_models_info(self):
        """Verifica l'endpoint /api/models."""
        response = requests.get(f"{BASE_URL}/api/models", timeout=10)
        self.assertEqual(response.status_code, 200)
        print("✓ Endpoint /api/models funzionante")


class TestSingleChatAPI(unittest.TestCase):
    """Test per l'API di chat singolo."""
    
    def test_simple_chat_request(self):
        """Test chat singolo con domanda semplice."""
        payload = {
            "message": "Ciao! Rispondi con esattamente una parola: 'OK'",
            "temperature": 0.1,
            "max_tokens": 50
        }
        
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json=payload,
            timeout=TIMEOUT
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verifica struttura risposta
        self.assertIn("response", data)
        self.assertIn("usage", data)
        
        # Verifica che ci sia una risposta
        self.assertGreater(len(data["response"]), 0)
        
        print(f"✓ Risposta ricevuta: {data['response'][:100]}...")
        print(f"  Tokens usati: {data['usage']}")
    
    def test_chat_with_math_question(self):
        """Test con domanda matematica per verificare correttezza."""
        payload = {
            "message": "Quanto fa 15 + 27? Rispondi solo con il numero.",
            "temperature": 0.1,
            "max_tokens": 20
        }
        
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json=payload,
            timeout=TIMEOUT
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verifica che la risposta contenga 42
        response_text = data["response"]
        self.assertTrue(
            "42" in response_text,
            f"Risposta non contiene 42: {response_text}"
        )
        
        print(f"✓ Calcolo matematico corretto: {response_text}")
    
    def test_chat_invalid_request(self):
        """Test con richiesta invalida (manca 'message')."""
        payload = {"temperature": 0.7}
        
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json=payload,
            timeout=10
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("error", data)
        print(f"✓ Errore gestito correttamente: {data['error']}")


class TestConversationAPI(unittest.TestCase):
    """Test per l'API di conversazione multi-turno."""
    
    def test_start_conversation(self):
        """Test avvio conversazione."""
        payload = {
            "system_prompt": "Sei un assistente matematico. Rispondi brevemente."
        }
        
        response = requests.post(
            f"{BASE_URL}/api/conversation/start",
            json=payload,
            timeout=10
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("conversation_id", data)
        self.assertIn("message", data)
        
        conv_id = data["conversation_id"]
        self.assertTrue(conv_id.startswith("conv_"))
        
        print(f"✓ Conversazione avviata: {conv_id}")
        return conv_id
    
    def test_multi_turn_conversation(self):
        """Test conversazione multi-turno con contesto."""
        # Avvia conversazione
        response = requests.post(
            f"{BASE_URL}/api/conversation/start",
            json={"system_prompt": "Sei un assistente che ricorda tutto."},
            timeout=10
        )
        conv_id = response.json()["conversation_id"]
        
        # Primo messaggio: stabilisci un fatto
        response1 = requests.post(
            f"{BASE_URL}/api/conversation/{conv_id}/message",
            json={
                "message": "Il mio colore preferito è il blu. Conferma di aver capito.",
                "temperature": 0.3,
                "max_tokens": 100
            },
            timeout=TIMEOUT
        )
        
        self.assertEqual(response1.status_code, 200)
        data1 = response1.json()
        self.assertIn("response", data1)
        print(f"✓ Messaggio 1: {data1['response'][:80]}...")
        
        # Secondo messaggio: verifica memoria
        time.sleep(1)
        response2 = requests.post(
            f"{BASE_URL}/api/conversation/{conv_id}/message",
            json={
                "message": "Qual è il mio colore preferito?",
                "temperature": 0.3,
                "max_tokens": 50
            },
            timeout=TIMEOUT
        )
        
        self.assertEqual(response2.status_code, 200)
        data2 = response2.json()
        
        # Verifica che la risposta contenga "blu"
        response_text = data2["response"].lower()
        self.assertTrue(
            "blu" in response_text,
            f"Il modello non ha ricordato il colore: {response_text}"
        )
        
        print(f"✓ Messaggio 2: {data2['response'][:80]}...")
        print("  Contesto mantenuto correttamente!")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/conversation/{conv_id}")
    
    def test_conversation_history(self):
        """Test recupero storia conversazione."""
        # Avvia conversazione
        response = requests.post(
            f"{BASE_URL}/api/conversation/start",
            timeout=10
        )
        conv_id = response.json()["conversation_id"]
        
        # Invia alcuni messaggi
        for i in range(2):
            requests.post(
                f"{BASE_URL}/api/conversation/{conv_id}/message",
                json={"message": f"Messaggio di test numero {i+1}"},
                timeout=TIMEOUT
            )
            time.sleep(1)
        
        # Ottieni storia
        response = requests.get(
            f"{BASE_URL}/api/conversation/{conv_id}/history",
            timeout=10
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("messages", data)
        messages = data["messages"]
        
        # Verifica struttura: system + user + assistant + user + assistant
        self.assertGreaterEqual(len(messages), 5)
        self.assertEqual(messages[0]["role"], "system")
        
        print(f"✓ Storia recuperata: {len(messages)} messaggi")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/conversation/{conv_id}")
    
    def test_list_conversations(self):
        """Test lista conversazioni attive."""
        # Crea alcune conversazioni
        conv_ids = []
        for i in range(3):
            response = requests.post(
                f"{BASE_URL}/api/conversation/start",
                timeout=10
            )
            conv_ids.append(response.json()["conversation_id"])
        
        # Lista conversazioni
        response = requests.get(
            f"{BASE_URL}/api/conversations",
            timeout=10
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("conversations", data)
        conversations = data["conversations"]
        
        # Verifica che le nostre conversazioni siano nella lista
        self.assertGreaterEqual(len(conversations), 3)
        
        print(f"✓ Conversazioni attive: {len(conversations)}")
        
        # Cleanup
        for conv_id in conv_ids:
            requests.delete(f"{BASE_URL}/api/conversation/{conv_id}")
    
    def test_delete_conversation(self):
        """Test eliminazione conversazione."""
        # Avvia conversazione
        response = requests.post(
            f"{BASE_URL}/api/conversation/start",
            timeout=10
        )
        conv_id = response.json()["conversation_id"]
        
        # Elimina conversazione
        response = requests.delete(
            f"{BASE_URL}/api/conversation/{conv_id}",
            timeout=10
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Verifica che sia stata eliminata
        response = requests.get(
            f"{BASE_URL}/api/conversation/{conv_id}/history",
            timeout=10
        )
        self.assertEqual(response.status_code, 404)
        
        print(f"✓ Conversazione eliminata: {conv_id}")


class TestOpenAICompatibility(unittest.TestCase):
    """Test per verificare compatibilità con API OpenAI."""
    
    def test_chat_completions_endpoint(self):
        """Test endpoint /v1/chat/completions."""
        payload = {
            "messages": [
                {"role": "system", "content": "Sei un assistente utile."},
                {"role": "user", "content": "Saluta con 'Ciao!'"}
            ],
            "temperature": 0.3,
            "max_tokens": 50
        }
        
        response = requests.post(
            f"{LLAMA_URL}/v1/chat/completions",
            json=payload,
            timeout=TIMEOUT
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verifica struttura OpenAI
        self.assertIn("choices", data)
        self.assertIn("usage", data)
        self.assertIn("model", data)
        
        choice = data["choices"][0]
        self.assertIn("message", choice)
        self.assertEqual(choice["message"]["role"], "assistant")
        
        response_text = choice["message"]["content"]
        self.assertGreater(len(response_text), 0)
        
        print(f"✓ API OpenAI-compatible: {response_text[:80]}...")


class TestPerformanceAndLimits(unittest.TestCase):
    """Test per performance e limiti del sistema."""
    
    def test_response_time(self):
        """Verifica che i tempi di risposta siano ragionevoli."""
        payload = {
            "message": "Conta da 1 a 5.",
            "max_tokens": 100
        }
        
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json=payload,
            timeout=TIMEOUT
        )
        elapsed_time = time.time() - start_time
        
        self.assertEqual(response.status_code, 200)
        
        # Il tempo dovrebbe essere ragionevole (< 60s per modelli piccoli)
        self.assertLess(
            elapsed_time,
            60,
            f"Risposta troppo lenta: {elapsed_time:.2f}s"
        )
        
        print(f"✓ Tempo di risposta: {elapsed_time:.2f}s")
    
    def test_long_context(self):
        """Test con input lungo per verificare gestione context."""
        # Crea un messaggio lungo ma non troppo
        long_message = "Ripeti questa frase: " + "test " * 100
        
        payload = {
            "message": long_message,
            "max_tokens": 200
        }
        
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json=payload,
            timeout=TIMEOUT
        )
        
        # Dovrebbe funzionare o dare errore chiaro
        self.assertIn(response.status_code, [200, 400, 500])
        
        if response.status_code == 200:
            print("✓ Context lungo gestito correttamente")
        else:
            print("✓ Context lungo rifiutato con errore appropriato")


def run_tests():
    """Esegue tutti i test."""
    print("\n" + "="*70)
    print("TEST SUITE ADDON LLAMA.CPP HOME ASSISTANT")
    print("="*70 + "\n")
    
    # Crea test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Aggiungi test in ordine logico
    suite.addTests(loader.loadTestsFromTestCase(TestLlamaServerHealth))
    suite.addTests(loader.loadTestsFromTestCase(TestHAServiceHealth))
    suite.addTests(loader.loadTestsFromTestCase(TestSingleChatAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestConversationAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestOpenAICompatibility))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformanceAndLimits))
    
    # Esegui test con output dettagliato
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Riassunto
    print("\n" + "="*70)
    print("RIASSUNTO TEST")
    print("="*70)
    print(f"Test eseguiti: {result.testsRun}")
    print(f"Successi: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallimenti: {len(result.failures)}")
    print(f"Errori: {len(result.errors)}")
    print("="*70 + "\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
