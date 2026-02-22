# Kyosan Ethical AI System - API Interface

A complete web interface for the Kyosan Ethical AI System with full API integration, conversation management, and parameter controls.

## Features

- **Full API Integration**: Connected to ethical processing backend
- **Parameter Controls**: Adjustable temperature, max tokens, top-p, frequency penalty, presence penalty, and stop sequences
- **Text Input/Output**: Clean interface for messages and responses
- **Conversation Management**: 
  - Save conversations with custom names
  - Load saved conversations
  - Clear current conversation
  - Start new conversations
- **Unlimited Follow-ups**: After each response, a new follow-up input box appears
- **Dark Theme UI**: Black and white design with red buttons and controls

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

1. **Sending Messages**: Type your message in the input box and click "Send" or press Enter
2. **Adjusting Parameters**: Use the sliders in the Parameters panel to adjust model behavior
3. **Saving Conversations**: Click "Save Conversation", enter a name, and save
4. **Loading Conversations**: Click "Load Conversation" to see and select from saved conversations
5. **Follow-ups**: After each response, a new follow-up input box appears automatically
6. **Clearing**: Use "Clear" to remove all messages from the current conversation
7. **New Conversation**: Start fresh with "New Conversation"

## API Endpoints

- `POST /api/chat` - Send a message and get a response
- `GET /api/conversations` - List all saved conversations
- `POST /api/conversations` - Save a conversation
- `GET /api/conversations/<id>` - Load a specific conversation
- `DELETE /api/conversations/<id>` - Delete a conversation
- `POST /api/clear` - Clear current conversation history

## File Structure

```
.
├── app.py                 # Flask API backend
├── index.html             # Main UI page
├── static/
│   ├── style.css          # Dark theme styling
│   └── script.js           # Frontend JavaScript
├── conversations/          # Saved conversations (auto-created)
└── requirements.txt        # Python dependencies
```

## UI Design

- **Background**: Pure black (#000000)
- **Text**: White (#ffffff)
- **Borders**: White (#ffffff)
- **Buttons/Controls**: Red (#ff0000)
- **Font**: Courier New monospace

## Notes

- Conversations are saved as JSON files in the `conversations/` directory
- The system integrates with your existing ethical processing framework
- All responses go through ethical checks (harm detection, instruction validation, system integrity, wellbeing assessment)

---

**Copyright © Sanjiva Kyosan**

