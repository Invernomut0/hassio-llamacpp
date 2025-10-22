# Debugging: "Model doesn't understand Home Assistant context"

## Problem

When you ask the model about your smart home (e.g., "What lights are on?"), it responds:

> "As a language model, I don't have access to personal information like the lights in your house..."

## Root Cause

The model is **not receiving** or **not using** the Home Assistant context that should be included in the system prompt.

## Diagnostic Steps

### 1. Check Service Health

```bash
curl http://localhost:5000/api/health
```

Expected output:
```json
{
  "status": "ok",
  "llama_server": "ok",
  "active_conversations": 0
}
```

### 2. Verify HA Entity Access

```bash
curl http://localhost:5000/api/ha/entities?domain=light
```

Expected: List of lights with their current states.

If this **fails**, the addon cannot access Home Assistant API:
- Check `hassio_api: true` in `config.yaml`
- Verify `SUPERVISOR_TOKEN` environment variable
- Check addon permissions

### 3. Inspect System Prompt

```bash
curl "http://localhost:5000/api/debug/prompt?domains=light"
```

Expected output should include:
```json
{
  "prompt": "You are a smart home assistant...\n=== CURRENT SMART HOME STATUS ===\n...(list of lights)...",
  "length": 1500,
  "tokens_estimate": 400
}
```

If the prompt **doesn't contain entity data**:
- The HA API call is failing silently
- Check logs: `docker logs addon_xxx_llamacpp`

### 4. Test with Explicit Request

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What lights are on?",
    "language": "en",
    "include_entities": true,
    "include_areas": true,
    "entity_domains": ["light"],
    "max_tokens": 200
  }'
```

Expected: Response mentioning specific lights by name.

## Common Issues

### Issue 1: Empty or Missing Context

**Symptom:** Prompt doesn't contain entity data

**Solutions:**

1. **Check config defaults:**
   ```yaml
   auto_fetch_entities: true
   include_areas: true
   ```

2. **Explicitly request context in API call:**
   ```json
   {
     "message": "...",
     "include_entities": true,
     "include_areas": true
   }
   ```

3. **Verify HA API access:**
   ```python
   # In ha_service.py logs, look for:
   "Impossibile recuperare contesto HA: ..."
   ```

### Issue 2: Model Ignores Context

**Symptom:** Context is in prompt, but model doesn't use it

**Possible causes:**

1. **Model too small:** Small models (<3B parameters) may not follow complex instructions
   - **Solution:** Use a larger model (7B+ recommended)

2. **Prompt too long:** Context exceeds model's attention
   - **Solution:** Reduce domains: `"entity_domains": ["light"]`
   - Increase `context_size` in config.yaml

3. **Prompt format unclear:** Model doesn't understand the instructions
   - **Solution:** The new prompt (v1.1.0) is more explicit with markers:
     ```
     === CURRENT SMART HOME STATUS ===
     (data here)
     === END OF SMART HOME STATUS ===
     
     IMPORTANT INSTRUCTIONS:
     1. You HAVE ACCESS to the smart home data shown above
     2. When asked about lights, USE THE DATA PROVIDED
     ```

### Issue 3: Wrong Language

**Symptom:** Model responds in wrong language

**Solution:**
```json
{
  "message": "Quali luci sono accese?",
  "language": "it"
}
```

Or set default in `config.yaml`:
```yaml
response_language: "it"
```

## Testing Checklist

- [ ] Health check returns OK
- [ ] `/api/ha/entities` returns actual entities
- [ ] `/api/debug/prompt` contains entity data
- [ ] Chat response mentions specific entity names
- [ ] Response is in correct language

## Advanced Debugging

### Enable Debug Logging

Edit `config.yaml`:
```yaml
log_level: "debug"
```

Restart addon and check logs:
```bash
docker logs -f addon_xxx_llamacpp
```

Look for:
- `"Configurazione caricata: {...}"` - Config loaded
- `"Impossibile recuperare contesto HA"` - HA context fetch failed
- HTTP requests to `http://supervisor/core/api`

### Manual HA API Test

Inside the addon container:
```bash
curl -H "Authorization: Bearer $SUPERVISOR_TOKEN" \
  http://supervisor/core/api/states | jq .
```

Should return array of entity states.

### Check Model Capabilities

Small models may not handle complex prompts well. Test with:

**Simple prompt (no context):**
```json
{
  "message": "The light called 'kitchen_light' is on. What lights are on?",
  "include_entities": false
}
```

If this works but the full context doesn't, your model may be too small.

## Solutions Summary

| Problem | Solution |
|---------|----------|
| No entities returned | Check `hassio_api: true`, verify permissions |
| Empty prompt context | Set `auto_fetch_entities: true` in config |
| Model ignores context | Use larger model (7B+), reduce context size |
| Wrong language | Set `"language": "it"` in request |
| Context too large | Filter domains: `["light", "switch"]` |
| Timeout errors | Increase `max_tokens`, reduce entity count |

## Still Not Working?

1. **Run the diagnostic script:**
   ```bash
   python3 test_quick_context.py
   ```

2. **Check logs for errors:**
   ```bash
   ha addons logs addon_xxx_llamacpp --tail 100
   ```

3. **Try the legacy simple prompt:**
   ```json
   {
     "message": "List all lights in the format: light.xxx: state",
     "include_entities": true,
     "include_areas": false
   }
   ```

4. **Test with minimal context:**
   ```json
   {
     "message": "What lights are on?",
     "entity_domains": ["light"],
     "max_tokens": 100
   }
   ```

5. **File an issue** on GitHub with:
   - Addon version
   - Model used
   - Output of `test_quick_context.py`
   - Relevant logs

---

**Version:** 1.1.0  
**Last Updated:** 2025-01-15
