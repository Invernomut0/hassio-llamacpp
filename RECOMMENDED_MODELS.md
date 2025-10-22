# 🤖 Modelli Raccomandati per Home Assistant

## ⚠️ Dimensione Minima Consigliata

Per utilizzare efficacemente l'integrazione Home Assistant con function calling e comprensione del contesto, si raccomanda un modello con **almeno 3-7 miliardi di parametri**.

## 📊 Modelli Testati e Raccomandati

### ✅ Tier 1: Eccellente (3B+ parametri) - Testati e Verificati

1. **Llama 3.2 3B Instruct** (BEST CHOICE - Testato) ⭐⭐⭐
   ```yaml
   model_url: "https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q4_K_M.gguf"
   model_name: "Llama-3.2-3B-Instruct-Q4_K_M"
   context_size: 4096
   ```
   - Dimensione: ~2.0 GB
   - RAM necessaria: 4 GB
   - **Modello default dell'addon - Testato e funzionante**
   - Eccellente instruction-following
   - Ottima comprensione contesto Home Assistant
   - Multilingua eccellente (IT, EN, ES, FR, DE, etc.)
   - Repository verificato e stabile

2. **Home-Llama-3.2-3B** (HA Specialized - In Testing) 🧪
   ```yaml
   # Nota: Verificare disponibilità su HuggingFace
   model_url: "https://huggingface.co/acon96/home-llm/resolve/main/[verifica-nome-file].gguf"
   model_name: "home-llama-3.2-3b-Q4_K_M"
   context_size: 4096
   ```
   - **Fine-tuned specificamente per Home Assistant**
   - Attualmente in fase di verifica compatibilità GGUF
   - Quando disponibile: comprensione nativa di entità/servizi HA
   - Controllare repository acon96/home-llm per aggiornamenti

3. **Mistral 7B Instruct v0.3** (Testato)
   ```yaml
   model_url: "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.3-GGUF/resolve/main/mistral-7b-instruct-v0.3.Q4_K_M.gguf"
   model_name: "mistral-7b-instruct-v0.3.Q4_K_M"
   context_size: 8192
   ```
   - Dimensione: ~4.4 GB
   - RAM necessaria: 8 GB
   - Eccellente per istruzioni complesse

3. **Phi-3 Medium (14B)**
   ```yaml
   model_url: "https://huggingface.co/microsoft/Phi-3-medium-4k-instruct-gguf/resolve/main/Phi-3-medium-4k-instruct-q4.gguf"
   model_name: "Phi-3-medium-4k-instruct-q4"
   context_size: 4096
   ```
   - Dimensione: ~7.9 GB
   - RAM necessaria: 12 GB
   - Molto intelligente, ottimo per ragionamento

### ⚡ Tier 2: Buono (3-7B parametri)
Funzionano bene ma potrebbero avere qualche limite con prompt molto complessi.

4. **Llama 3.2 1B Instruct** (attuale - SOSTITUIRE)
   - ❌ Troppo piccolo per HA context
   - Sostituire con modello più grande

5. **Gemma 2 2B IT**
   ```yaml
   model_url: "https://huggingface.co/google/gemma-2-2b-it-GGUF/resolve/main/gemma-2-2b-it-Q4_K_M.gguf"
   model_name: "gemma-2-2b-it-Q4_K_M"
   context_size: 2048
   ```
   - Dimensione: ~1.5 GB
   - RAM necessaria: 3 GB
   - Migliore di 1B ma ancora limitato

### 🚀 Tier 3: Avanzato (13B+ parametri)
Per hardware potente, risultati eccezionali.

6. **Llama 3.1 8B Instruct**
   ```yaml
   model_url: "https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
   model_name: "Meta-Llama-3.1-8B-Instruct-Q4_K_M"
   context_size: 8192
   ```
   - Dimensione: ~4.9 GB
   - RAM necessaria: 8 GB
   - Eccellente, context window molto grande

## 🔧 Come Cambiare Modello

### Metodo 1: Via Interfaccia HA (Raccomandato)
1. Vai su **Supervisor → Llama.cpp LLM Server → Configuration**
2. Cambia i parametri:
   - `model_url`: URL del nuovo modello
   - `model_name`: nome del modello
   - `context_size`: dimensione context (minimo 2048, consigliato 4096)
3. **Salva** e **Riavvia addon**

### Metodo 2: Editing config.yaml
```bash
cd /addon_configs/local_llamacpp_llm
nano options.json
```

Modifica:
```json
{
  "model_url": "https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q4_K_M.gguf",
  "model_name": "Llama-3.2-3B-Instruct-Q4_K_M",
  "context_size": 4096,
  ...
}
```

## 💡 Requisiti Hardware

| Modello | RAM Min | Storage | CPU/GPU |
|---------|---------|---------|---------|
| 1-2B | 2-3 GB | 1-2 GB | Solo CPU OK |
| 3B | 4 GB | 2 GB | Solo CPU OK |
| 7B | 6-8 GB | 4-5 GB | CPU (lento) o GPU |
| 13B+ | 12+ GB | 7+ GB | GPU raccomandato |

## 🎯 Raccomandazione Finale

**Per la migliore esperienza con Home Assistant:**

```yaml
model_url: "https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q4_K_M.gguf"
model_name: "Llama-3.2-3B-Instruct-Q4_K_M"
context_size: 4096
threads: 4
gpu_layers: 0  # Aumenta se hai GPU
```

✅ **Modello default testato e funzionante**  
✅ Repository verificato e stabile (bartowski)  
✅ Dimensione gestibile (~2 GB)  
✅ RAM ragionevole (4 GB)  
✅ Eccellente instruction-following  
✅ Ottima comprensione contesto Home Assistant  
✅ Supporto multilingua eccellente  
✅ Context window grande (4096 tokens)

**Nota su Home-Llama:** Quando sarà disponibile una versione GGUF stabile e verificata, 
sarà la scelta ottimale per l'integrazione HA. Nel frattempo, Llama-3.2-3B-Instruct 
offre prestazioni eccellenti.

## 🔍 Test del Modello

Dopo aver cambiato modello, testa con:
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Quali luci sono accese in casa?",
    "include_entities": true
  }'
```

Il modello dovrebbe rispondere con informazioni specifiche sulle tue luci, non con "non ho accesso".
