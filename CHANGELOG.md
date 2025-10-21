# Changelog

Tutte le modifiche significative a questo progetto saranno documentate in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/it/1.0.0/),
e questo progetto aderisce al [Semantic Versioning](https://semver.org/lang/it/).

## [1.0.4] - 2025-01-15

### 🆕 Aggiunto - Home Assistant Integration
- 🏠 **Integrazione completa con Home Assistant**
  - Nuovo modulo `ha_integration.py` con client per Supervisor API
  - Classe `HomeAssistantClient` per accesso a entità, servizi, configurazione
  - Classe `HAContextBuilder` per costruzione contesto intelligente per LLM
  
- 📡 **Nuovi endpoint API**:
  - `GET /api/ha/entities` - Lista tutte le entità con filtro per dominio
  - `GET /api/ha/entity/{id}` - Dettagli entità specifica
  - `GET /api/ha/services` - Lista tutti i servizi disponibili
  - `POST /api/ha/service/call` - Chiamata diretta servizi HA
  - `GET /api/ha/config` - Configurazione sistema Home Assistant
  - `GET /api/ha/context` - Contesto formattato per LLM
  
- 🧠 **Context-aware Chat**:
  - Endpoint `/api/chat` ora supporta parametri per contesto HA
  - `include_entities`: Include stato entità nel prompt
  - `include_services`: Include servizi disponibili nel prompt
  - `entity_domains`: Filtra entità per domini specifici (light, switch, etc.)
  - LLM ora ha visibilità completa dello stato della smart home
  
- 📚 **Documentazione**:
  - Nuovo file `HA_INTEGRATION.md` con guida completa integrazione
  - Esempi API con Python, JavaScript, cURL
  - Documentazione architettura e context injection
  - Script di test `test_ha_integration.py`
  
- ⚙️ **Configurazione**:
  - Porta 5000 esposta per API integrazione HA
  - Flag `hassio_api: true` per accesso Supervisor API
  - Token `SUPERVISOR_TOKEN` automaticamente disponibile

### Modificato
- 📝 README aggiornato con sezione integrazione HA
- 📝 TODO aggiornato con nuove feature implementate e roadmap
- 🔧 `config.yaml` aggiornato alla versione 1.0.4
- 🔧 Descrizione addon evidenzia integrazione HA

### Prossime feature pianificate
- Function calling automatico per esecuzione servizi HA
- Natural language → service execution (es: "turn on lights")
- Webhook support per aggiornamenti real-time
- Entity history analysis
- Automation suggestions basate su pattern

---

## [1.0.3] - 2025-01-14

### Risolto
- 🐛 **Fix crash llama-server**: Rimossi flag non supportati
  - `--log-format`, `--metrics`, `--cont-batching`, `--flash-attn`
  - Server ora avvia correttamente senza crash loop
  
### Modificato
- ⚡ Comando llama-server semplificato in `run.sh`
- 📝 Documentazione aggiornata

---

## [1.0.2] - 2025-01-14

### Risolto
- 🐛 **Fix build Alpine Linux**: Dockerfile riscritto per Alpine
  - Sostituito `apt-get` con `apk` (Alpine package manager)
  - Build statica con `-DGGML_STATIC=ON`
  - Compatibilità con immagini base Home Assistant (Alpine 3.18)
  
### Modificato
- 🏗️ Dockerfile completamente riscritto per Alpine Linux
- 📦 Builder stage usa `alpine:3.18` invece di Ubuntu

---

## [1.0.1] - 2025-01-13

### Risolto
- 🐛 **Fix errore 403**: Commentata riga `image:` in config.yaml
  - Forza build locale da Dockerfile
  - Risolve impossibilità di scaricare immagine da ghcr.io
  
### Modificato
- 🔧 `config.yaml`: Riga `image:` commentata per build locale
- 📝 Documentazione aggiornata con note sul build

---

## [1.0.0] - 2025-01-10

### Aggiunto
- 🎉 Release iniziale dell'addon Llama.cpp per Home Assistant
- ✅ Integrazione completa di llama.cpp in container Docker
- ✅ Build multi-stage ottimizzato per dimensioni ridotte
- ✅ Server API OpenAI-compatible sulla porta 8080
- ✅ Servizio Home Assistant custom sulla porta 5000
- ✅ Supporto per chat singolo tramite `/api/chat`
- ✅ Supporto per conversazioni multi-turno con gestione sessioni
- ✅ Endpoint per avvio, gestione e eliminazione conversazioni
- ✅ Download automatico modelli GGUF da Hugging Face
- ✅ Configurazione tramite config.yaml di Home Assistant
- ✅ Supporto per modelli configurabili dall'utente
- ✅ Parametri configurabili: context size, threads, GPU layers, parallel requests
- ✅ Health check endpoints per monitoring
- ✅ Logging configurabile con livelli debug/info/warning/error
- ✅ Traduzioni italiane e inglesi per l'interfaccia HA
- ✅ Documentazione completa con README dettagliato
- ✅ Test suite completa con dati reali (no mock)
- ✅ Script di esempi Python per integrazione
- ✅ TODO list per roadmap futura
- ✅ License MIT

### Caratteristiche Tecniche
- Docker multi-stage build per ottimizzazione
- Compilazione llama.cpp da sorgente con supporto CUDA opzionale
- Flask API server per servizi Home Assistant
- Requests library per chiamate HTTP
- CORS abilitato per cross-origin requests
- Storage in-memory per sessioni conversazione
- Timeout configurabili per operazioni LLM
- Error handling robusto con messaggi descrittivi
- Validazione input su tutti gli endpoint

### Modelli Supportati
- ✅ Gemma 3 1B (default)
- ✅ Phi-3 Mini
- ✅ LLaMA 3.2 3B
- ✅ LLaMA 3.1 8B
- ✅ Qualsiasi modello GGUF compatibile

### API Endpoints
- `POST /api/chat` - Chat singolo
- `POST /api/conversation/start` - Avvia conversazione
- `POST /api/conversation/<id>/message` - Invia messaggio
- `GET /api/conversation/<id>/history` - Storia conversazione
- `DELETE /api/conversation/<id>` - Elimina conversazione
- `GET /api/conversations` - Lista conversazioni
- `GET /api/health` - Health check
- `GET /api/models` - Info modelli
- `POST /v1/chat/completions` - OpenAI compatible
- `GET /v1/models` - OpenAI models
- `GET /health` - Llama.cpp health

### Documentazione
- README.md con guida completa
- Esempi di utilizzo con Python
- Integrazioni con automazioni Home Assistant
- Guide per configurazione modelli
- Troubleshooting e best practices
- Performance benchmarks

### Test
- Test suite con unittest
- Health checks per server
- Test API chat singolo
- Test conversazioni multi-turno
- Test compatibilità OpenAI
- Test performance e limiti
- Tutti i test con dati reali

## [Unreleased]

### Pianificato per v1.1.0
- [ ] Integrazione nativa con Conversation Agent HA
- [ ] Dashboard Lovelace per UI chat
- [ ] Supporto WebSocket per streaming
- [ ] Cache intelligente risposte
- [ ] Metrics Prometheus
- [ ] Build ARM64 ottimizzata

### Pianificato per v1.2.0
- [ ] Supporto RAG (Retrieval Augmented Generation)
- [ ] Multi-modello con switch dinamico
- [ ] Fine-tuning capabilities
- [ ] Advanced security features

---

## Formato delle Modifiche

### Categorie
- **Aggiunto** - per nuove funzionalità
- **Modificato** - per cambiamenti a funzionalità esistenti
- **Deprecato** - per funzionalità che saranno rimosse
- **Rimosso** - per funzionalità rimosse
- **Corretto** - per bug fix
- **Sicurezza** - per vulnerabilità corrette

### Esempio Entry
```markdown
## [X.Y.Z] - YYYY-MM-DD

### Aggiunto
- Nuova funzionalità XYZ (#123)

### Corretto
- Bug nella funzione ABC (#456)
```

---

Per vedere la differenza tra versioni, usa:
```
git diff v1.0.0..v1.1.0
```
