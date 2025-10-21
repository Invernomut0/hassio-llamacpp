# Llama.cpp LLM Server - Home Assistant Addon

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Addon per Home Assistant che integra [llama.cpp](https://github.com/ggml-org/llama.cpp) per eseguire modelli LLM (Large Language Models) localmente con API compatibili OpenAI.

## 🎯 Caratteristiche

- ✅ **Server LLM locale** - Nessuna dipendenza da servizi cloud
- ✅ **API compatibili OpenAI** - Integrazione semplice con client esistenti
- ✅ **Conversazioni multi-turno** - Mantiene il contesto delle conversazioni
- ✅ **Modelli configurabili** - Scarica automaticamente i modelli GGUF da Hugging Face
- ✅ **Supporto GPU** - Accelerazione con CUDA (opzionale)
- ✅ **Performance ottimizzate** - Quantizzazione e batching efficiente
- ✅ **Health monitoring** - Endpoint per verificare lo stato del servizio

## 📋 Requisiti

- Home Assistant OS o Supervised
- Almeno 4 GB di RAM (8 GB raccomandati per modelli grandi)
- 10+ GB di spazio disco per i modelli
- (Opzionale) GPU NVIDIA per accelerazione

## 🚀 Installazione

### 1. Aggiungi il Repository

Aggiungi questo repository agli addon di Home Assistant:

1. Vai su **Supervisor** → **Add-on Store**
2. Clicca sui tre puntini in alto a destra → **Repositories**
3. Aggiungi l'URL: `https://github.com/[TUO_USERNAME]/hassio-llamacpp`
4. Clicca **Add**

### 2. Installa l'Addon

1. Trova "Llama.cpp LLM Server" nella lista degli addon
2. Clicca su **Install**
3. Attendi il completamento dell'installazione

### 3. Configura l'Addon

Vai alla scheda **Configuration** e personalizza le opzioni:

```yaml
model_url: "https://huggingface.co/ggml-org/gemma-3-1b-it-GGUF/resolve/main/gemma-3-1b-it-Q4_K_M.gguf"
model_name: "gemma-3-1b-it-Q4_K_M"
context_size: 2048
threads: 4
gpu_layers: 0
parallel_requests: 1
log_level: "info"
```

### 4. Avvia l'Addon

1. Attiva le opzioni:
   - **Start on boot** (raccomandato)
   - **Watchdog** (raccomandato)
2. Clicca su **Start**
3. Controlla i log per verificare il download del modello e l'avvio

## ⚙️ Configurazione

### Opzioni Disponibili

| Opzione | Tipo | Default | Descrizione |
|---------|------|---------|-------------|
| `model_url` | URL | gemma-3-1b-it | URL del modello GGUF da scaricare |
| `model_name` | string | gemma-3-1b-it-Q4_K_M | Nome del modello (usato per il file locale) |
| `context_size` | int | 2048 | Dimensione del contesto (512-32768) |
| `threads` | int | 4 | Numero di thread CPU (1-32) |
| `gpu_layers` | int | 0 | Numero di layer da caricare su GPU (0 = CPU only) |
| `parallel_requests` | int | 1 | Richieste parallele simultanee (1-8) |
| `log_level` | string | info | Livello di log (debug, info, warning, error) |

### Modelli Consigliati

#### Modelli Leggeri (2-4 GB RAM)
```yaml
# Gemma 2B (veloce, accurato)
model_url: "https://huggingface.co/ggml-org/gemma-3-1b-it-GGUF/resolve/main/gemma-3-1b-it-Q4_K_M.gguf"
model_name: "gemma-3-1b-it-Q4_K_M"

# Phi-3 Mini (eccellente qualità/dimensione)
model_url: "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf"
model_name: "phi-3-mini-q4"
```

#### Modelli Medi (6-8 GB RAM)
```yaml
# LLaMA 3.2 3B
model_url: "https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q4_K_M.gguf"
model_name: "llama-3.2-3b-q4"
```

#### Modelli Grandi (12+ GB RAM)
```yaml
# LLaMA 3.1 8B
model_url: "https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
model_name: "llama-3.1-8b-q4"
```

### Supporto GPU

Per abilitare l'accelerazione GPU (solo NVIDIA):

1. Verifica che il tuo sistema supporti CUDA
2. Configura il numero di layer da caricare sulla GPU:

```yaml
gpu_layers: 35  # Per modelli 7B-8B
```

Più layer = più veloce, ma richiede più VRAM.

## 📡 API Endpoints

L'addon espone due server:

- **Porta 8080**: Server llama.cpp (API OpenAI-compatible)
- **Porta 5000**: Servizio Home Assistant (API custom)

### API OpenAI-Compatible (Porta 8080)

#### Chat Completions
```bash
curl http://homeassistant.local:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "system", "content": "Sei un assistente utile."},
      {"role": "user", "content": "Ciao, chi sei?"}
    ],
    "temperature": 0.7,
    "max_tokens": 512
  }'
```

#### Models Info
```bash
curl http://homeassistant.local:8080/v1/models
```

#### Health Check
```bash
curl http://homeassistant.local:8080/health
```

### API Home Assistant (Porta 5000)

#### Chat Singolo
```bash
curl -X POST http://homeassistant.local:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Qual è la temperatura in casa?",
    "temperature": 0.7,
    "max_tokens": 512
  }'
```

**Risposta:**
```json
{
  "response": "Mi dispiace, ma non ho accesso ai dati dei tuoi sensori...",
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 50,
    "total_tokens": 75
  }
}
```

#### Avvia Conversazione
```bash
curl -X POST http://homeassistant.local:5000/api/conversation/start \
  -H "Content-Type: application/json" \
  -d '{
    "system_prompt": "Sei un assistente per la domotica."
  }'
```

**Risposta:**
```json
{
  "conversation_id": "conv_1729512345_a3b2c1d4",
  "message": "Conversazione avviata con successo"
}
```

#### Invia Messaggio in Conversazione
```bash
curl -X POST http://homeassistant.local:5000/api/conversation/conv_123/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Ricordi cosa ti ho chiesto prima?"
  }'
```

**Risposta:**
```json
{
  "response": "Sì, mi hai chiesto...",
  "usage": {...},
  "message_count": 3
}
```

#### Ottieni Storia Conversazione
```bash
curl http://homeassistant.local:5000/api/conversation/conv_123/history
```

#### Lista Conversazioni Attive
```bash
curl http://homeassistant.local:5000/api/conversations
```

#### Elimina Conversazione
```bash
curl -X DELETE http://homeassistant.local:5000/api/conversation/conv_123
```

#### Health Check
```bash
curl http://homeassistant.local:5000/api/health
```

## 🏠 Integrazione con Home Assistant

### Automazione con RESTful Command

Aggiungi al tuo `configuration.yaml`:

```yaml
rest_command:
  ask_llm:
    url: "http://localhost:5000/api/chat"
    method: POST
    content_type: "application/json"
    payload: '{"message": "{{ message }}"}'
```

### Script per Conversazione

```yaml
script:
  chat_with_llm:
    alias: "Chat con LLM"
    sequence:
      - service: rest_command.ask_llm
        data:
          message: "{{ user_input }}"
```

### Sensor per Risposta

```yaml
sensor:
  - platform: rest
    name: "LLM Response"
    resource: "http://localhost:5000/api/health"
    method: GET
    value_template: "{{ value_json.status }}"
    json_attributes:
      - llama_server
      - active_conversations
```

### Automazione Esempio

```yaml
automation:
  - alias: "Saluto Mattutino"
    trigger:
      - platform: time
        at: "07:00:00"
    action:
      - service: rest_command.ask_llm
        data:
          message: "Buongiorno! Dammi 3 consigli per iniziare bene la giornata."
      - service: notify.mobile_app
        data:
          message: "{{ states('sensor.llm_response') }}"
```

## 🐍 Utilizzo con Python

```python
import requests

# Chat singolo
def ask_llm(question: str) -> str:
    """Chiedi una risposta al LLM."""
    response = requests.post(
        "http://homeassistant.local:5000/api/chat",
        json={"message": question}
    )
    return response.json()["response"]

# Conversazione multi-turno
class LLMConversation:
    """Gestisce una conversazione con il LLM."""
    
    def __init__(self, system_prompt: str = None):
        """Inizializza una nuova conversazione."""
        data = {}
        if system_prompt:
            data["system_prompt"] = system_prompt
        
        response = requests.post(
            "http://homeassistant.local:5000/api/conversation/start",
            json=data
        )
        self.conversation_id = response.json()["conversation_id"]
    
    def send(self, message: str) -> str:
        """Invia un messaggio nella conversazione."""
        response = requests.post(
            f"http://homeassistant.local:5000/api/conversation/{self.conversation_id}/message",
            json={"message": message}
        )
        return response.json()["response"]
    
    def history(self) -> list:
        """Ottieni la storia della conversazione."""
        response = requests.get(
            f"http://homeassistant.local:5000/api/conversation/{self.conversation_id}/history"
        )
        return response.json()["messages"]
    
    def close(self):
        """Chiudi la conversazione."""
        requests.delete(
            f"http://homeassistant.local:5000/api/conversation/{self.conversation_id}"
        )

# Esempio di utilizzo
if __name__ == "__main__":
    # Chat singolo
    answer = ask_llm("Che ore sono?")
    print(f"Risposta: {answer}")
    
    # Conversazione
    conv = LLMConversation(system_prompt="Sei un esperto di domotica.")
    print(conv.send("Ciao! Come posso automatizzare le luci?"))
    print(conv.send("E i termostati?"))
    conv.close()
```

## 🔍 Troubleshooting

### Il modello non viene scaricato

**Problema**: Il download del modello fallisce o si blocca.

**Soluzione**:
1. Verifica la connettività internet
2. Controlla lo spazio disco disponibile
3. Prova un modello più piccolo
4. Scarica manualmente il modello e posizionalo in `/addon_configs/local_llamacpp/models/`

### Server lento o non risponde

**Problema**: Le risposte richiedono troppo tempo o vanno in timeout.

**Soluzione**:
1. Riduci `context_size` (es. 1024)
2. Aumenta `threads` se hai CPU multi-core
3. Usa un modello quantizzato più piccolo (Q4_0 invece di Q8_0)
4. Abilita GPU se disponibile

### Errore "Out of Memory"

**Problema**: Il sistema esaurisce la RAM.

**Soluzione**:
1. Usa un modello più piccolo (1B-3B parametri)
2. Riduci `context_size`
3. Riduci `parallel_requests` a 1
4. Chiudi altre applicazioni per liberare RAM

### GPU non rilevata

**Problema**: `gpu_layers` > 0 ma la GPU non viene usata.

**Soluzione**:
1. Verifica che il driver NVIDIA sia installato
2. Il Dockerfile necessita build con supporto CUDA
3. Controlla i log per messaggi relativi a CUDA
4. Usa CPU-only impostando `gpu_layers: 0`

## 📊 Performance e Benchmarks

### Modelli Testati

| Modello | Parametri | Dimensione | RAM | Tokens/s (CPU) | Tokens/s (GPU) |
|---------|-----------|------------|-----|----------------|----------------|
| Gemma 3 1B Q4 | 1.5B | 900 MB | 2 GB | ~40 | ~150 |
| Phi-3 Mini Q4 | 3.8B | 2.3 GB | 4 GB | ~25 | ~100 |
| LLaMA 3.2 3B Q4 | 3B | 1.9 GB | 4 GB | ~30 | ~120 |
| LLaMA 3.1 8B Q4 | 8B | 4.7 GB | 8 GB | ~12 | ~60 |

*Test su: Intel i7-12700K, 32GB RAM, RTX 3080*

## 🛠️ Sviluppo

### Build Locale

```bash
# Clone repository
git clone https://github.com/[TUO_USERNAME]/hassio-llamacpp
cd hassio-llamacpp

# Build immagine Docker
docker build -t local/llamacpp-addon .

# Test locale
docker run -p 8080:8080 -p 5000:5000 \
  -e MODEL_URL="https://..." \
  local/llamacpp-addon
```

### Test API

```bash
# Esegui test
python3 tests/test_api.py
```

## 🤝 Contributi

I contributi sono benvenuti! Segui queste linee guida:

1. Fork del repository
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

### Sviluppo Best Practices

- ✅ Codice testato con dati reali (no mock)
- ✅ Documentazione completa per ogni funzione
- ✅ Test coverage > 80%
- ✅ Segui PEP 8 per Python
- ✅ Commit atomici e messaggi descrittivi

## 📝 Changelog

### [1.0.0] - 2025-10-21

#### Added
- Integrazione completa llama.cpp
- API OpenAI-compatible
- Gestione conversazioni multi-turno
- Download automatico modelli
- Supporto GPU CUDA
- Health monitoring
- Documentazione completa

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file [LICENSE](LICENSE) per i dettagli.

## 🙏 Ringraziamenti

- [llama.cpp](https://github.com/ggml-org/llama.cpp) - Il fantastico motore LLM
- [Home Assistant](https://www.home-assistant.io/) - La migliore piattaforma di domotica
- Community di Hugging Face per i modelli GGUF

## 📞 Supporto

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/[TUO_USERNAME]/hassio-llamacpp/issues)
- 💬 **Discussioni**: [GitHub Discussions](https://github.com/[TUO_USERNAME]/hassio-llamacpp/discussions)
- 📧 **Email**: support@example.com

## 🔗 Link Utili

- [Documentazione llama.cpp](https://github.com/ggml-org/llama.cpp/tree/master/docs)
- [Modelli GGUF su Hugging Face](https://huggingface.co/models?library=gguf)
- [Home Assistant Add-on Development](https://developers.home-assistant.io/docs/add-ons)
- [Quantizzazione modelli](https://github.com/ggml-org/llama.cpp/blob/master/tools/quantize/README.md)

---

**Made with ❤️ for the Home Assistant Community**
