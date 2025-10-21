# Contribuire al Progetto

Grazie per il tuo interesse nel contribuire all'addon Llama.cpp per Home Assistant! 🎉

## 📋 Linee Guida

### Codice di Condotta

- Rispetta gli altri contributori
- Sii costruttivo nelle critiche
- Concentrati sul problema, non sulla persona
- Aiuta a creare un ambiente accogliente

## 🐛 Segnalazione Bug

Prima di aprire un issue:
1. ✅ Controlla che non esista già un issue simile
2. ✅ Verifica di usare l'ultima versione
3. ✅ Leggi la documentazione e TROUBLESHOOTING

### Template Issue Bug

```markdown
**Descrizione Bug**
Descrizione chiara e concisa del bug.

**Riproduzione**
Passi per riprodurre:
1. Vai su '...'
2. Clicca su '...'
3. Vedi errore

**Comportamento Atteso**
Cosa ti aspettavi che accadesse.

**Screenshots**
Se applicabile, aggiungi screenshot.

**Ambiente:**
- OS: [es. Home Assistant OS 11.2]
- Architettura: [es. amd64, aarch64]
- Versione Addon: [es. 1.0.0]
- Modello LLM: [es. Gemma 3 1B Q4]

**Log**
```
Incolla qui i log dell'addon
```

**Contesto Aggiuntivo**
Qualsiasi altra informazione rilevante.
```

## 💡 Richiesta Feature

### Template Issue Feature

```markdown
**Descrizione Feature**
Descrizione chiara della funzionalità desiderata.

**Motivazione**
Perché questa feature è utile? Quale problema risolve?

**Soluzione Proposta**
Come vorresti che funzionasse?

**Alternative Considerate**
Hai considerato altre soluzioni?

**Contesto Aggiuntivo**
Screenshot, mockup, esempi...
```

## 🔧 Contribuire al Codice

### Setup Ambiente Sviluppo

```bash
# Clone repository
git clone https://github.com/[TUO_USERNAME]/hassio-llamacpp.git
cd hassio-llamacpp

# Installa dipendenze Python
pip install -r requirements.txt

# Build immagine Docker
./build.sh amd64

# Run tests
python3 tests/test_api.py
```

### Workflow Git

1. **Fork** il repository
2. **Clone** il tuo fork localmente
3. **Crea branch** per la tua feature
   ```bash
   git checkout -b feature/amazing-feature
   ```
4. **Commit** le modifiche
   ```bash
   git commit -m "Add: Amazing feature"
   ```
5. **Push** al tuo fork
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Apri Pull Request** sul repository principale

### Commit Messages

Segui il formato:

```
<tipo>: <descrizione breve>

<descrizione dettagliata opzionale>

<footer opzionale>
```

**Tipi:**
- `Add:` - Nuova funzionalità
- `Fix:` - Bug fix
- `Update:` - Modifica funzionalità esistente
- `Remove:` - Rimozione codice
- `Docs:` - Solo documentazione
- `Style:` - Formattazione, punto e virgola, ecc.
- `Refactor:` - Refactoring codice
- `Test:` - Aggiunta o modifica test
- `Chore:` - Manutenzione (build, config, ecc.)

**Esempi:**
```
Add: Support for ARM64 architecture

Update: Improve error handling in chat endpoint

Fix: Memory leak in conversation manager (#42)

Docs: Update README with new API endpoints
```

## 🧪 Testing

### Requisiti Test

- ✅ Tutti i test devono usare **dati reali** (no mock)
- ✅ Coverage > 80%
- ✅ Test devono essere veloci (<2 min totali)
- ✅ Nomi test descrittivi

### Eseguire Test

```bash
# Tutti i test
python3 tests/test_api.py

# Test specifico
python3 -m unittest tests.test_api.TestSingleChatAPI

# Con coverage
pip install coverage
coverage run -m unittest tests.test_api
coverage report
```

### Scrivere Test

```python
def test_new_feature(self):
    """Test per nuova funzionalità X."""
    # Setup
    payload = {"key": "value"}
    
    # Execute
    response = requests.post(f"{BASE_URL}/api/new", json=payload)
    
    # Assert
    self.assertEqual(response.status_code, 200)
    data = response.json()
    self.assertIn("result", data)
    
    # Log
    print(f"✓ Feature X funziona: {data['result']}")
```

## 📝 Documentazione

### Docstrings Python

Usa Google Style:

```python
def my_function(param1: str, param2: int) -> dict:
    """
    Breve descrizione della funzione.
    
    Descrizione più dettagliata se necessaria.
    Può essere su più righe.
    
    Args:
        param1: Descrizione parametro 1
        param2: Descrizione parametro 2
    
    Returns:
        Dizionario con risultati
        
    Raises:
        ValueError: Se param2 è negativo
    
    Example:
        >>> result = my_function("test", 42)
        >>> print(result["status"])
        "ok"
    """
    pass
```

### README Updates

Quando aggiungi feature:
1. Aggiorna README.md con esempi
2. Aggiungi entry in CHANGELOG.md
3. Aggiorna TODO.md se necessario

## 🎨 Stile Codice

### Python (PEP 8)

- Indentazione: 4 spazi
- Linee max 100 caratteri
- Nomi: `snake_case` per funzioni/variabili, `PascalCase` per classi
- Imports ordinati: stdlib, third-party, local
- Type hints dove possibile

```python
from typing import Dict, Optional

def process_data(
    input_data: str,
    options: Optional[Dict[str, any]] = None
) -> Dict[str, str]:
    """Process input data with optional parameters."""
    if options is None:
        options = {}
    
    # Implementation
    return {"status": "ok"}
```

### Bash

- Usa `set -e` per exit on error
- Quote variabili: `"${VAR}"`
- Commenti per sezioni complesse

```bash
#!/bin/bash
set -e

# Download model
MODEL_URL="${1}"
if [ -z "${MODEL_URL}" ]; then
    echo "Error: MODEL_URL required"
    exit 1
fi
```

## 📦 Pull Request

### Checklist PR

Prima di aprire PR, verifica:

- [ ] Codice segue lo stile del progetto
- [ ] Test aggiunti/aggiornati
- [ ] Tutti i test passano
- [ ] Documentazione aggiornata
- [ ] CHANGELOG.md aggiornato
- [ ] No conflitti con `main`
- [ ] Commit messages chiari
- [ ] PR description dettagliata

### Template PR

```markdown
## Descrizione
Descrizione chiara delle modifiche.

## Tipo di Cambiamento
- [ ] Bug fix (non-breaking change)
- [ ] Nuova feature (non-breaking change)
- [ ] Breaking change
- [ ] Documentazione

## Testing
Come hai testato le modifiche?
- [ ] Test unitari
- [ ] Test manuali
- [ ] Test su hardware reale

## Checklist
- [ ] Codice segue stile progetto
- [ ] Self-review completata
- [ ] Commenti aggiunti dove necessario
- [ ] Documentazione aggiornata
- [ ] No warnings generati
- [ ] Test aggiunti
- [ ] Tutti i test passano

## Screenshots (se applicabile)
```

## 🔍 Code Review

### Per Reviewers

- Sii rispettoso e costruttivo
- Fai domande, non accuse
- Fornisci suggerimenti concreti
- Approva quando il codice è buono (non serve perfezione)

### Per Authors

- Rispondi a tutti i commenti
- Non prenderla sul personale
- Spiega le tue scelte se necessario
- Implementa feedback ragionevoli

## 🚀 Release Process

1. Aggiorna versione in `config.yaml` e `config.json`
2. Aggiorna CHANGELOG.md con data release
3. Crea tag Git: `git tag v1.X.Y`
4. Push tag: `git push origin v1.X.Y`
5. GitHub Actions builderà immagini Docker
6. Annuncia release su discussioni

## 📞 Contatti

- **Issues**: Per bug e feature requests
- **Discussions**: Per domande e idee
- **Email**: support@example.com

## 🙏 Riconoscimenti

Tutti i contributori saranno riconosciuti in README.md!

---

**Grazie per contribuire!** 🎉
