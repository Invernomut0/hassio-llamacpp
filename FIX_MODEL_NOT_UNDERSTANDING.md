# 🔧 FIX: Model Non Capisce il Contesto Home Assistant

## 🚨 Problema

Il modello risponde con "Come modello linguistico, non ho accesso a informazioni personali" quando chiedi informazioni sulle tue entità Home Assistant (luci, switch, sensori, etc.).

## 🎯 Causa Radice

**I modelli piccoli (<3B parametri) non hanno capacità sufficienti per:**
1. Seguire istruzioni complesse nel system prompt
2. Interpretare correttamente il contesto HA fornito
3. Ragionare su stati delle entità
4. Applicare le istruzioni a dati strutturati

**Modelli come Gemma 3 1B (1 miliardo di parametri) sono troppo limitati per questo task.**

## ✅ Soluzioni

### Soluzione 1: Usare un Modello Più Grande (RACCOMANDATO)

#### Modello Consigliato: Home-Llama-3.2-3B (Specializzato HA) ⭐

Questo modello è **specificamente fine-tuned per Home Assistant** - è la scelta perfetta!

1. **Apri Home Assistant**
2. **Vai su: Supervisor → Llama.cpp LLM Server → Configuration**
3. **Modifica questi parametri:**

```yaml
model_url: https://huggingface.co/acon96/Home-Llama-3.2-3B-GGUF/resolve/main/home-llama-3.2-3b-Q4_K_M.gguf
model_name: home-llama-3.2-3b-Q4_K_M
context_size: 4096
```

4. **Salva e Riavvia l'addon**
5. **Attendi il download del nuovo modello (~2 GB)**

#### Requisiti Hardware
- RAM: minimo 4 GB
- Storage: 2 GB liberi
- CPU: Qualsiasi (GPU opzionale ma consigliata)

#### Perché Home-Llama-3.2-3B?
✅ **Addestrato specificamente per Home Assistant** 🎯  
✅ 3 miliardi di parametri (3x più intelligente di Gemma 1B)  
✅ Comprensione nativa di entità, servizi, automazioni HA  
✅ Ottima comprensione del contesto  
✅ Seguire istruzioni complesse  
✅ Multilingua eccellente (IT, EN, ES, FR, DE, etc.)  
✅ Dimensione ragionevole (~2 GB)  
✅ Context window grande (4096 tokens)  

### Soluzione 2: Modalità Prompt Semplificato (Per Gemma 1B)

Se **non puoi usare un modello più grande**, ho aggiunto una modalità prompt ultra-semplificata:

1. **Apri Configuration dell'addon**
2. **Aggiungi questa opzione:**

```yaml
simple_prompt_mode: true
```

3. **Salva e Riavvia**

Questa modalità:
- Rimuove istruzioni complesse
- Usa un prompt minimalista
- Aumenta le probabilità che il modello capisca

⚠️ **Nota**: Anche con prompt semplificato, Gemma 1B potrebbe non funzionare bene.

### Soluzione 3: Modelli Alternativi

Se Llama 3.2 3B non funziona sul tuo hardware:

#### Opzione A: Mistral 7B (migliore qualità, più RAM)
```yaml
model_url: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.3-GGUF/resolve/main/mistral-7b-instruct-v0.3.Q4_K_M.gguf
model_name: mistral-7b-instruct-v0.3.Q4_K_M
context_size: 8192
```
- Dimensione: ~4.4 GB
- RAM necessaria: 8 GB
- Eccellente per istruzioni complesse

#### Opzione B: Gemma 2 2B (compromesso)
```yaml
model_url: https://huggingface.co/google/gemma-2-2b-it-GGUF/resolve/main/gemma-2-2b-it-Q4_K_M.gguf
model_name: gemma-2-2b-it-Q4_K_M
context_size: 2048
```
- Dimensione: ~1.5 GB
- RAM necessaria: 3 GB
- Migliore di 1B ma ancora limitato

## 📊 Confronto Modelli

| Modello | Parametri | RAM | Storage | Qualità HA | Velocità |
|---------|-----------|-----|---------|------------|----------|
| **Gemma 3 1B** | 1B | 2 GB | 1 GB | ❌ Scarsa | ⚡⚡⚡ Veloce |
| **Gemma 2 2B** | 2B | 3 GB | 1.5 GB | ⚠️ Limitata | ⚡⚡ Buona |
| **Llama 3.2 3B** ⭐ | 3B | 4 GB | 2 GB | ✅ Ottima | ⚡⚡ Buona |
| **Mistral 7B** | 7B | 8 GB | 4.4 GB | ✅✅ Eccellente | ⚡ Media |
| **Phi-3 14B** | 14B | 12 GB | 7.9 GB | ✅✅✅ Superiore | 🐌 Lenta |

## 🧪 Test

Dopo aver cambiato modello, testa con:

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Quali luci sono accese in casa?",
    "include_entities": true
  }'
```

**Risposta attesa:**
```json
{
  "response": "In base allo stato attuale della casa, le seguenti luci sono accese: [lista luci con stato 'on']",
  "usage": {...}
}
```

**Risposta ERRATA (modello troppo piccolo):**
```json
{
  "response": "Come modello linguistico, non ho accesso a informazioni personali...",
  "usage": {...}
}
```

## 📝 Note Tecniche

### Perché i modelli piccoli falliscono?

1. **Context Window Limitato**: 2048 tokens potrebbero non bastare per system prompt + entità HA + conversazione
2. **Capacità di Reasoning Limitata**: <3B parametri non bastano per "ragionare" su stati delle entità
3. **Instruction-Following Debole**: Non seguono fedelmente le istruzioni nel system prompt
4. **Overflow del Context**: Se troppe entità, il context "satura" e il modello perde le istruzioni iniziali

### Perché Llama 3.2 3B Funziona?

1. **3B parametri**: Capacità cognitive sufficienti per task complessi
2. **4096 tokens context**: Spazio per system prompt + molte entità + conversazione
3. **Training avanzato**: Ottimizzato per instruction-following
4. **Multilingua nativo**: Supporto eccellente per italiano
5. **Architettura moderna**: Llama 3.x è state-of-the-art

## 🔍 Debug

Se anche con Llama 3.2 3B non funziona:

1. **Verifica le entità HA siano accessibili:**
```bash
curl http://localhost:5000/api/ha/entities
```

2. **Verifica il prompt contenga le entità:**
```bash
curl http://localhost:5000/api/debug/prompt
```

3. **Controlla i log dell'addon:**
```bash
docker logs addon_local_llamacpp_llm
```

4. **Verifica SUPERVISOR_TOKEN:**
```bash
echo $SUPERVISOR_TOKEN
```

## 📚 Riferimenti

- **Lista Completa Modelli**: Vedi `RECOMMENDED_MODELS.md`
- **Guida Debug**: Vedi `DEBUG_CONTEXT.md`
- **Configurazione Avanzata**: Vedi `README.md`

## ✨ Raccomandazione Finale

**Passa a Llama 3.2 3B Instruct** - È il miglior compromesso tra:
- Qualità delle risposte
- Uso RAM/Storage
- Velocità di risposta
- Supporto multilingua

Con questo modello, l'integrazione Home Assistant funzionerà perfettamente! 🎉
