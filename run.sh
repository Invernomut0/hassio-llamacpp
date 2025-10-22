#!/usr/bin/with-contenv bashio

set -e

bashio::log.info "Avvio addon Llama.cpp LLM Server..."

# Leggi configurazione da Home Assistant
MODEL_URL=$(bashio::config 'model_url')
MODEL_NAME=$(bashio::config 'model_name')
CONTEXT_SIZE=$(bashio::config 'context_size')
THREADS=$(bashio::config 'threads')
GPU_LAYERS=$(bashio::config 'gpu_layers')
PARALLEL=$(bashio::config 'parallel_requests')
LOG_LEVEL=$(bashio::config 'log_level')

MODEL_PATH="/data/models/${MODEL_NAME}.gguf"

# Download del modello se non esiste
if [ ! -f "$MODEL_PATH" ]; then
    bashio::log.info "Download modello da ${MODEL_URL}..."
    mkdir -p /data/models
    curl -L -o "$MODEL_PATH" "$MODEL_URL"
    bashio::log.info "Download completato: ${MODEL_PATH}"
else
    bashio::log.info "Modello già presente: ${MODEL_PATH}"
fi

# Verifica che il modello esista
if [ ! -f "$MODEL_PATH" ]; then
    bashio::log.error "Modello non trovato: ${MODEL_PATH}"
    exit 1
fi

# Avvia il servizio Home Assistant in background
bashio::log.info "Avvio servizio Home Assistant API..."
python3 /ha_service.py 2>&1 | sed 's/^/[HA-SERVICE] /' &
HA_SERVICE_PID=$!
bashio::log.info "Servizio HA avviato con PID: ${HA_SERVICE_PID}"

# Aspetta che il servizio sia pronto
sleep 2

# Avvia llama-server con configurazione
bashio::log.info "Avvio llama-server..."
bashio::log.info "Modello: ${MODEL_PATH}"
bashio::log.info "Context size: ${CONTEXT_SIZE}, Threads: ${THREADS}, GPU layers: ${GPU_LAYERS}"
bashio::log.info "Function calling/tools support: enabled (--jinja)"

exec llama-server \
    --model "$MODEL_PATH" \
    --ctx-size "$CONTEXT_SIZE" \
    --threads "$THREADS" \
    --n-gpu-layers "$GPU_LAYERS" \
    --parallel "$PARALLEL" \
    --host 0.0.0.0 \
    --port 8080 \
    --jinja
    --jinja
