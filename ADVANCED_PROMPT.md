# Advanced System Prompt - Home Assistant Integration

## Overview

Version 1.1.0 introduces an **advanced system prompt** that automatically fetches and organizes Home Assistant context before each conversation, similar to the native Home Assistant conversation agent.

## Key Features

### 🌍 Multi-Language Support
- **12 languages supported**: Italian, English, Spanish, French, German, Portuguese, Dutch, Polish, Russian, Chinese, Japanese, Korean
- Automatic language enforcement in responses
- TTS-optimized output (spells out numbers, dates, currencies)

### 🏠 Smart Context Fetching
- **Automatic entity retrieval** before each request
- **Area-based organization**: Entities grouped by room/area
- **Device awareness**: Shows devices and their entities
- **Domain filtering**: Focus on specific entity types (lights, climate, etc.)

### 🔒 Safe Control Rejection
- Model instructed to **reject control requests**
- Suggests using Home Assistant app for device control
- Maintains security by preventing unauthorized actions

## Configuration

### `config.yaml` Options

```yaml
response_language: "it"        # Default language (it, en, es, fr, de, pt, nl, pl, ru, zh, ja, ko)
auto_fetch_entities: true      # Automatically fetch HA entities before each request
include_areas: true            # Organize entities by areas
include_devices: true          # Show device information
```

## System Prompt Structure

The advanced system prompt follows this structure:

```
This smart home is controlled by Home Assistant.

An overview of the areas and the devices in this smart home:

Living Room:
- Devices:
  - Philips Hue Light (model: HUE-001)
- Entities:
  - Living Room Light (light.living_room): on
  - Living Room Temperature (sensor.living_room_temp): 22.5°C

Bedroom:
- Devices:
  - Smart Switch (model: SW-100)
- Entities:
  - Bedroom Light (light.bedroom): off
  - Bedroom Switch (switch.bedroom): on

Answer the user's questions about the world truthfully.
Make sure your text is TTS-readable, and spell out numbers, dates and currencies.
You must speak in Italian unless the user asks you to speak in another language.

If the user wants to control a device, reject the request and suggest using the Home Assistant app.
```

## API Usage

### Chat with Advanced Prompt

**POST** `/api/chat`

```json
{
  "message": "Quali luci sono accese?",
  "language": "it",
  "include_entities": true,
  "include_areas": true,
  "entity_domains": ["light", "switch"],
  "temperature": 0.7,
  "max_tokens": 512
}
```

**Parameters:**
- `message` (required): User message
- `language` (optional): Response language code (default: from config)
- `include_entities` (optional): Fetch HA entities (default: from config)
- `include_areas` (optional): Organize by areas (default: from config)
- `entity_domains` (optional): Filter entity domains (default: all)
- `temperature` (optional): Creativity level (default: 0.7)
- `max_tokens` (optional): Max response tokens (default: 512)

**Response:**
```json
{
  "response": "Attualmente ci sono 3 luci accese: la luce del salotto, la luce della cucina e la luce della camera da letto.",
  "usage": {
    "prompt_tokens": 450,
    "completion_tokens": 35,
    "total_tokens": 485
  }
}
```

### Multi-turn Conversation with Context

**POST** `/api/conversation/start`

```json
{
  "language": "it",
  "include_entities": true,
  "include_areas": true,
  "entity_domains": ["light", "climate"]
}
```

**Response:**
```json
{
  "conversation_id": "conv_1705345200_a1b2c3d4",
  "message": "Conversazione avviata con successo"
}
```

**POST** `/api/conversation/{conversation_id}/message`

```json
{
  "message": "Quali sono le temperature in casa?"
}
```

**Response:**
```json
{
  "response": "Le temperature attuali sono: salotto ventitré gradi, camera da letto ventidue gradi, cucina ventiquattro gradi.",
  "usage": {...},
  "message_count": 2
}
```

## Language Examples

### Italian (it)
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Quante luci sono accese?",
    "language": "it"
  }'
```

**Response:** "Ci sono tre luci accese in questo momento."

### English (en)
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How many lights are on?",
    "language": "en"
  }'
```

**Response:** "There are three lights on right now."

### Spanish (es)
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Cuántas luces están encendidas?",
    "language": "es"
  }'
```

**Response:** "Hay tres luces encendidas en este momento."

## Context Organization

### By Areas (Recommended)

When `include_areas: true`:
- Entities grouped by room/area (Living Room, Bedroom, etc.)
- Devices shown with their model information
- Clear hierarchical structure
- Easier for LLM to understand spatial relationships

### Flat List (Legacy)

When `include_areas: false`:
- Simple list of all entities
- No area organization
- Useful for small homes or testing

## Control Request Handling

The model is instructed to **reject control requests**:

**User:** "Accendi la luce del salotto"  
**Model:** "Mi dispiace, non posso controllare direttamente i dispositivi. Ti suggerisco di utilizzare l'app di Home Assistant per accendere la luce del salotto."

**User:** "Turn on the living room light"  
**Model:** "I'm sorry, I cannot directly control devices. I suggest using the Home Assistant app to turn on the living room light."

This ensures the LLM only provides **information** and **assistance**, not unauthorized control.

## TTS Optimization

Responses are optimized for Text-to-Speech:

❌ **Bad:** "The temperature is 22.5°C"  
✅ **Good:** "The temperature is twenty-two point five degrees Celsius"

❌ **Bad:** "It costs €15.99"  
✅ **Good:** "It costs fifteen euros and ninety-nine cents"

❌ **Bad:** "On 2025-01-15 at 14:30"  
✅ **Good:** "On January fifteenth, two thousand twenty-five at two thirty PM"

## Performance Considerations

### Context Size

The advanced prompt can be large with many entities:
- **Small home** (20 entities): ~500 tokens
- **Medium home** (50 entities): ~1,200 tokens
- **Large home** (100+ entities): ~2,500+ tokens

**Optimization tips:**
- Use `entity_domains` to filter relevant entities only
- Set `include_areas: false` for smaller context
- Adjust `context_size` in config.yaml if needed

### Caching

Consider implementing caching for:
- Entity states (update every 30-60 seconds)
- Area configurations (update on home setup changes)
- Device information (rarely changes)

## Examples

### Check Lights Status
```python
import requests

response = requests.post('http://localhost:5000/api/chat', json={
    'message': 'Quali luci sono accese?',
    'language': 'it',
    'entity_domains': ['light']
})

print(response.json()['response'])
# "Attualmente ci sono tre luci accese: ..."
```

### Check Temperature
```python
response = requests.post('http://localhost:5000/api/chat', json={
    'message': 'Qual è la temperatura in casa?',
    'language': 'it',
    'entity_domains': ['sensor', 'climate']
})

print(response.json()['response'])
# "La temperatura media in casa è di ventidue gradi..."
```

### Multi-room Overview
```python
response = requests.post('http://localhost:5000/api/chat', json={
    'message': 'Dammi un riepilogo dello stato della casa',
    'language': 'it',
    'include_areas': True
})

print(response.json()['response'])
# "Nel salotto ci sono due luci accese, in camera da letto..."
```

## Troubleshooting

### "Context too large" error

**Solution:** Filter entities by domain or disable area organization:
```json
{
  "entity_domains": ["light", "switch"],
  "include_areas": false
}
```

### Wrong language in responses

**Solution:** Explicitly set language in request:
```json
{
  "language": "en"
}
```

Or update default in config.yaml:
```yaml
response_language: "en"
```

### Model still tries to control devices

**Solution:** The system prompt includes rejection instructions, but smaller models may not follow them consistently. Consider:
- Using a larger, more capable model
- Adding explicit control prevention in application logic
- Implementing safety filters on responses

## Best Practices

1. **Always filter by domain** when asking specific questions
2. **Use multi-turn conversations** for follow-up questions
3. **Set appropriate language** for your users
4. **Monitor token usage** with large homes
5. **Test responses** before production deployment

## Migration from Legacy System

Old approach:
```json
{
  "message": "Quali luci?",
  "include_entities": true,
  "include_services": false
}
```

New approach:
```json
{
  "message": "Quali luci?",
  "language": "it",
  "include_areas": true,
  "entity_domains": ["light"]
}
```

Key changes:
- `include_services` removed (not needed in advanced prompt)
- `language` parameter added
- `include_areas` added for better organization
- `entity_domains` for filtering

---

**Version:** 1.1.0  
**Date:** 2025-01-15
