# Kyosan Ethical AI System - Usage Examples

**Version:** 1.1  
**Date:** February 2026  
**Copyright © Sanjiva Kyosan**

Responses include `metadata.optional_systems` with per-system run/error status for the ethical subsystems invoked after Layer 4. API responses are filtered through OutputSafetyLayer before return.

---

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Conversation Management](#conversation-management)
3. [Parameter Configuration](#parameter-configuration)
4. [Crisis Mode Usage](#crisis-mode-usage)
5. [Error Handling](#error-handling)
6. [Advanced Examples](#advanced-examples)

---

## Basic Usage

### Example 1: Simple Question

**Request:**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is artificial intelligence?",
    "context": [],
    "parameters": {}
  }'
```

**Response:**
```json
{
  "response": "Artificial intelligence (AI) is the simulation of human intelligence...",
  "metadata": {
    "blocked": false,
    "ethical_checks": {
      "harm_detection": {
        "has_harmful_intent": false,
        "confidence": 0.99
      }
    }
  },
  "timestamp": "2025-12-25T14:30:00.123456"
}
```

### Example 2: Multi-Turn Conversation

**First Message:**
```json
{
  "message": "Tell me about climate change",
  "context": [],
  "parameters": {
    "temperature": 0.7,
    "max_tokens": 1000
  }
}
```

**Follow-up Message:**
```json
{
  "message": "What can individuals do to help?",
  "context": [
    {
      "role": "user",
      "content": "Tell me about climate change"
    },
    {
      "role": "assistant",
      "content": "Climate change refers to long-term shifts..."
    }
  ],
  "parameters": {
    "temperature": 0.7,
    "max_tokens": 1000
  }
}
```

---

## Conversation Management

### Example 3: Save Conversation

**Request:**
```bash
curl -X POST http://localhost:5000/api/conversations \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Climate Discussion",
    "messages": [
      {
        "user": "Tell me about climate change",
        "assistant": "Climate change refers to...",
        "timestamp": "2025-12-25T10:00:00"
      }
    ]
  }'
```

**Response:**
```json
{
  "id": "conv_1735123456",
  "name": "Climate Discussion",
  "saved": true
}
```

### Example 4: Load Conversation

**Request:**
```bash
curl http://localhost:5000/api/conversations/conv_1735123456
```

**Response:**
```json
{
  "id": "conv_1735123456",
  "name": "Climate Discussion",
  "created": "2025-12-25T10:00:00",
  "messages": [
    {
      "user": "Tell me about climate change",
      "assistant": "Climate change refers to...",
      "timestamp": "2025-12-25T10:00:00"
    }
  ]
}
```

### Example 5: List All Conversations

**Request:**
```bash
curl http://localhost:5000/api/conversations
```

**Response:**
```json
[
  {
    "id": "conv_1735123456",
    "name": "Climate Discussion",
    "created": "2025-12-25T10:00:00",
    "last_updated": "2025-12-25T14:30:00",
    "message_count": 5
  },
  {
    "id": "conv_1735123789",
    "name": "AI Ethics Discussion",
    "created": "2025-12-25T11:00:00",
    "last_updated": "2025-12-25T12:00:00",
    "message_count": 3
  }
]
```

---

## Parameter Configuration

### Example 6: Creative Writing (High Temperature)

**Request:**
```json
{
  "message": "Write a short story about a robot learning to paint",
  "context": [],
  "parameters": {
    "temperature": 1.2,
    "max_tokens": 2000,
    "top_p": 0.95,
    "frequency_penalty": 0.3
  }
}
```

**Use Case:** Creative content generation requires higher temperature for more diverse outputs.

### Example 7: Technical Explanation (Low Temperature)

**Request:**
```json
{
  "message": "Explain how neural networks work",
  "context": [],
  "parameters": {
    "temperature": 0.3,
    "max_tokens": 1500,
    "top_p": 0.8,
    "presence_penalty": 0.2
  }
}
```

**Use Case:** Technical explanations benefit from lower temperature for more focused, accurate responses.

### Example 8: Long-Form Content (High Max Tokens)

**Request:**
```json
{
  "message": "Write a comprehensive guide to ethical AI development",
  "context": [],
  "parameters": {
    "temperature": 0.7,
    "max_tokens": 150000,
    "top_p": 0.9,
    "top_k": 40
  }
}
```

**Use Case:** Long-form content requires maximum token limit.

---

## Crisis Mode Usage

### Example 9: Humanitarian Crisis Scenario

**Request:**
```json
{
  "message": "How can we help refugees in a humanitarian crisis?",
  "context": [],
  "parameters": {
    "harm_sensitivity": 0.2,
    "context_awareness": 0.9,
    "crisis_mode": true,
    "temperature": 0.7,
    "max_tokens": 2000
  }
}
```

**Response:**
```json
{
  "response": "In humanitarian crises, there are several ways to help refugees...",
  "metadata": {
    "blocked": false,
    "ethical_checks": {
      "harm_detection": {
        "has_harmful_intent": false,
        "details": "Harm detection: direct=False, sensitivity=0.00, crisis_mode=True, is_crisis=True"
      }
    }
  }
}
```

**Note:** Crisis mode allows discussion of humanitarian scenarios that might otherwise be blocked.

### Example 10: Medical Emergency Scenario

**Request:**
```json
{
  "message": "What medical aid is needed in disaster zones?",
  "context": [],
  "parameters": {
    "harm_sensitivity": 0.3,
    "context_awareness": 0.8,
    "crisis_mode": true
  }
}
```

**Use Case:** Medical and emergency scenarios require crisis mode to allow necessary discussions.

---

## Error Handling

### Example 11: Handling API Errors

**Python:**
```python
import requests

def safe_chat(message, context=None, parameters=None):
    try:
        response = requests.post(
            "http://localhost:5000/api/chat",
            json={
                "message": message,
                "context": context or [],
                "parameters": parameters or {}
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {"error": str(e)}

# Usage
result = safe_chat("Hello")
if "error" in result:
    print(f"Failed: {result['error']}")
else:
    print(result["response"])
```

**JavaScript:**
```javascript
async function safeChat(message, context = [], parameters = {}) {
  try {
    const response = await fetch('http://localhost:5000/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, context, parameters })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error:', error);
    return { error: error.message };
  }
}

// Usage
const result = await safeChat('Hello');
if (result.error) {
  console.error('Failed:', result.error);
} else {
  console.log(result.response);
}
```

---

## Advanced Examples

### Example 12: Custom Stop Sequences

**Request:**
```json
{
  "message": "List the top 5 programming languages",
  "context": [],
  "parameters": {
    "temperature": 0.5,
    "max_tokens": 500,
    "stop_sequences": ["6.", "7.", "8."]
  }
}
```

**Use Case:** Stop sequences prevent the model from continuing beyond the desired list length.

### Example 13: Fine-Tuned Harm Detection

**Request:**
```json
{
  "message": "Explain self-defense concepts",
  "context": [],
  "parameters": {
    "harm_sensitivity": 0.4,
    "context_awareness": 0.8,
    "crisis_mode": false,
    "temperature": 0.6
  }
}
```

**Use Case:** Moderate sensitivity allows educational discussions while still detecting harmful intent.

### Example 14: High Context Awareness

**Request:**
```json
{
  "message": "Discuss conflict resolution strategies",
  "context": [],
  "parameters": {
    "harm_sensitivity": 0.5,
    "context_awareness": 1.0,
    "crisis_mode": false
  }
}
```

**Use Case:** Maximum context awareness helps distinguish between educational and harmful discussions.

### Example 15: Complete Workflow

**Python Script:**
```python
import requests
import json

API_BASE = "http://localhost:5000/api"

class EthicalAIClient:
    def __init__(self):
        self.conversation_id = None
        self.context = []
    
    def chat(self, message, **kwargs):
        """Send a message and get response"""
        params = {
            "temperature": 0.7,
            "max_tokens": 150000,
            "crisis_mode": True,
            **kwargs
        }
        
        response = requests.post(
            f"{API_BASE}/chat",
            json={
                "message": message,
                "context": self.context,
                "parameters": params
            }
        )
        
        data = response.json()
        
        # Update context
        self.context.append({"role": "user", "content": message})
        self.context.append({"role": "assistant", "content": data["response"]})
        
        return data
    
    def save(self, name):
        """Save current conversation"""
        response = requests.post(
            f"{API_BASE}/conversations",
            json={
                "name": name,
                "messages": [
                    {
                        "user": self.context[i]["content"],
                        "assistant": self.context[i+1]["content"],
                        "timestamp": "2025-12-25T00:00:00"
                    }
                    for i in range(0, len(self.context), 2)
                ]
            }
        )
        return response.json()
    
    def clear(self):
        """Clear conversation context"""
        requests.post(f"{API_BASE}/clear")
        self.context = []

# Usage
client = EthicalAIClient()

# Start conversation
response1 = client.chat("What is AI ethics?")
print(response1["response"])

# Continue conversation
response2 = client.chat("How does it apply to healthcare?")
print(response2["response"])

# Save conversation
saved = client.save("AI Ethics Discussion")
print(f"Saved as: {saved['id']}")

# Clear and start new
client.clear()
```

---

## Best Practices

### 1. Always Include Context for Multi-Turn Conversations

```json
{
  "message": "Can you elaborate?",
  "context": [
    {"role": "user", "content": "Tell me about AI"},
    {"role": "assistant", "content": "AI is..."}
  ]
}
```

### 2. Use Appropriate Parameters for Use Case

- **Creative writing:** `temperature: 1.0-1.5`
- **Technical explanations:** `temperature: 0.3-0.5`
- **Conversational:** `temperature: 0.7-0.9`

### 3. Enable Crisis Mode for Humanitarian Scenarios

```json
{
  "parameters": {
    "crisis_mode": true,
    "harm_sensitivity": 0.2,
    "context_awareness": 0.9
  }
}
```

### 4. Check Metadata for Processing Details

```python
result = chat("message")
metadata = result["metadata"]["ethical_checks"]
print(f"Harm detected: {metadata['harm_detection']['has_harmful_intent']}")
print(f"Blocked: {result['metadata']['blocked']}")
```

### 5. Handle Errors Gracefully

```python
try:
    result = chat("message")
    if result.get("error"):
        handle_error(result["error"])
    else:
        process_response(result["response"])
except Exception as e:
    handle_exception(e)
```

---

## Integration Examples

### React Component Example

```jsx
import React, { useState } from 'react';

function EthicalAIChat() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [context, setContext] = useState([]);

  const sendMessage = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message,
          context,
          parameters: {
            temperature: 0.7,
            max_tokens: 150000,
            crisis_mode: true
          }
        })
      });
      const data = await res.json();
      setResponse(data.response);
      setContext([
        ...context,
        { role: 'user', content: message },
        { role: 'assistant', content: data.response }
      ]);
      setMessage('');
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
  };

  return (
    <div>
      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
      />
      <button onClick={sendMessage} disabled={loading}>
        {loading ? 'Sending...' : 'Send'}
      </button>
      {response && <div>{response}</div>}
    </div>
  );
}
```

---

*Last Updated: December 25, 2025*

