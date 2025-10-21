# 🚨 Quick Fix Reference

Guida rapida ai problemi più comuni e relative soluzioni immediate.

## 🔴 Errore 403 durante installazione

**Errore**: `Can't install ghcr.io/home-assistant/.../aarch64-addon-llamacpp: 403 Forbidden`

**Fix immediato**:
```yaml
# In config.yaml, commenta questa riga:
# image: "ghcr.io/home-assistant/{arch}-addon-llamacpp"
```

**Causa**: L'addon cerca un'immagine precompilata che non esiste. Home Assistant deve costruirla localmente.

**Tempo build**: 15-45 minuti la prima volta.

---

## 🔴 Errore "apt-get: not found" durante build

**Errore**: `/bin/ash: apt-get: not found` durante build Docker

**Fix**: ✅ **RISOLTO nella v1.0.2+**

Il Dockerfile ora usa Alpine Linux (apk) invece di Ubuntu (apt-get), compatibile con le immagini base di Home Assistant.

**Se usi versione vecchia**: Aggiorna a v1.0.2 o successiva.

---

## 🔴 Build troppo lenta o timeout

**Fix immediato**:
1. Chiudi tutti gli addon non essenziali
2. Verifica spazio disco: `df -h` (serve 5+ GB liberi)
3. Monitora i log in tempo reale per vedere il progresso
4. Sii paziente: la compilazione di llama.cpp è lenta!

**Hardware minimo**: 2 CPU cores, 4 GB RAM, 10 GB disco

---

## 🔴 Modello non si scarica

**Fix immediato**:
```yaml
# Usa un modello più piccolo e veloce
model_url: "https://huggingface.co/ggml-org/gemma-3-1b-it-GGUF/resolve/main/gemma-3-1b-it-Q4_K_M.gguf"
model_name: "gemma-3-1b-it-Q4_K_M"
```

**Test connettività**:
```bash
ping huggingface.co
```

---

## 🔴 Out of Memory (OOM)

**Fix immediato**:
```yaml
context_size: 512          # Riduci da 2048
parallel_requests: 1       # Una richiesta alla volta
model_name: "gemma-1b"     # Usa modello più piccolo
```

**RAM necessaria** per modello:
- 1B Q4: ~1.5 GB
- 3B Q4: ~2.5 GB
- 7B Q4: ~5 GB

---

## 🔴 Risposte troppo lente

**Fix immediato**:
```yaml
threads: 8              # Aumenta (numero CPU cores)
context_size: 1024      # Riduci se possibile
gpu_layers: 35          # Se hai GPU NVIDIA
```

**Target performance**: 5-15 token/sec su CPU moderna

---

## 🔴 Connection refused (porta 8080)

**Fix immediato**:
```yaml
# Cambia porta in config.yaml
ports:
  8081/tcp: 8081
```

**Test**:
```bash
curl http://homeassistant.local:8080/health
```

---

## 🔴 Addon crasha continuamente

**Checklist rapida**:
1. ✅ RAM sufficiente? (4+ GB raccomandati)
2. ✅ Modello scaricato correttamente? (controlla `/data/models`)
3. ✅ Log level su `debug` per vedere errori dettagliati
4. ✅ Prova modello più piccolo (1B-2B)

**Restart addon**:
```
Supervisor → Llama.cpp → Restart
```

---

## 🔴 Qualità output scarsa

**Fix immediato**:
```yaml
# Usa modello instruction-tuned
model_url: "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf"
model_name: "phi-3-mini-q4"

# Evita quantizzazioni aggressive
# ✅ Q4_K_M (raccomandato)
# ❌ Q2_K (troppo aggressivo)
```

**Migliori modelli per qualità**:
1. Phi-3 Mini (ottimo rapporto)
2. Gemma 3 3B (veloce e accurato)
3. Llama 3.2 3B (versatile)

---

## 🔴 GPU non rilevata

**Verifica**:
```bash
nvidia-smi  # Deve mostrare la GPU
```

**Se non funziona**: usa CPU-only ottimizzato
```yaml
gpu_layers: 0
threads: 16  # Massimizza CPU usage
```

**Nota**: Il Dockerfile di default è CPU-only. Per GPU serve ricompilare con `-DGGML_CUDA=ON`.

---

## 📞 Serve aiuto?

1. **Log completi**: Supervisor → Addon → Logs (copia tutto)
2. **Configurazione**: Copia il tuo `config.yaml`
3. **Hardware**: CPU, RAM, GPU, Home Assistant OS version
4. **Apri issue**: [GitHub Issues](https://github.com/Invernomut0/hassio-llamacpp/issues)

Per problemi dettagliati: vedi [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Quick Reference Card** - Stampa o salva questa pagina per riferimento veloce!
