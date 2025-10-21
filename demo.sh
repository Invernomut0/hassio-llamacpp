#!/bin/bash
# Quick Demo Script - Testa l'addon localmente

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Llama.cpp Home Assistant Addon - Demo Script           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check requirements
echo "→ Verifico requisiti..."

if ! command -v docker &> /dev/null; then
    echo "✗ Docker non trovato. Installalo prima di continuare."
    exit 1
fi

if ! command -v curl &> /dev/null; then
    echo "✗ curl non trovato. Installalo prima di continuare."
    exit 1
fi

echo "✓ Docker trovato"
echo "✓ curl trovato"
echo ""

# Build
echo "→ Build immagine Docker..."
echo "  (Questo può richiedere 10-15 minuti la prima volta)"
echo ""

./build.sh amd64

if [ $? -ne 0 ]; then
    echo "✗ Build fallita"
    exit 1
fi

echo ""
echo "✓ Build completata!"
echo ""

# Run
echo "→ Avvio container..."
echo ""

docker run -d \
    --name llamacpp-addon-demo \
    -p 8080:8080 \
    -p 5000:5000 \
    -e MODEL_URL="https://huggingface.co/ggml-org/gemma-3-1b-it-GGUF/resolve/main/gemma-3-1b-it-Q4_K_M.gguf" \
    -e MODEL_NAME="gemma-3-1b-it-Q4_K_M" \
    -e CONTEXT_SIZE="2048" \
    -e THREADS="4" \
    local/llamacpp-addon:1.0.0-amd64

if [ $? -ne 0 ]; then
    echo "✗ Avvio container fallito"
    exit 1
fi

echo "✓ Container avviato!"
echo ""

# Wait for startup
echo "→ Attendo avvio servizi..."
echo "  (Download modello + inizializzazione, ~2-3 minuti)"
echo ""

for i in {1..60}; do
    if curl -s http://localhost:5000/api/health > /dev/null 2>&1; then
        echo "✓ Servizi pronti!"
        break
    fi
    
    if [ $i -eq 60 ]; then
        echo "✗ Timeout: servizi non pronti dopo 60 secondi"
        echo "  Controlla i log: docker logs llamacpp-addon-demo"
        exit 1
    fi
    
    echo -n "."
    sleep 2
done

echo ""
echo ""

# Test API
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    TEST API                               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "→ Test 1: Health Check"
curl -s http://localhost:5000/api/health | python3 -m json.tool
echo ""
echo ""

echo "→ Test 2: Chat Singolo"
echo "  Domanda: 'Ciao! Rispondi con una sola parola.'"
curl -s -X POST http://localhost:5000/api/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "Ciao! Rispondi con una sola parola.", "max_tokens": 20}' \
    | python3 -m json.tool
echo ""
echo ""

echo "→ Test 3: Avvia Conversazione"
CONV_ID=$(curl -s -X POST http://localhost:5000/api/conversation/start \
    -H "Content-Type: application/json" \
    -d '{"system_prompt": "Sei un assistente conciso."}' \
    | python3 -c "import sys, json; print(json.load(sys.stdin)['conversation_id'])")

echo "  Conversazione ID: $CONV_ID"
echo ""

echo "→ Test 4: Messaggio in Conversazione"
echo "  Domanda: 'Che ore sono?'"
curl -s -X POST "http://localhost:5000/api/conversation/$CONV_ID/message" \
    -H "Content-Type: application/json" \
    -d '{"message": "Che ore sono?", "max_tokens": 50}' \
    | python3 -m json.tool
echo ""
echo ""

# Cleanup
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    CLEANUP                                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

read -p "Vuoi fermare e rimuovere il container? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "→ Fermo container..."
    docker stop llamacpp-addon-demo
    
    echo "→ Rimuovo container..."
    docker rm llamacpp-addon-demo
    
    echo "✓ Cleanup completato!"
else
    echo "Container lasciato in esecuzione."
    echo ""
    echo "Per fermarlo manualmente:"
    echo "  docker stop llamacpp-addon-demo"
    echo "  docker rm llamacpp-addon-demo"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    DEMO COMPLETATA!                       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📚 Per maggiori informazioni:"
echo "  - README.md           Documentazione completa"
echo "  - QUICKSTART.md       Guida rapida"
echo "  - examples.py         Esempi Python"
echo "  - tests/test_api.py   Test suite"
echo ""
