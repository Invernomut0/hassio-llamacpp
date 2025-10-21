ARG BUILD_FROM
FROM ubuntu:22.04 AS builder

# Installazione dipendenze per build
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    curl \
    libcurl4-openssl-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Clone e build llama.cpp
WORKDIR /build
RUN git clone https://github.com/ggml-org/llama.cpp.git
WORKDIR /build/llama.cpp

# Build con supporto CUDA opzionale (commentato per CPU-only)
# Per GPU: aggiungere -DGGML_CUDA=ON
RUN cmake -B build \
    -DGGML_NATIVE=OFF \
    -DBUILD_SHARED_LIBS=OFF \
    -DLLAMA_CURL=ON \
    && cmake --build build --config Release --target llama-server -j$(nproc)

# Immagine finale leggera
FROM ${BUILD_FROM}

# Installazione runtime dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    libgomp1 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Installazione dipendenze Python
RUN pip3 install --no-cache-dir \
    requests \
    flask \
    flask-cors \
    pyyaml

# Copia binario llama-server dal builder
COPY --from=builder /build/llama.cpp/build/bin/llama-server /usr/local/bin/llama-server

# Crea directory per modelli e configurazioni
RUN mkdir -p /data/models /config

# Copia scripts
COPY run.sh /
COPY ha_service.py /
RUN chmod a+x /run.sh

WORKDIR /data

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

CMD ["/run.sh"]
