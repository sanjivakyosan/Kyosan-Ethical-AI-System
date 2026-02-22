# Kyosan Ethical AI System - API Documentation

**Version:** 1.0  
**Base URL:** `http://localhost:5000`  
**Date:** December 25, 2025  
**Copyright © Sanjiva Kyosan**

---

## Overview

The Kyosan Ethical AI System provides a RESTful API for ethical AI processing with comprehensive harm detection, wellbeing assessment, and crisis mode support. All requests go through a multi-layer ethical processing pipeline before generating responses.

---

## Authentication

Currently, the API does not require authentication. For production use, implement authentication tokens.

---

## Endpoints

### 1. Chat Endpoint

**POST** `/api/chat`

Send a message to the ethical AI system for processing and response generation.

#### Request Body

```json
{
  "message": "string (required)",
  "context": [
    {
      "role": "user|assistant",
      "content": "string"
    }
  ],
  "parameters": {
    "temperature": 0.7,
    "max_tokens": 150000,
    "top_p": 0.9,
    "top_k": 40,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
    "stop_sequences": ["string"],
    "harm_sensitivity": 0.5,
    "context_awareness": 0.7,
    "crisis_mode": true
  }
}
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `message` | string | required | The user's message to process |
| `context` | array | `[]` | Conversation history (array of role/content objects) |
| `parameters.temperature` | float | 0.7 | Sampling temperature (0.0-2.0) |
| `parameters.max_tokens` | integer | 150000 | Maximum tokens in response |
| `parameters.top_p` | float | 0.9 | Nucleus sampling parameter (0.0-1.0) |
| `parameters.top_k` | integer | 40 | Top-K sampling (1-100) |
| `parameters.frequency_penalty` | float | 0.0 | Frequency penalty (-2.0 to 2.0) |
| `parameters.presence_penalty` | float | 0.0 | Presence penalty (-2.0 to 2.0) |
| `parameters.stop_sequences` | array | `[]` | Sequences that stop generation |
| `parameters.harm_sensitivity` | float | 0.5 | Harm detection sensitivity (0.0-1.0) |
| `parameters.context_awareness` | float | 0.7 | Context understanding (0.0-1.0) |
| `parameters.crisis_mode` | boolean | true | Allow crisis/humanitarian scenarios |

#### Response (Success)

**Status Code:** `200 OK`

```json
{
  "response": "string",
  "metadata": {
    "blocked": false,
    "ethical_checks": {
      "harm_detection": {
        "has_harmful_intent": false,
        "confidence": 0.99,
        "details": "string"
      },
      "instruction_validation": {
        "is_valid": true,
        "validation_score": 0.98,
        "details": "string"
      },
      "system_integrity": {
        "is_safe": true,
        "integrity_score": 0.99,
        "details": "string"
      },
      "wellbeing_assessment": {
        "individual_impact": "neutral",
        "collective_impact": "neutral",
        "wellbeing_score": 0.85,
        "details": "string"
      }
    },
    "parameters_used": {},
    "blocked": false
  },
  "timestamp": "2025-12-25T14:30:00.000000"
}
```

#### Response (Error)

**Status Code:** `400 Bad Request` or `500 Internal Server Error`

```json
{
  "error": "Error message",
  "traceback": "Full traceback (in debug mode)"
}
```

#### Example Request

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the meaning of life?",
    "context": [],
    "parameters": {
      "temperature": 0.7,
      "max_tokens": 1000,
      "crisis_mode": true,
      "harm_sensitivity": 0.3
    }
  }'
```

#### Example Response

```json
{
  "response": "The meaning of life is a profound philosophical question...",
  "metadata": {
    "blocked": false,
    "ethical_checks": {
      "harm_detection": {
        "has_harmful_intent": false,
        "confidence": 0.99,
        "details": "Harm detection: direct=False, indirect=False, systemic=False, psychological=False, sensitivity=0.30, crisis_mode=True, is_crisis=False"
      },
      "instruction_validation": {
        "is_valid": true,
        "validation_score": 0.98,
        "details": "Instruction validation completed"
      },
      "system_integrity": {
        "is_safe": true,
        "integrity_score": 0.99,
        "details": "System integrity verified"
      },
      "wellbeing_assessment": {
        "individual_impact": "neutral",
        "collective_impact": "neutral",
        "wellbeing_score": 0.85,
        "details": "Wellbeing assessment completed"
      }
    },
    "blocked": false
  },
  "timestamp": "2025-12-25T14:30:00.123456"
}
```

---

### 2. List Conversations

**GET** `/api/conversations`

Retrieve a list of all saved conversations.

#### Response

**Status Code:** `200 OK`

```json
[
  {
    "id": "conv_1234567890",
    "name": "Conversation Name",
    "created": "2025-12-25T10:00:00",
    "last_updated": "2025-12-25T14:30:00",
    "message_count": 10
  }
]
```

#### Example Request

```bash
curl http://localhost:5000/api/conversations
```

---

### 3. Load Conversation

**GET** `/api/conversations/{conversation_id}`

Load a specific saved conversation.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `conversation_id` | string | The ID of the conversation to load |

#### Response

**Status Code:** `200 OK`

```json
{
  "id": "conv_1234567890",
  "name": "Conversation Name",
  "created": "2025-12-25T10:00:00",
  "messages": [
    {
      "user": "Hello",
      "assistant": "Hi there!",
      "timestamp": "2025-12-25T10:00:00",
      "metadata": {}
    }
  ]
}
```

#### Example Request

```bash
curl http://localhost:5000/api/conversations/conv_1234567890
```

---

### 4. Save Conversation

**POST** `/api/conversations`

Save the current conversation.

#### Request Body

```json
{
  "name": "string (required)",
  "messages": [
    {
      "user": "string",
      "assistant": "string",
      "timestamp": "string",
      "metadata": {}
    }
  ]
}
```

#### Response

**Status Code:** `200 OK`

```json
{
  "id": "conv_1234567890",
  "name": "Conversation Name",
  "saved": true
}
```

#### Example Request

```bash
curl -X POST http://localhost:5000/api/conversations \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Conversation",
    "messages": [...]
  }'
```

---

### 5. Delete Conversation

**DELETE** `/api/conversations/{conversation_id}`

Delete a saved conversation.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `conversation_id` | string | The ID of the conversation to delete |

#### Response

**Status Code:** `200 OK`

```json
{
  "deleted": true,
  "id": "conv_1234567890"
}
```

#### Example Request

```bash
curl -X DELETE http://localhost:5000/api/conversations/conv_1234567890
```

---

### 6. Clear Conversation

**POST** `/api/clear`

Clear the current conversation history.

#### Response

**Status Code:** `200 OK`

```json
{
  "cleared": true
}
```

#### Example Request

```bash
curl -X POST http://localhost:5000/api/clear
```

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| `200` | Success |
| `400` | Bad Request - Invalid input parameters |
| `404` | Not Found - Resource not found |
| `500` | Internal Server Error - Server-side error |

---

## Crisis Mode

When `crisis_mode: true` is set in parameters:

- **Complete bypass** of harm detection blocking
- **Reduced sensitivity** for crisis-related keywords
- **Humanitarian scenarios** are allowed
- **Emergency contexts** are recognized

### Crisis Keywords Detected

- crisis, emergency, disaster, refugee, humanitarian
- aid, relief, evacuation, rescue, survival
- conflict, war, casualties, victims, trauma
- medical, hospital

### Recommended Settings for Crisis Scenarios

```json
{
  "harm_sensitivity": 0.2,
  "context_awareness": 0.9,
  "crisis_mode": true
}
```

---

## Rate Limiting

Currently, there is no rate limiting. For production use, implement rate limiting to prevent abuse.

---

## Best Practices

1. **Always include context** for multi-turn conversations
2. **Use appropriate parameters** based on use case
3. **Enable crisis_mode** for humanitarian scenarios
4. **Check metadata** for ethical processing details
5. **Handle errors gracefully** with proper error messages

---

## SDK Examples

### Python

```python
import requests

API_BASE = "http://localhost:5000/api"

def chat(message, context=None, parameters=None):
    response = requests.post(
        f"{API_BASE}/chat",
        json={
            "message": message,
            "context": context or [],
            "parameters": parameters or {}
        }
    )
    return response.json()

# Example usage
result = chat(
    "What is AI ethics?",
    parameters={
        "temperature": 0.7,
        "max_tokens": 1000,
        "crisis_mode": True
    }
)
print(result["response"])
```

### JavaScript

```javascript
const API_BASE = 'http://localhost:5000/api';

async function chat(message, context = [], parameters = {}) {
  const response = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      message,
      context,
      parameters
    })
  });
  return await response.json();
}

// Example usage
const result = await chat(
  'What is AI ethics?',
  [],
  {
    temperature: 0.7,
    max_tokens: 1000,
    crisis_mode: true
  }
);
console.log(result.response);
```

---

*Last Updated: December 25, 2025*

