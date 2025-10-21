# 🚨 Quick Fix Reference

Quick guide to the most common problems and immediate solutions.

## 🔴 403 Error during installation

**Error**: `Can't install ghcr.io/home-assistant/.../aarch64-addon-llamacpp: 403 Forbidden`

**Immediate fix**:
```yaml
# In config.yaml, comment out this line:
# image: "ghcr.io/home-assistant/{arch}-addon-llamacpp"
```

**Cause**: The addon is looking for a prebuilt image that doesn't exist. Home Assistant must build it locally.

**Build time**: 15-45 minutes the first time.

---

## 🔴 "apt-get: not found" error during build

**Error**: `/bin/ash: apt-get: not found` during Docker build

**Fix**: ✅ **FIXED in v1.0.2+**

The Dockerfile now uses Alpine Linux (apk) instead of Ubuntu (apt-get), compatible with Home Assistant base images.

**If using old version**: Update to v1.0.2 or later.

---

## 🔴 Build too slow or timeout

**Immediate fix**:
1. Close all non-essential addons
2. Check disk space: `df -h` (needs 5+ GB free)
3. Monitor logs in real-time to see progress
4. Be patient: llama.cpp compilation is slow!

**Minimum hardware**: 2 CPU cores, 4 GB RAM, 10 GB disk

---

## 🔴 Model not downloading

**Immediate fix**:
```yaml
# Use a smaller and faster model
model_url: "https://huggingface.co/ggml-org/gemma-3-1b-it-GGUF/resolve/main/gemma-3-1b-it-Q4_K_M.gguf"
model_name: "gemma-3-1b-it-Q4_K_M"
```

**Test connectivity**:
```bash
ping huggingface.co
```

---

## 🔴 Out of Memory (OOM)

**Immediate fix**:
```yaml
context_size: 512          # Reduce from 2048
parallel_requests: 1       # One request at a time
model_name: "gemma-1b"     # Use smaller model
```

**RAM required** per model:
- 1B Q4: ~1.5 GB
- 3B Q4: ~2.5 GB
- 7B Q4: ~5 GB

---

## 🔴 Responses too slow

**Immediate fix**:
```yaml
threads: 8              # Increase (number of CPU cores)
context_size: 1024      # Reduce if possible
gpu_layers: 35          # If you have NVIDIA GPU
```

**Target performance**: 5-15 tokens/sec on modern CPU

---

## 🔴 Connection refused (port 8080)

**Immediate fix**:
```yaml
# Change port in config.yaml
ports:
  8081/tcp: 8081
```

**Test**:
```bash
curl http://homeassistant.local:8080/health
```

---

## 🔴 Addon crashes continuously

**Quick checklist**:
1. ✅ Sufficient RAM? (4+ GB recommended)
2. ✅ Model downloaded correctly? (check `/data/models`)
3. ✅ Log level on `debug` to see detailed errors
4. ✅ Try smaller model (1B-2B)

**Restart addon**:
```
Supervisor → Llama.cpp → Restart
```

---

## 🔴 Poor output quality

**Immediate fix**:
```yaml
# Use instruction-tuned model
model_url: "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf"
model_name: "phi-3-mini-q4"

# Avoid aggressive quantization
# ✅ Q4_K_M (recommended)
# ❌ Q2_K (too aggressive)
```

**Best models for quality**:
1. Phi-3 Mini (excellent ratio)
2. Gemma 3 3B (fast and accurate)
3. Llama 3.2 3B (versatile)

---

## 🔴 GPU not detected

**Verify**:
```bash
nvidia-smi  # Must show the GPU
```

**If it doesn't work**: use CPU-only optimized
```yaml
gpu_layers: 0
threads: 16  # Maximize CPU usage
```

**Note**: Default Dockerfile is CPU-only. For GPU you need to recompile with `-DGGML_CUDA=ON`.

---

## 📞 Need help?

1. **Complete logs**: Supervisor → Addon → Logs (copy all)
2. **Configuration**: Copy your `config.yaml`
3. **Hardware**: CPU, RAM, GPU, Home Assistant OS version
4. **Open issue**: [GitHub Issues](https://github.com/Invernomut0/hassio-llamacpp/issues)

For detailed problems: see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Quick Reference Card** - Print or save this page for quick reference!
