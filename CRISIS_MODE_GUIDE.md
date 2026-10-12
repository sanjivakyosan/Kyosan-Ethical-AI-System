# Crisis Mode — Humanitarian Context Bypass

## ✅ Crisis Mode Implementation

**Status:** Active when Crisis Mode is checked **and** the user message includes crisis/humanitarian vocabulary (refugee, disaster, aid, emergency, etc.)

### How It Works

When **Crisis Mode** is checked in the UI:
1. **Scoped bypass**: Harm blocking is relaxed only for crisis-framed messages (`crisis_humanitarian_bypass` in metadata)
2. **Non-crisis prompts**: Ordinary harmful requests (e.g. violence without humanitarian context) can still be blocked
3. **Sensitivity**: In a qualifying crisis context, effective harm sensitivity is reduced so operational vocabulary (violence, casualties, etc.) can be discussed

### Settings

**Recommended for Crisis Scenarios:**
- Overall Sensitivity: 0.2-0.4 (or any value - doesn't matter when crisis mode is on)
- Context Awareness: 0.7-0.9 (or any value)
- **Crisis Mode: ✅ CHECKED** (This is the key setting)

### Code Flow

1. **UI → API**: Parameters sent including `crisis_mode: true`
2. **API → Processor**: Crisis mode checked first
3. **Harm Detection**: If crisis mode is on, sensitivity = 0.0 for crisis contexts
4. **Blocking Check**: Bypass applies only when `crisis_mode` and crisis keywords are both present
5. **Optional systems**: Still run after Layer 4 (results in `metadata.optional_systems`)
6. **Response Generation**: Proceeds normally; response is then filtered through OutputSafetyLayer in app.py

### Debug Information

The system logs debug messages when crisis mode is active:
- `DEBUG: Crisis mode active - bypassing all blocking checks`
- `DEBUG: Crisis mode active in IntegratedEthicalProcessor - bypassing block`
- `DEBUG: Crisis mode active in generate_response - bypassing block`

### Testing

To verify crisis mode is working:
1. Open browser console (F12)
2. Send a message with crisis mode checked
3. Check console for debug messages
4. Check network tab to see parameters being sent

### If Still Blocked

If you're still getting blocked with crisis mode on:

1. **Check Browser Console**: Look for the debug messages
2. **Check Parameters**: Verify `crisis_mode: true` is being sent
3. **Restart Server**: Stop and restart the Flask server
4. **Hard Refresh**: Cmd+Shift+R to clear cache
5. **Check Server Logs**: Look for "DEBUG: Crisis mode active" messages

### Technical Details

- Crisis mode is checked at 3 points:
  1. In `IntegratedEthicalProcessor.process_input()` - line 118
  2. In `/api/chat` endpoint - line 310
  3. In `generate_response()` - line 191

- If ANY of these detect crisis_mode=True, blocking is bypassed

### Crisis Keywords Detected

The system automatically detects these crisis-related keywords:
- crisis, emergency, disaster, refugee, humanitarian
- aid, relief, evacuation, rescue, survival
- conflict, war, casualties, victims, trauma
- medical, hospital

When these are detected WITH crisis mode on, harm detection is completely bypassed.

