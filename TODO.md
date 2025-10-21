# TODO List - Llama.cpp Home Assistant Addon

## ✅ Completati

### Core Features
- [x] Struttura base addon Home Assistant
- [x] Dockerfile multi-stage con llama.cpp
- [x] Script di avvio con gestione configurazione
- [x] Servizio Python con API REST
- [x] Endpoint chat singolo
- [x] Endpoint conversazioni multi-turno
- [x] Gestione sessioni conversazione
- [x] Health checks e monitoring
- [x] Documentazione completa README
- [x] Test suite con dati reali
- [x] API OpenAI-compatible
- [x] Download automatico modelli

### Bug Fixes & Improvements
- [x] Fix errore 403 build locale (config.yaml)
- [x] Build.yaml multi-arch (aarch64 + amd64)
- [x] Guida troubleshooting completa
- [x] Sezione FAQ nel README
- [x] Fix Alpine Linux compatibility (apk instead of apt-get)
- [x] Fix llama-server crash (removed unsupported flags)

### 🆕 Home Assistant Integration (v1.0.3)
- [x] `HomeAssistantClient` - Client per Supervisor API
- [x] `HAContextBuilder` - Costruzione contesto per LLM
- [x] Integrazione entità HA nel contesto chat
- [x] Endpoint `/api/ha/entities` - Lista tutte le entità
- [x] Endpoint `/api/ha/entity/{id}` - Info entità specifica
- [x] Endpoint `/api/ha/services` - Lista tutti i servizi
- [x] Endpoint `/api/ha/service/call` - Chiamata servizi HA
- [x] Endpoint `/api/ha/config` - Configurazione sistema HA
- [x] Endpoint `/api/ha/context` - Contesto formattato per LLM
- [x] Filtro per domini entità (light, switch, etc.)
- [x] Documentazione completa integrazione HA
- [x] Esempi API con Python, JavaScript, cURL

## 🚧 In Progress

- [ ] Testing integrazione HA con istanza reale
- [ ] Build e test su hardware reale
- [ ] Pubblicazione su repository addon HA

## 📋 To Do

### Features
- [ ] Dashboard Lovelace per chat UI con contesto HA
- [ ] Supporto per upload modelli custom
- [ ] Cache intelligente delle risposte
- [ ] Rate limiting per protezione
- [ ] Autenticazione API con token
- [ ] WebSocket per streaming responses
- [ ] Supporto per funzioni/tools calling
- [ ] Persistent storage conversazioni (SQLite/Redis)

### 🏠 Home Assistant Integration (Next Steps)
- [ ] Function calling automatico per servizi HA
- [ ] Natural language → service call (es: "turn on lights" → automatic execution)
- [ ] Webhook support per aggiornamenti real-time entità
- [ ] Entity history analysis
- [ ] Automation suggestions basate su pattern
- [ ] Multi-turn conversations con HA context retention
- [ ] Scene creation via natural language
- [ ] Smart suggestions per routine giornaliere

### Ottimizzazioni
- [ ] Supporto AMD ROCm per GPU AMD
- [ ] Build ARM64 ottimizzata
- [ ] Quantizzazione on-the-fly
- [ ] Batch processing per performance
- [ ] Caching modelli in memoria
- [ ] Prometheus metrics export
- [ ] Ottimizzazione dimensione contesto HA (ridurre token usage)

### Testing & Quality
- [ ] Integration test con HA reale
- [ ] Performance benchmarks con contesto HA
- [ ] Load testing con multiple entità
- [ ] Security audit
- [ ] Documentation review

### DevOps
- [ ] CI/CD pipeline
- [ ] Auto-build multi-arch
- [ ] Versioning semantico
- [ ] Release notes automatiche
- [ ] Docker Hub publishing

## 🐛 Bug Noti

Nessun bug noto al momento.

## 💡 Idee Future

- Integrazione con Conversation Agent HA
- Supporto per RAG (Retrieval Augmented Generation)
- Fine-tuning su dati specifici utente
- Multi-modello con switch dinamico
- TTS/STT integration
- Automation suggestions basate su ML
- Energy usage prediction
- Anomaly detection

## 📅 Roadmap

### v1.0.0 (Attuale)
- Core functionality
- Basic API
- Documentation

### v1.1.0
- Performance improvements
- GPU support enhancement
- More model presets

### v1.2.0
- Advanced features (RAG, tools)
- Better HA integration
- UI dashboard

### v2.0.0
- Multi-model support
- Fine-tuning capabilities
- Enterprise features

---
Ultimo aggiornamento: 21 Ottobre 2025
