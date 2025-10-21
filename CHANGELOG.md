# Changelog

Tutte le modifiche significative a questo progetto saranno documentate in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/it/1.0.0/),
e questo progetto aderisce al [Semantic Versioning](https://semver.org/lang/it/).

## [1.0.0] - 2025-10-21

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
