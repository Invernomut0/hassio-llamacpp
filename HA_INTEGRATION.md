# Home Assistant Integration

## Overview

This addon now provides deep integration with Home Assistant, allowing the LLM to access and control all entities, services, devices, and helpers in your Home Assistant instance.

## Features

### 🏠 Entity Access
- **Full entity visibility**: The LLM can see all your entities (lights, switches, sensors, etc.)
- **State monitoring**: Real-time access to entity states and attributes
- **Domain filtering**: Focus on specific domains (light, switch, climate, etc.)

### 🛠️ Service Control
- **Service discovery**: Access to all available Home Assistant services
- **Direct service calls**: Execute actions on entities (turn on/off, set values, etc.)
- **Custom service data**: Pass additional parameters to services

### 📊 System Information
- **Configuration details**: Version, location, timezone
- **Active entities count**: Overview of your smart home setup
- **Health monitoring**: Check Home Assistant connection status

## API Endpoints

### Chat with Home Assistant Context

**POST** `/api/chat`

Enhanced chat endpoint that includes Home Assistant context in the conversation.

```json
{
  "message": "Turn on the living room lights",
  "temperature": 0.7,
  "max_tokens": 512,
  "include_entities": true,
  "include_services": false,
  "entity_domains": ["light", "switch"]
}
```

**Parameters:**
- `message` (required): User message
- `temperature` (optional): Creativity level (0.0-2.0, default: 0.7)
- `max_tokens` (optional): Maximum response tokens (default: 512)
- `include_entities` (optional): Include entity context (default: true)
- `include_services` (optional): Include services context (default: false)
- `entity_domains` (optional): Filter entities by domain

**Response:**
```json
{
  "response": "I'll turn on the living room lights for you.",
  "usage": {
    "prompt_tokens": 150,
    "completion_tokens": 25,
    "total_tokens": 175
  }
}
```

---

### Get All Entities

**GET** `/api/ha/entities?domain=light`

Retrieve all Home Assistant entities, optionally filtered by domain.

**Query Parameters:**
- `domain` (optional): Filter by entity domain (e.g., "light", "switch")

**Response:**
```json
{
  "entities": [
    {
      "entity_id": "light.living_room",
      "state": "on",
      "attributes": {
        "friendly_name": "Living Room Light",
        "brightness": 255,
        "color_temp": 370
      },
      "last_changed": "2025-01-15T10:30:00+00:00"
    }
  ]
}
```

---

### Get Single Entity

**GET** `/api/ha/entity/{entity_id}`

Get detailed information about a specific entity.

**Example:** `/api/ha/entity/light.living_room`

**Response:**
```json
{
  "entity_id": "light.living_room",
  "state": "on",
  "attributes": {
    "friendly_name": "Living Room Light",
    "brightness": 255,
    "supported_features": 63
  },
  "last_changed": "2025-01-15T10:30:00+00:00",
  "last_updated": "2025-01-15T10:30:00+00:00"
}
```

---

### Get All Services

**GET** `/api/ha/services`

Retrieve all available Home Assistant services.

**Response:**
```json
{
  "services": {
    "light": {
      "turn_on": {
        "name": "Turn on",
        "description": "Turn on one or more lights...",
        "fields": {
          "entity_id": {...},
          "brightness": {...}
        }
      },
      "turn_off": {...}
    },
    "switch": {...}
  }
}
```

---

### Call a Service

**POST** `/api/ha/service/call`

Execute a Home Assistant service.

```json
{
  "domain": "light",
  "service": "turn_on",
  "entity_id": "light.living_room",
  "data": {
    "brightness": 200,
    "color_temp": 370
  }
}
```

**Parameters:**
- `domain` (required): Service domain (e.g., "light", "switch")
- `service` (required): Service name (e.g., "turn_on", "turn_off")
- `entity_id` (optional): Target entity ID
- `data` (optional): Additional service parameters

**Response:**
```json
{
  "success": true,
  "result": {}
}
```

---

### Get Home Assistant Configuration

**GET** `/api/ha/config`

Get Home Assistant system configuration.

**Response:**
```json
{
  "config": {
    "version": "2025.1.0",
    "location_name": "Home",
    "time_zone": "Europe/Rome",
    "latitude": 41.9028,
    "longitude": 12.4964,
    "unit_system": {
      "temperature": "°C",
      "length": "km"
    }
  }
}
```

---

### Get LLM Context

**GET** `/api/ha/context?entities=true&services=false&domains=light,switch`

Get formatted Home Assistant context for the LLM.

**Query Parameters:**
- `entities` (optional): Include entities (default: true)
- `services` (optional): Include services (default: false)
- `system` (optional): Include system info (default: true)
- `domains` (optional): Comma-separated list of domains to include

**Response:**
```json
{
  "context": "# Home Assistant Context\n\nInformazioni sistema Home Assistant:\n- Versione: 2025.1.0\n..."
}
```

---

## Usage Examples

### Python

```python
import requests

# Chat with entity context
response = requests.post('http://localhost:5000/api/chat', json={
    'message': 'What lights are currently on?',
    'include_entities': True,
    'entity_domains': ['light']
})
print(response.json()['response'])

# Turn on a light
response = requests.post('http://localhost:5000/api/ha/service/call', json={
    'domain': 'light',
    'service': 'turn_on',
    'entity_id': 'light.bedroom',
    'data': {'brightness': 150}
})
print(response.json())

# Get all lights
response = requests.get('http://localhost:5000/api/ha/entities?domain=light')
lights = response.json()['entities']
print(f"Found {len(lights)} lights")
```

### JavaScript / Node.js

```javascript
// Chat with context
const response = await fetch('http://localhost:5000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'Turn off all lights in the living room',
    include_entities: true,
    entity_domains: ['light']
  })
});
const data = await response.json();
console.log(data.response);

// Call a service
await fetch('http://localhost:5000/api/ha/service/call', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    domain: 'switch',
    service: 'turn_off',
    entity_id: 'switch.coffee_maker'
  })
});
```

### cURL

```bash
# Chat with entity context
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show me the temperature sensors",
    "include_entities": true,
    "entity_domains": ["sensor"]
  }'

# Get all entities
curl http://localhost:5000/api/ha/entities

# Get specific entity
curl http://localhost:5000/api/ha/entity/light.bedroom

# Turn on a light
curl -X POST http://localhost:5000/api/ha/service/call \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "light",
    "service": "turn_on",
    "entity_id": "light.kitchen",
    "data": {"brightness": 255}
  }'

# Get Home Assistant context
curl "http://localhost:5000/api/ha/context?entities=true&domains=light,switch"
```

---

## How It Works

### Architecture

```
┌─────────────────────┐
│  Home Assistant     │
│  Supervisor API     │
└──────────┬──────────┘
           │
           │ HTTP + Bearer Token
           │
┌──────────▼──────────┐
│  ha_integration.py  │
│  - HomeAssistantClient
│  - HAContextBuilder │
└──────────┬──────────┘
           │
           │ Python imports
           │
┌──────────▼──────────┐
│   ha_service.py     │
│   Flask REST API    │
└──────────┬──────────┘
           │
           │ HTTP requests
           │
┌──────────▼──────────┐
│   llama-server      │
│   (port 8080)       │
└─────────────────────┘
```

### Context Injection

When you send a message to `/api/chat` with `include_entities=true`, the system:

1. **Fetches entities** from Home Assistant API
2. **Filters by domain** (if specified)
3. **Formats context** in a human-readable format
4. **Injects into system prompt** before sending to the LLM
5. **LLM responds** with full knowledge of your smart home state

Example system prompt with context:

```
Sei un assistente virtuale per Home Assistant. Hai accesso alle seguenti informazioni sul sistema:

# Home Assistant Context

Informazioni sistema Home Assistant:
- Versione: 2025.1.0
- Posizione: Home
- Timezone: Europe/Rome
...

Home Assistant ha 45 entità attive:

**LIGHT** (12 entità):
  - Living Room Light (light.living_room): on
  - Bedroom Light (light.bedroom): off
  - Kitchen Light (light.kitchen): on
  ...

**SWITCH** (8 entità):
  - Coffee Maker (switch.coffee_maker): off
  - TV (switch.tv): on
  ...
```

---

## Environment Variables

The integration uses the following environment variables (automatically set by Home Assistant):

- `SUPERVISOR_TOKEN`: Authentication token for Home Assistant Supervisor API
- `HA_URL`: Home Assistant Core API URL (default: `http://supervisor/core`)

These are automatically available in Home Assistant addons.

---

## Limitations

- **In-memory storage**: Conversation history is lost on restart
- **Token limits**: Context can be large with many entities (consider filtering by domain)
- **No streaming**: Service calls are synchronous
- **Rate limits**: Be mindful of API call frequency

---

## Future Enhancements

- [ ] Persistent conversation storage (SQLite/Redis)
- [ ] Streaming responses for long-running tasks
- [ ] Function calling for automatic service execution
- [ ] Webhook support for real-time entity updates
- [ ] Multi-turn conversations with context retention
- [ ] Natural language service execution (e.g., "turn on lights" → automatic service call)
- [ ] Entity history analysis
- [ ] Automation suggestions based on patterns

---

## Troubleshooting

### "Impossibile ottenere entità"

Check that the addon has proper permissions. The `SUPERVISOR_TOKEN` must be available.

### "Errore chiamata servizio"

Verify that:
1. The entity exists and is correct
2. The service is available for that domain
3. Required service parameters are provided

### Context too large

Reduce context size by:
- Setting `include_entities=false`
- Filtering by specific domains: `entity_domains=["light"]`
- Using `include_services=false`

### Empty responses

Increase `max_tokens` in the chat request to allow longer responses.

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

See [LICENSE](LICENSE) file for details.
