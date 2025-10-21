# 🚀 Deployment su GitHub Container Registry (GHCR)

Guida per pubblicare immagini precompilate e velocizzare l'installazione dell'addon.

## 📦 Vantaggi delle Immagini Precompilate

**Con build locale** (attuale):
- ❌ 15-45 minuti di compilazione
- ❌ Richiede risorse significative
- ❌ Può fallire su hardware limitato

**Con immagine precompilata** (GHCR):
- ✅ Installazione in 30-60 secondi
- ✅ Nessuna compilazione necessaria
- ✅ Funziona su qualsiasi hardware

## 🛠️ Setup Iniziale

### 1. Crea Personal Access Token (PAT)

1. Vai su GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Clicca "Generate new token (classic)"
3. Configura:
   - **Note**: `GHCR Access for hassio-llamacpp`
   - **Expiration**: No expiration (o personalizza)
   - **Scopes**: 
     - ✅ `write:packages` (include read)
     - ✅ `delete:packages` (opzionale)
4. Clicca "Generate token"
5. **IMPORTANTE**: Copia il token ora, non lo rivedrai!

### 2. Configura GitHub Secrets

1. Vai al tuo repository → Settings → Secrets and variables → Actions
2. Clicca "New repository secret"
3. Crea:
   - **Name**: `GHCR_TOKEN`
   - **Value**: [Incolla il PAT creato]
4. Salva

## 🔨 Build e Pubblicazione

### Metodo 1: GitHub Actions (Automatico, Raccomandato)

Crea `.github/workflows/build.yml`:

```yaml
name: Build and Publish Docker Images

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]
  workflow_dispatch:

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    strategy:
      matrix:
        arch: [amd64, aarch64]
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GHCR_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          file: ./Dockerfile
          platforms: linux/${{ matrix.arch == 'amd64' && 'amd64' || 'arm64' }}
          push: true
          tags: ${{ env.REGISTRY }}/home-assistant/${{ matrix.arch }}-addon-llamacpp:${{ github.ref_name }}
          build-args: |
            BUILD_FROM=ghcr.io/home-assistant/${{ matrix.arch }}-base:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

**Trigger automatici**:
- Push su `main` → Build automatica
- Tag `v*` (es. `v1.0.0`) → Build release
- Manual dispatch → Build on-demand

### Metodo 2: Build Manuale (Locale)

#### Prerequisiti
```bash
# Installa Docker e buildx
docker buildx create --use --name multiarch --driver docker-container

# Login a GHCR
echo $GHCR_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
```

#### Build Multi-Arch
```bash
# AMD64
docker buildx build \
  --platform linux/amd64 \
  --build-arg BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest \
  --tag ghcr.io/home-assistant/amd64-addon-llamacpp:1.0.0 \
  --push \
  .

# ARM64/AARCH64
docker buildx build \
  --platform linux/arm64 \
  --build-arg BUILD_FROM=ghcr.io/home-assistant/aarch64-base:latest \
  --tag ghcr.io/home-assistant/aarch64-addon-llamacpp:1.0.0 \
  --push \
  .
```

#### Build tutte le architetture insieme
```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag ghcr.io/USERNAME/hassio-llamacpp:latest \
  --tag ghcr.io/USERNAME/hassio-llamacpp:1.0.0 \
  --push \
  .
```

## 📝 Aggiorna Configurazione Addon

Dopo la pubblicazione, aggiorna `config.yaml`:

```yaml
# Decommentare questa riga per usare immagini precompilate
image: "ghcr.io/home-assistant/{arch}-addon-llamacpp"
```

**Nota**: Sostituisci `home-assistant` con il tuo username GitHub se necessario.

## 🔄 Workflow Completo

### Sviluppo
1. Lavora localmente con build locale (riga `image:` commentata)
2. Testa modifiche
3. Commit e push

### Release
1. Tag versione: `git tag v1.0.0 && git push --tags`
2. GitHub Actions fa build automatica
3. Immagini pubblicate su GHCR
4. Decommentare `image:` in `config.yaml`
5. Commit finale: `git commit -am "Release v1.0.0 with prebuilt images"`

### Utenti finali
- Installazione veloce con immagini precompilate
- Nessuna build necessaria

## 🏷️ Versioning

Usa [Semantic Versioning](https://semver.org/):

```bash
# Major release (breaking changes)
git tag v2.0.0

# Minor release (new features, backward compatible)
git tag v1.1.0

# Patch release (bug fixes)
git tag v1.0.1
```

## 📦 Package Visibility

Per default i package GHCR sono **pubblici**. Per cambiarli:

1. Vai su GitHub → Profile → Packages
2. Trova `hassio-llamacpp`
3. Settings → Change visibility

**Raccomandazione**: Mantieni pubblico per facilità d'uso.

## 🧹 Pulizia Vecchie Versioni

```bash
# Via GitHub UI
# Packages → hassio-llamacpp → Package settings → Manage versions

# Via CLI (con gh CLI installato)
gh api \
  --method DELETE \
  -H "Accept: application/vnd.github+json" \
  /user/packages/container/hassio-llamacpp/versions/VERSION_ID
```

## 🔍 Verifica Pubblicazione

### Check su GHCR
```bash
# Verifica esistenza immagine
docker manifest inspect ghcr.io/home-assistant/amd64-addon-llamacpp:1.0.0

# Pull test
docker pull ghcr.io/home-assistant/amd64-addon-llamacpp:1.0.0
```

### Test in Home Assistant
1. Aggiorna repository addon
2. Reinstalla addon
3. Verifica log: deve mostrare "Pulling image" invece di "Building"
4. Installazione completata in <1 minuto

## 📊 Monitoraggio

GitHub fornisce statistiche su:
- Download counts
- Storage usage
- Version history

Accedi via: GitHub Profile → Packages → hassio-llamacpp → Insights

## 🚨 Troubleshooting

### Errore: "denied: permission_denied"
**Causa**: Token senza permessi write:packages
**Fix**: Rigenera PAT con scope corretto

### Errore: "failed to push: unexpected status: 403"
**Causa**: Package esiste ma appartiene a un'organizzazione
**Fix**: Cambia namespace in `config.yaml`

### Build fallisce su ARM64
**Causa**: Emulazione QEMU lenta o timeout
**Fix**: 
- Aumenta timeout: `timeout-minutes: 120` in workflow
- Usa runner ARM nativo (GitHub runners non supportano nativamente)
- Considera build locale su hardware ARM

### Immagine troppo grande (>2 GB)
**Causa**: Layer intermedi non puliti
**Fix**: Multi-stage build (già implementato)

## 💡 Best Practices

1. **Versionamento chiaro**: Usa sempre tag semantici
2. **Build automatiche**: Usa GitHub Actions
3. **Test prima del push**: Build locale prima di committare
4. **Documentazione**: Aggiorna README e CHANGELOG
5. **Cache layers**: Sfrutta cache Docker per build veloci
6. **Multi-arch**: Supporta sia amd64 che arm64

## 📚 Risorse

- [GitHub Container Registry Docs](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Docker Buildx Multi-platform](https://docs.docker.com/build/building/multi-platform/)
- [Home Assistant Addon Development](https://developers.home-assistant.io/docs/add-ons)
- [Semantic Versioning](https://semver.org/)

---

**Prossimi passi**: Dopo aver configurato GHCR, considera di configurare anche:
- Automatic security scanning (Dependabot, Snyk)
- Badge per mostrare build status nel README
- Changelog automatico da commit messages
