# TODO List - Llama.cpp Home Assistant Addon

## ✅ Completati

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
- [x] Fix errore 403 build locale (config.yaml)
- [x] Build.yaml multi-arch (aarch64 + amd64)
- [x] Guida troubleshooting completa
- [x] Sezione FAQ nel README

## 🚧 In Progress

- [ ] Build e test su hardware reale
- [ ] Pubblicazione su repository addon HA

## 📋 To Do

### Features
- [ ] Integrazione con servizi HA nativi
- [ ] Dashboard Lovelace per chat UI
- [ ] Supporto per upload modelli custom
- [ ] Cache intelligente delle risposte
- [ ] Rate limiting per protezione
- [ ] Autenticazione API con token
- [ ] WebSocket per streaming responses
- [ ] Supporto per funzioni/tools calling

### Ottimizzazioni
- [ ] Supporto AMD ROCm per GPU AMD
- [ ] Build ARM64 ottimizzata
- [ ] Quantizzazione on-the-fly
- [ ] Batch processing per performance
- [ ] Caching modelli in memoria
- [ ] Prometheus metrics export

### Testing & Quality
- [ ] Integration test con HA
- [ ] Performance benchmarks
- [ ] Load testing
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
