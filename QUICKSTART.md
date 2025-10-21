# Guida Quick Start

Questa guida ti permetterà di avere il tuo addon LLM funzionante in pochi minuti.

## 🚀 Installazione Rapida

### 1. Aggiungi Repository

In Home Assistant:
1. Vai su **Supervisor** → **Add-on Store** → **⋮** (menu) → **Repositories**
2. Aggiungi: `https://github.com/[TUO_USERNAME]/hassio-llamacpp`

### 2. Installa Addon

1. Trova "Llama.cpp LLM Server" nella lista
2. Click **Install** (ci vorranno ~10-15 minuti per la prima build)
3. Aspetta il completamento

### 3. Configura (Opzionale)

L'addon funziona out-of-the-box con Gemma 3 1B. Per cambiare modello:

```yaml
model_url: "https://huggingface.co/ggml-org/gemma-3-1b-it-GGUF/resolve/main/gemma-3-1b-it-Q4_K_M.gguf"
model_name: "gemma-3-1b-it-Q4_K_M"
context_size: 2048
threads: 4
gpu_layers: 0
parallel_requests: 1
log_level: "info"
```

### 4. Avvia

1. Attiva **Start on boot** e **Watchdog**
2. Click **Start**
3. Controlla i log: vedrai il download del modello (~1GB)

### 5. Testa

Dopo l'avvio (controlla nei log "Avvio llama-server..."):

```bash
curl -X POST http://homeassistant.local:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Ciao! Dimmi ciao in 3 lingue."}'
```

Dovresti ricevere una risposta JSON con il testo generato!

## 💬 Primo Utilizzo

### Chat Singolo

```python
import requests

response = requests.post(
    "http://homeassistant.local:5000/api/chat",
    json={"message": "Come posso automatizzare le luci?"}
)

print(response.json()["response"])
```

### Conversazione

```python
import requests

# Avvia conversazione
start = requests.post(
    "http://homeassistant.local:5000/api/conversation/start",
    json={"system_prompt": "Sei un esperto di domotica."}
)
conv_id = start.json()["conversation_id"]

# Invia messaggi
for msg in ["Ciao!", "Come automatizzare le luci?", "E i termostati?"]:
    response = requests.post(
        f"http://homeassistant.local:5000/api/conversation/{conv_id}/message",
        json={"message": msg}
    )
    print(f"Bot: {response.json()['response']}")

# Cleanup
requests.delete(f"http://homeassistant.local:5000/api/conversation/{conv_id}")
```

## 🏠 Integrazione Home Assistant

### Automazione Base

`configuration.yaml`:
```yaml
rest_command:
  ask_llm:
    url: "http://localhost:5000/api/chat"
    method: POST
    content_type: "application/json"
    payload: '{"message": "{{ message }}"}'

automation:
  - alias: "Consiglio Mattutino"
    trigger:
      - platform: time
        at: "07:00:00"
    action:
      - service: rest_command.ask_llm
        data:
          message: "Dammi un consiglio energetico per oggi."
```

## 🔧 Troubleshooting Rapido

### L'addon non si avvia
- Controlla i log per errori specifici
- Verifica spazio disco (serve ~10GB)
- Prova un modello più piccolo

### Download modello lento
- È normale, i modelli sono grandi (500MB-5GB)
- Il download avviene solo la prima volta
- Controlla la tua connessione internet

### Risposte lente
- Riduci `context_size` a 1024
- Aumenta `threads` se hai più CPU
- Usa un modello più piccolo (1B-3B parametri)

### Errore "Out of Memory"
- Usa un modello quantizzato più aggressivamente (Q4_0 invece di Q8_0)
- Riduci `context_size`
- Chiudi altre applicazioni

## 📚 Prossimi Passi

1. Leggi il [README completo](README.md) per funzionalità avanzate
2. Esplora gli [esempi Python](examples.py)
3. Testa l'API con [test suite](tests/test_api.py)
4. Consulta [TODO.md](TODO.md) per roadmap futura

## 💡 Modelli Consigliati

### Per sistemi con 4GB RAM
- **Gemma 3 1B** (default) - Veloce e accurato
- **Phi-3 Mini** - Ottimo rapporto qualità/dimensione

### Per sistemi con 8GB RAM
- **LLaMA 3.2 3B** - Più potente, ottime prestazioni

### Per sistemi con 12GB+ RAM
- **LLaMA 3.1 8B** - Massima qualità

## 🎯 Casi d'Uso Comuni

### Assistente Vocale
Integra con TTS/STT per controllo vocale della casa.

### Automazioni Intelligenti
Genera suggerimenti per automazioni basate su pattern.

### Notifiche Personalizzate
Crea messaggi di notifica contestuali e naturali.

### Q&A sulla Casa
Rispondi a domande su dispositivi e sensori.

### Analisi Consumi
Fornisci insight sui dati energetici.

---

**Hai problemi?** Apri un [issue su GitHub](https://github.com/[TUO_USERNAME]/hassio-llamacpp/issues)!
