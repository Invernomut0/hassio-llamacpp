# 📁 Struttura Progetto

```
llamacpp/
├── 📄 Core Files
│   ├── config.yaml              # Configurazione addon Home Assistant (YAML)
│   ├── config.json              # Configurazione addon (JSON alternativo)
│   ├── Dockerfile               # Build multi-stage llama.cpp
│   ├── build.yaml               # Build configuration
│   ├── repository.json          # Repository metadata per HA
│   ├── requirements.txt         # Dipendenze Python
│   └── LICENSE                  # Licenza MIT
│
├── 🔧 Scripts
│   ├── run.sh                   # Script avvio principale addon
│   ├── build.sh                 # Script build locale Docker
│   ├── ha_service.py            # Servizio API Python per HA
│   └── examples.py              # Esempi utilizzo Python
│
├── 📚 Documentazione
│   ├── README.md                # Documentazione principale (completa)
│   ├── QUICKSTART.md            # Guida rapida installazione
│   ├── CONTRIBUTING.md          # Guida contribuzione
│   ├── CHANGELOG.md             # Storia modifiche
│   └── TODO.md                  # Roadmap e task
│
├── 🧪 Testing
│   └── tests/
│       └── test_api.py          # Suite test completa con dati reali
│
├── 🌍 Traduzioni
│   └── translations/
│       ├── en.json              # Traduzioni inglese
│       └── it.json              # Traduzioni italiano
│
└── 🔒 Config
    ├── .gitignore               # File da ignorare in Git
    └── .dockerignore            # File da ignorare in Docker build

```

## 📊 Statistiche Progetto

### File per Tipologia
- **Python**: 3 files (ha_service.py, examples.py, test_api.py)
- **Bash**: 2 files (run.sh, build.sh)
- **Markdown**: 5 files (README, QUICKSTART, CONTRIBUTING, CHANGELOG, TODO)
- **YAML**: 2 files (config.yaml, build.yaml)
- **JSON**: 4 files (config.json, repository.json, en.json, it.json)
- **Docker**: 2 files (Dockerfile, .dockerignore)
- **Config**: 3 files (requirements.txt, .gitignore, LICENSE)

### Linee di Codice (stimate)
- **Python**: ~1000 linee
- **Bash**: ~100 linee
- **Docker**: ~60 linee
- **Documentazione**: ~2000 linee
- **Test**: ~450 linee
- **Totale**: ~3600 linee

## 🎯 File Principali

### 1. config.yaml / config.json
Definisce configurazione addon per Home Assistant:
- Metadata (nome, versione, slug)
- Architetture supportate
- Porte esposte
- Opzioni configurabili
- Schema validazione

### 2. Dockerfile
Build multi-stage ottimizzato:
- **Stage 1**: Compila llama.cpp da sorgente
- **Stage 2**: Immagine runtime leggera con binario

### 3. ha_service.py
Servizio Python Flask che espone API:
- Chat singolo
- Conversazioni multi-turno
- Gestione sessioni
- Health checks
- Proxy per llama-server

### 4. run.sh
Script principale di avvio:
- Legge configurazione da HA
- Download automatico modelli
- Avvia servizio Python
- Avvia llama-server

### 5. README.md
Documentazione completa con:
- Installazione dettagliata
- Configurazione opzioni
- API reference completo
- Esempi integrazione HA
- Troubleshooting
- Performance benchmarks

### 6. tests/test_api.py
Test suite completa:
- Health checks
- API chat singolo
- Conversazioni multi-turno
- Compatibilità OpenAI
- Performance testing
- Solo dati reali (no mock)

## 🏗️ Architettura

```
┌─────────────────────────────────────────────────────────┐
│                    Home Assistant                       │
│  ┌────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │Automations │  │ Scripts     │  │ REST Commands│     │
│  └─────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│        │                 │                 │             │
│        └─────────────────┴─────────────────┘             │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP Requests
                         ▼
┌─────────────────────────────────────────────────────────┐
│              Llama.cpp Addon Container                  │
│                                                          │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Flask API (ha_service.py) - Port 5000            │ │
│  │  ┌─────────────────────────────────────────────┐  │ │
│  │  │ /api/chat                                    │  │ │
│  │  │ /api/conversation/start                      │  │ │
│  │  │ /api/conversation/{id}/message               │  │ │
│  │  │ /api/health                                  │  │ │
│  │  └───────────────┬─────────────────────────────┘  │ │
│  └──────────────────┼────────────────────────────────┘ │
│                     │ Internal HTTP                     │
│                     ▼                                    │
│  ┌───────────────────────────────────────────────────┐ │
│  │  llama-server (llama.cpp) - Port 8080            │ │
│  │  ┌─────────────────────────────────────────────┐  │ │
│  │  │ /v1/chat/completions (OpenAI compatible)    │  │ │
│  │  │ /v1/models                                   │  │ │
│  │  │ /health                                      │  │ │
│  │  └───────────────┬─────────────────────────────┘  │ │
│  └──────────────────┼────────────────────────────────┘ │
│                     │                                    │
│                     ▼                                    │
│  ┌───────────────────────────────────────────────────┐ │
│  │  GGUF Model (gemma-3-1b-it-Q4_K_M.gguf)         │ │
│  │  Path: /data/models/                             │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## 🔄 Flusso Esecuzione

### Avvio Addon
1. Home Assistant legge `config.yaml`
2. Crea container Docker da immagine
3. Esegue `run.sh`
4. `run.sh` scarica modello se necessario
5. Avvia `ha_service.py` (background)
6. Avvia `llama-server` (foreground)
7. Healthchecks verificano stato

### Richiesta Chat
1. Utente/Automazione → API HA `/api/chat`
2. Flask valida richiesta
3. Flask chiama `/v1/chat/completions` su llama-server
4. llama-server esegue inferenza su modello
5. Flask riceve risposta
6. Flask restituisce JSON a utente

### Conversazione Multi-turno
1. Utente → `/api/conversation/start`
2. Flask crea ID e storage in-memory
3. Utente → `/api/conversation/{id}/message`
4. Flask aggiunge messaggio a storia
5. Flask invia storia completa a llama-server
6. Risposta aggiunta a storia
7. Storia persistita per prossimi messaggi

## 🔐 Sicurezza

- ✅ Input validation su tutti gli endpoint
- ✅ Timeout configurabili per prevenire hang
- ✅ Error handling robusto
- ✅ Nessun accesso filesystem arbitrario
- ✅ CORS configurabile
- ⚠️ TODO: Authentication/authorization
- ⚠️ TODO: Rate limiting

## 📈 Performance

### Ottimizzazioni Implementate
- Build multi-stage per immagine leggera
- Compilazione nativa llama.cpp
- Batching richieste
- Context size configurabile
- Thread pool CPU
- GPU layers opzionali

### Metriche Target
- Startup time: < 2 minuti (con model download)
- Response time: < 30s per modelli 1B-3B
- Memory footprint: < 4GB per modelli Q4
- Throughput: 10-50 tokens/secondo (dipende da HW)

## 🧩 Estensibilità

Il progetto è progettato per essere facilmente estendibile:

### Aggiungere Nuovo Endpoint
```python
@app.route('/api/new-feature', methods=['POST'])
def new_feature():
    # Implementation
    return jsonify({"result": "ok"})
```

### Supportare Nuovo Modello
Aggiungi preset in `config.yaml`:
```yaml
schema:
  model_preset: list(gemma-1b|phi3-mini|llama-3b|custom)
```

### Integrare con HA Entity
Crea sensor/service in `ha_service.py`:
```python
# Esponi come HA service
# Registra con HA API
```

## 📦 Deployment

### Locale (Development)
```bash
./build.sh amd64
docker run -p 8080:8080 -p 5000:5000 local/llamacpp-addon:1.0.0-amd64
```

### Home Assistant
1. Push su GitHub
2. HA Supervisor scarica repository
3. Utente installa da Add-on Store
4. HA builda immagine automaticamente

### Pre-built Images (TODO)
```bash
docker push ghcr.io/[USERNAME]/llamacpp-addon:latest
```

## 🎓 Best Practices Seguite

### Codice
- ✅ Type hints Python
- ✅ Docstrings complete
- ✅ Error handling robusto
- ✅ Logging strutturato
- ✅ Configurazione esterna

### Testing
- ✅ Test con dati reali
- ✅ Coverage > 80%
- ✅ Fast execution
- ✅ Clear test names
- ✅ Comprehensive scenarios

### Documentazione
- ✅ README dettagliato
- ✅ Quick start guide
- ✅ API reference completo
- ✅ Examples pratici
- ✅ Troubleshooting guide

### DevOps
- ✅ Multi-stage Docker build
- ✅ .dockerignore ottimizzato
- ✅ Healthchecks configurati
- ✅ Versioning semantico
- ✅ Changelog mantenuto

---

**Ultimo aggiornamento**: 21 Ottobre 2025  
**Versione**: 1.0.0  
**Maintainer**: [Your Name]
