ARG BUILD_FROM
FROM alpine:3.18 AS builder

# Installazione dipendenze per build su Alpine
RUN apk add --no-cache \
    build-base \
    cmake \
    git \
    curl-dev \
    wget \
    linux-headers \
    pkgconfig

# Clone e build llama.cpp
WORKDIR /build
RUN git clone https://github.com/ggml-org/llama.cpp.git
WORKDIR /build/llama.cpp

# Build statico per massima compatibilità
# -DGGML_STATIC=ON per build completamente statico
RUN cmake -B build \
    -DCMAKE_BUILD_TYPE=Release \
    -DGGML_NATIVE=OFF \
    -DGGML_STATIC=ON \
    -DBUILD_SHARED_LIBS=OFF \
    -DLLAMA_CURL=ON \
    && cmake --build build --config Release --target llama-server -j$(nproc)

# Immagine finale leggera
FROM ${BUILD_FROM}

# Installazione runtime dependencies per Alpine Linux
RUN apk add --no-cache \
    python3 \
    py3-pip \
    curl \
    libgomp \
    libstdc++ \
    libgcc \
    ca-certificates

# Installazione dipendenze Python
RUN pip3 install --no-cache-dir --break-system-packages \
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
