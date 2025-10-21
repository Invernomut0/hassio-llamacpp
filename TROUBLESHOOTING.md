# 🔧 Guida al Troubleshooting - Llama.cpp Addon

## Problemi di Installazione

### ❌ Errore 403: "denied" su ghcr.io

**Messaggio di errore completo**:
```
Can't install ghcr.io/home-assistant/aarch64-addon-llamacpp:1.0.0: 
403 Client Error for http+docker://localhost/v1.51/images/create?tag=1.0.0&
fromImage=ghcr.io%2Fhome-assistant%2Faarch64-addon-llamacpp&platform=linux%2Farm64: 
Forbidden ("Head "https://ghcr.io/v2/home-assistant/aarch64-addon-llamacpp/manifests/1.0.0": denied")
```

**Causa**:
L'addon sta tentando di scaricare un'immagine Docker precompilata da GitHub Container Registry (ghcr.io) che non esiste o non è accessibile pubblicamente.

**Soluzione**:

1. **Verifica il file `config.yaml`**:
   - La riga `image: "ghcr.io/home-assistant/{arch}-addon-llamacpp"` deve essere commentata
   - Home Assistant costruirà l'immagine localmente dal `Dockerfile`

2. **Rimuovi e reinstalla l'addon**:
   ```bash
   # Dal Supervisor di Home Assistant:
   # 1. Disinstalla l'addon se presente
   # 2. Rimuovi il repository
   # 3. Aggiungi nuovamente il repository
   # 4. Installa l'addon
   ```

3. **Aspetta il completamento della build**:
   - La prima build può richiedere 15-45 minuti
   - Monitora i log in tempo reale per vedere il progresso
   - Vedrai messaggi come "Building llama.cpp", "Compiling sources", ecc.

**Build locale vs Immagine precompilata**:
- **Locale**: Home Assistant compila dal Dockerfile (più lento, ma sempre funzionante)
- **Precompilata**: Scarica un'immagine già pronta (veloce, ma richiede pubblicazione su registry)

### ❌ Build timeout o bloccata

**Sintomi**:
- Installazione che sembra ferma per oltre 1 ora
- Nessun log nuovo dopo molti minuti
- Errore "timeout" durante l'installazione

**Causa**:
La compilazione di llama.cpp è intensiva e può essere lenta su hardware limitato.

**Soluzioni**:

1. **Aumenta le risorse**:
   - Chiudi altri addon pesanti (es. database, Node-RED)
   - Libera almeno 2 GB di RAM
   - Assicurati di avere 5+ GB di spazio disco libero

2. **Controlla i log in tempo reale**:
   ```bash
   # Supervisor → Llama.cpp Addon → Logs → Refresh
   ```

3. **Considera un'installazione con immagine precompilata**:
   - Per utenti che vogliono evitare la build locale
   - Richiede pubblicazione su Docker Hub o GHCR
   - Vedi sezione "Deployment" nel README

4. **Hardware minimo raccomandato**:
   - 2+ CPU cores
   - 4 GB RAM
   - 10 GB spazio disco
   - Connessione internet stabile

---

## Problemi di Download Modelli

### ❌ Modello non si scarica

**Sintomi**:
- Addon avviato ma modello bloccato al download
- Log mostra "Downloading model..." ma nessun progresso
- Errore "Failed to download model"

**Causa**:
Problemi di rete, URL errato, o modello troppo grande.

**Soluzioni**:

1. **Verifica la connettività**:
   ```bash
   # Dal terminale SSH di Home Assistant:
   ping -c 3 huggingface.co
   curl -I https://huggingface.co
   ```

2. **Testa l'URL del modello**:
   - Apri l'URL del modello nel browser
   - Verifica che il file sia accessibile
   - Controlla che non ci siano errori 404 o 403

3. **Modelli alternativi testati**:
   ```yaml
   # Gemma 3 1B (leggero, veloce)
   model_url: "https://huggingface.co/ggml-org/gemma-3-1b-it-GGUF/resolve/main/gemma-3-1b-it-Q4_K_M.gguf"
   
   # Phi-3 Mini (ottimo rapporto qualità/dimensione)
   model_url: "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf"
   
   # Llama 3.2 1B (ultra-leggero)
   model_url: "https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF/resolve/main/Llama-3.2-1B-Instruct-Q4_K_M.gguf"
   ```

4. **Download manuale** (workaround):
   ```bash
   # SSH in Home Assistant
   docker exec -it addon_xxx_llamacpp_llm bash
   cd /data/models
   wget -O model.gguf "URL_DEL_MODELLO"
   ```

### ❌ Spazio disco insufficiente

**Sintomi**:
- Download del modello fallisce al 90%+
- Errore "No space left on device"

**Soluzioni**:

1. **Verifica lo spazio disponibile**:
   ```bash
   df -h
   ```

2. **Libera spazio**:
   - Rimuovi backup vecchi
   - Elimina addon non utilizzati
   - Pulisci la cache Docker: `docker system prune -a`

3. **Usa modelli più piccoli**:
   - 1B-2B modelli: ~1-2 GB
   - 3B modelli: ~2-3 GB
   - 7B-8B modelli: ~4-5 GB

---

## Problemi di Performance

### ❌ Risposte molto lente (>60 secondi)

**Sintomi**:
- Ogni richiesta impiega minuti per rispondere
- Token generation rate < 1 token/secondo

**Cause e soluzioni**:

1. **Troppi pochi thread**:
   ```yaml
   threads: 8  # Aumenta a 8-16 su sistemi multicore
   ```

2. **Context size troppo grande**:
   ```yaml
   context_size: 1024  # Riduci da 2048 se non hai bisogno di conversazioni lunghe
   ```

3. **Modello troppo grande per la RAM**:
   - Usa Q4_K_M invece di Q8 o F16
   - Prova modelli più piccoli (2B invece di 7B)

4. **GPU non utilizzata** (se disponibile):
   ```yaml
   gpu_layers: 35  # Carica più layer su GPU
   ```

5. **Verifica risorse**:
   ```bash
   # Supervisor → System → Monitor
   # Controlla CPU e RAM usage durante le richieste
   ```

### ❌ Out of Memory (OOM) / Crash

**Sintomi**:
- Addon crasha improvvisamente
- Log mostra "Out of memory" o "Killed"
- Sistema Home Assistant rallenta

**Soluzioni**:

1. **Riduci l'utilizzo di memoria**:
   ```yaml
   context_size: 512       # Dimezza il contesto
   parallel_requests: 1    # Una richiesta alla volta
   gpu_layers: 0           # Se GPU ha poca VRAM
   ```

2. **Usa modelli quantizzati aggressivamente**:
   - Q4_K_M: ~4 bit per parametro (raccomandato)
   - Q3_K_M: ~3 bit (compromesso qualità/dimensione)
   - Q2_K: ~2 bit (estremo, qualità ridotta)

3. **Chiudi addon non essenziali**:
   - Studio Code Server
   - Grafana
   - Database pesanti

4. **Calcola memoria necessaria**:
   ```
   RAM richiesta = (Parametri modello × Bit quantizzazione) / 8 + Context overhead
   
   Esempio per modello 3B Q4_K_M:
   RAM = (3B × 4) / 8 + 1GB = ~2.5 GB
   ```

### ❌ GPU non rilevata

**Sintomi**:
- `gpu_layers > 0` ma GPU non viene usata
- Performance uguali a CPU-only

**Soluzioni**:

1. **Verifica supporto NVIDIA**:
   ```bash
   nvidia-smi  # Deve mostrare la GPU
   ```

2. **Ricompila con CUDA** (richiede modifica Dockerfile):
   ```dockerfile
   RUN cmake -B build \
       -DGGML_CUDA=ON \
       -DCMAKE_CUDA_ARCHITECTURES=native \
       && cmake --build build --config Release
   ```

3. **GPU supportate**:
   - NVIDIA con compute capability 6.0+ (Pascal e successivi)
   - CUDA 11.7+ installato
   - Driver NVIDIA aggiornati

4. **Alternativa: CPU-only ottimizzato**:
   - Aumenta `threads`
   - Usa quantizzazione Q4_K_M
   - Riduci `context_size`

---

## Problemi di Rete/API

### ❌ Errore 502/503 dall'API

**Sintomi**:
- Chiamate API restituiscono errori 502 o 503
- Health check fallisce

**Soluzioni**:

1. **Verifica che l'addon sia in esecuzione**:
   ```bash
   # Supervisor → Llama.cpp Addon → Info
   # Stato deve essere "Started"
   ```

2. **Testa l'health endpoint**:
   ```bash
   curl http://homeassistant.local:8080/health
   # Dovrebbe rispondere: {"status": "ok", ...}
   ```

3. **Controlla i log per errori**:
   ```bash
   # Log deve mostrare:
   # "llama-server listening on 0.0.0.0:8080"
   ```

4. **Riavvia l'addon**:
   - Supervisor → Llama.cpp → Restart

### ❌ Connection refused

**Sintomi**:
- `curl: (7) Failed to connect to localhost port 8080: Connection refused`
- Non riesci a connetterti all'API

**Cause**:

1. **Porta occupata**:
   ```bash
   # Cambia porta in config.yaml
   ports:
     8081/tcp: 8081  # Usa porta diversa
   ```

2. **Firewall**:
   - Verifica regole firewall di Home Assistant
   - Assicurati che la porta sia accessibile

3. **Network mode errato**:
   ```yaml
   # In config.yaml
   host_network: false  # Deve essere false per sicurezza
   ```

---

## Problemi di Qualità Output

### ❌ Risposte incoerenti o di bassa qualità

**Cause**:
- Modello troppo piccolo per la task
- Quantizzazione troppo aggressiva
- Context size insufficiente

**Soluzioni**:

1. **Usa modelli più grandi**:
   - 1B → 3B → 7B (se RAM sufficiente)
   - Istruzioni specifiche: modelli `-instruct` o `-it`

2. **Migliora la quantizzazione**:
   - Q2_K → Q4_K_M → Q5_K_M → Q8_0
   - Q4_K_M è il miglior compromesso

3. **Aumenta il contesto**:
   ```yaml
   context_size: 4096  # Per conversazioni più complesse
   ```

4. **Ottimizza i prompt**:
   - Sii specifico e dettagliato
   - Fornisci esempi
   - Usa system messages appropriati

### ❌ Modello ripete o va in loop

**Sintomi**:
- Output contiene ripetizioni infinite
- Modello non conclude la risposta

**Soluzioni**:

1. **Parametri di sampling**:
   ```python
   # Nell'API call
   {
     "temperature": 0.7,
     "top_p": 0.9,
     "repeat_penalty": 1.1,
     "top_k": 40
   }
   ```

2. **Limita lunghezza output**:
   ```python
   {"max_tokens": 256}
   ```

3. **Cambia modello**:
   - Alcuni modelli sono più stabili di altri
   - Testa Phi-3 o Gemma per stabilità

---

## Debug Avanzato

### Abilitare log dettagliati

```yaml
# config.yaml
log_level: "debug"
```

### Accedere al container

```bash
# SSH in Home Assistant
docker ps | grep llamacpp
docker exec -it addon_xxx_llamacpp_llm bash

# Verifica configurazione
ls -lh /data/models
cat /config/options.json
ps aux | grep llama-server
```

### Testare llama-server manualmente

```bash
# Dentro il container
/usr/local/bin/llama-server \
  --model /data/models/model.gguf \
  --host 0.0.0.0 \
  --port 8080 \
  --ctx-size 2048 \
  --verbose
```

### Analizzare performance

```bash
# Test velocità token generation
curl -X POST http://localhost:8080/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Ciao, come stai?",
    "max_tokens": 50,
    "stream": false
  }'
```

---

## Supporto

Se i problemi persistono:

1. **Raccogli informazioni**:
   - Log completi dell'addon
   - Configurazione utilizzata (`config.yaml`)
   - Sistema operativo e versione Home Assistant
   - Hardware (CPU, RAM, GPU)

2. **Apri un issue su GitHub**:
   - [https://github.com/Invernomut0/hassio-llamacpp/issues](https://github.com/Invernomut0/hassio-llamacpp/issues)
   - Includi tutti i dettagli sopra

3. **Community**:
   - Forum Home Assistant
   - Discord llama.cpp

---

**Ultima aggiornamento**: 21 Ottobre 2025
