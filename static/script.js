// Copyright © Sanjiva Kyosan — Kyosan Ethical AI System
// API Base URL
const API_BASE = 'http://localhost:5000/api';

// State Management
let conversationHistory = [];
let currentConversationId = null;

// DOM Elements
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const outputArea = document.getElementById('outputArea');
const followUpContainer = document.getElementById('followUpContainer');
const clearBtn = document.getElementById('clearBtn');
const newConversationBtn = document.getElementById('newConversationBtn');
const saveConversationBtn = document.getElementById('saveConversationBtn');
const loadConversationBtn = document.getElementById('loadConversationBtn');
const conversationModal = document.getElementById('conversationModal');
const saveModal = document.getElementById('saveModal');
const conversationList = document.getElementById('conversationList');
const conversationName = document.getElementById('conversationName');
const confirmSaveBtn = document.getElementById('confirmSaveBtn');

// Parameter Controls
const temperature = document.getElementById('temperature');
const maxTokens = document.getElementById('maxTokens');
const topP = document.getElementById('topP');
const topK = document.getElementById('topK');
const frequencyPenalty = document.getElementById('frequencyPenalty');
const presencePenalty = document.getElementById('presencePenalty');
const stopSequences = document.getElementById('stopSequences');
const repetitionPenalty = document.getElementById('repetitionPenalty');
const seed = document.getElementById('seed');
const minP = document.getElementById('minP');
const topA = document.getElementById('topA');

// Harm Detection Controls
const harmSensitivity = document.getElementById('harmSensitivity');
const contextAwareness = document.getElementById('contextAwareness');
const crisisMode = document.getElementById('crisisMode');

// Parameter Value Displays
const temperatureValue = document.getElementById('temperatureValue');
const maxTokensValue = document.getElementById('maxTokensValue');
const topPValue = document.getElementById('topPValue');
const topKValue = document.getElementById('topKValue');
const frequencyPenaltyValue = document.getElementById('frequencyPenaltyValue');
const presencePenaltyValue = document.getElementById('presencePenaltyValue');
const repetitionPenaltyValue = document.getElementById('repetitionPenaltyValue');
const seedValue = document.getElementById('seedValue');
const minPValue = document.getElementById('minPValue');
const topAValue = document.getElementById('topAValue');
const harmSensitivityValue = document.getElementById('harmSensitivityValue');
const contextAwarenessValue = document.getElementById('contextAwarenessValue');

// Parameters Panel Toggle
const toggleParametersBtn = document.getElementById('toggleParametersBtn');
const paramsGrid = document.getElementById('paramsGrid');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    setupParamInfoButtons();
    updateParameterDisplays();
});

// Parameter info buttons: show/hide description on click, close on outside click
function setupParamInfoButtons() {
    const panel = document.getElementById('parametersPanel');
    if (!panel) return;

    panel.addEventListener('click', (e) => {
        const btn = e.target.closest('.param-info-btn');
        if (!btn) return;
        e.preventDefault();
        e.stopPropagation();
        const box = btn.parentElement.querySelector('.param-info-box');
        const wasVisible = box && box.classList.contains('visible');
        document.querySelectorAll('.param-info-box.visible').forEach((b) => b.classList.remove('visible'));
        if (box && !wasVisible) box.classList.add('visible');
    });

    document.addEventListener('click', (e) => {
        if (e.target.closest('.param-info-btn') || e.target.closest('.param-info-box')) return;
        document.querySelectorAll('.param-info-box.visible').forEach((b) => b.classList.remove('visible'));
    });
}

// Event Listeners
function setupEventListeners() {
    // Send button
    sendBtn.addEventListener('click', (e) => {
        e.preventDefault();
        sendMessage(userInput);
    });
    
    // Enter key to send (Shift+Enter for new line)
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage(userInput);
        }
    });
    
    // Parameter sliders
    temperature.addEventListener('input', () => {
        temperatureValue.textContent = temperature.value;
    });
    
    maxTokens.addEventListener('input', () => {
        maxTokensValue.textContent = maxTokens.value;
    });
    
    topP.addEventListener('input', () => {
        topPValue.textContent = topP.value;
    });
    
    topK.addEventListener('input', () => {
        topKValue.textContent = topK.value;
    });
    
    frequencyPenalty.addEventListener('input', () => {
        frequencyPenaltyValue.textContent = frequencyPenalty.value;
    });
    
    presencePenalty.addEventListener('input', () => {
        presencePenaltyValue.textContent = presencePenalty.value;
    });

    repetitionPenalty.addEventListener('input', () => {
        repetitionPenaltyValue.textContent = repetitionPenalty.value;
    });

    seed.addEventListener('input', () => {
        seedValue.textContent = seed.value.trim() === '' ? '—' : seed.value;
    });

    minP.addEventListener('input', () => {
        minPValue.textContent = minP.value;
    });

    topA.addEventListener('input', () => {
        topAValue.textContent = topA.value;
    });
    
    harmSensitivity.addEventListener('input', () => {
        harmSensitivityValue.textContent = harmSensitivity.value;
    });
    
    contextAwareness.addEventListener('input', () => {
        contextAwarenessValue.textContent = contextAwareness.value;
    });
    
    // Toggle parameters panel
    toggleParametersBtn.addEventListener('click', () => {
        const harmDetectionSection = document.querySelector('.harm-detection-section');
        const isHidden = paramsGrid.style.display === 'none';
        paramsGrid.style.display = isHidden ? 'grid' : 'none';
        if (harmDetectionSection) {
            harmDetectionSection.style.display = isHidden ? 'block' : 'none';
        }
        toggleParametersBtn.textContent = isHidden ? 'Hide Parameters' : 'Show Parameters';
    });
    
    // Control buttons
    clearBtn.addEventListener('click', clearConversation);
    newConversationBtn.addEventListener('click', newConversation);
    saveConversationBtn.addEventListener('click', openSaveModal);
    loadConversationBtn.addEventListener('click', openLoadModal);
    confirmSaveBtn.addEventListener('click', saveConversation);
    
    // Modal close buttons
    document.querySelectorAll('.close').forEach(closeBtn => {
        closeBtn.addEventListener('click', (e) => {
            e.target.closest('.modal').style.display = 'none';
        });
    });
    
    // Close modal on outside click
    window.addEventListener('click', (e) => {
        if (e.target === conversationModal) {
            conversationModal.style.display = 'none';
        }
        if (e.target === saveModal) {
            saveModal.style.display = 'none';
        }
    });
}

function updateParameterDisplays() {
    temperatureValue.textContent = temperature.value;
    maxTokensValue.textContent = maxTokens.value;
    topPValue.textContent = topP.value;
    topKValue.textContent = topK.value;
    frequencyPenaltyValue.textContent = frequencyPenalty.value;
    presencePenaltyValue.textContent = presencePenalty.value;
    repetitionPenaltyValue.textContent = repetitionPenalty.value;
    seedValue.textContent = seed.value.trim() === '' ? '—' : seed.value;
    minPValue.textContent = minP.value;
    topAValue.textContent = topA.value;
    harmSensitivityValue.textContent = harmSensitivity.value;
    contextAwarenessValue.textContent = contextAwareness.value;
}

// Send Message
async function sendMessage(inputElementOrMessage = null) {
    let message;
    let inputElement;
    
    // Handle both string message and input element
    if (typeof inputElementOrMessage === 'string') {
        message = inputElementOrMessage.trim();
        inputElement = userInput; // Use main input for clearing
    } else {
        inputElement = inputElementOrMessage || userInput;
        // Validate input element
        if (!inputElement) {
            console.error('Invalid input element:', inputElement);
            return;
        }
        message = inputElement.value ? inputElement.value.trim() : '';
    }
    
    if (!message) {
        return;
    }
    
    // Disable send button
    sendBtn.disabled = true;
    sendBtn.textContent = 'Sending...';
    
    // Add user message to output
    addMessageToOutput('user', message);
    
    // Clear input if it's a valid element
    if (inputElement && inputElement.value !== undefined) {
        inputElement.value = '';
    }
    
    // Show loading
    const loadingId = addLoadingIndicator();
    
    try {
        // Get parameters
        const parameters = getParameters();
        
        // Debug logging
        console.log('Sending message with parameters:', {
            harm_sensitivity: parameters.harm_sensitivity,
            context_awareness: parameters.context_awareness,
            crisis_mode: parameters.crisis_mode
        });
        
        // Prepare context from conversation history
        const context = conversationHistory.map(msg => ({
            role: msg.role,
            content: msg.content
        }));
        
        // Send to API
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                context: context,
                parameters: parameters
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Add assistant response to output
            addMessageToOutput('assistant', data.response, data.metadata);
            
            // Update conversation history
            conversationHistory.push({
                role: 'user',
                content: message,
                timestamp: new Date().toISOString()
            });
            
            conversationHistory.push({
                role: 'assistant',
                content: data.response,
                timestamp: data.timestamp,
                metadata: data.metadata
            });
            
            // Add follow-up input box
            addFollowUpInput();
        } else {
            addMessageToOutput('system', `Error: ${data.error || 'Unknown error'}`);
        }
    } catch (error) {
        addMessageToOutput('system', `Error: ${error.message}`);
    } finally {
        // Remove loading indicator
        removeLoadingIndicator(loadingId);
        
        // Re-enable send button
        sendBtn.disabled = false;
        sendBtn.textContent = 'Send';
        
        // Focus on the last follow-up input if it exists
        const lastFollowUp = followUpContainer.querySelector('.follow-up-input:last-of-type');
        if (lastFollowUp) {
            lastFollowUp.focus();
        } else {
            userInput.focus();
        }
    }
}

// Get Parameters
function getParameters() {
    const params = {
        temperature: parseFloat(temperature.value),
        max_tokens: parseInt(maxTokens.value),
        top_p: parseFloat(topP.value),
        top_k: parseInt(topK.value),
        frequency_penalty: parseFloat(frequencyPenalty.value),
        presence_penalty: parseFloat(presencePenalty.value),
        repetition_penalty: parseFloat(repetitionPenalty.value),
        min_p: parseFloat(minP.value),
        top_a: parseFloat(topA.value),
        // Harm detection parameters
        harm_sensitivity: parseFloat(harmSensitivity.value),
        context_awareness: parseFloat(contextAwareness.value),
        crisis_mode: crisisMode.checked
    };

    const seedVal = seed.value.trim();
    if (seedVal !== '' && !isNaN(parseInt(seedVal, 10))) {
        params.seed = parseInt(seedVal, 10);
    }
    
    if (stopSequences.value.trim()) {
        params.stop_sequences = stopSequences.value.split(',').map(s => s.trim());
    }
    
    return params;
}

// Add Message to Output
function addMessageToOutput(role, content, metadata = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const header = document.createElement('div');
    header.className = 'message-header';
    header.textContent = role === 'user' ? 'You' : role === 'assistant' ? 'Assistant' : 'System';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = content;
    
    const timestamp = document.createElement('div');
    timestamp.className = 'message-timestamp';
    timestamp.textContent = new Date().toLocaleString();
    
    messageDiv.appendChild(header);
    messageDiv.appendChild(messageContent);
    messageDiv.appendChild(timestamp);
    
    if (metadata && role === 'assistant') {
        const metadataDiv = document.createElement('div');
        metadataDiv.className = 'message-timestamp';
        metadataDiv.style.marginTop = '10px';
        metadataDiv.style.fontSize = '11px';
        metadataDiv.textContent = `Ethical Checks: Harm=${metadata.ethical_checks?.harm_detection?.has_harmful_intent ? 'Flagged' : 'Passed'}, Integrity=${metadata.ethical_checks?.system_integrity?.is_safe ? 'Passed' : 'Failed'}`;
        messageDiv.appendChild(metadataDiv);
    }
    
    outputArea.appendChild(messageDiv);
    outputArea.scrollTop = outputArea.scrollHeight;
}

// Add Loading Indicator
function addLoadingIndicator() {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'loading';
    loadingDiv.id = 'loading-indicator';
    loadingDiv.textContent = 'Processing...';
    outputArea.appendChild(loadingDiv);
    outputArea.scrollTop = outputArea.scrollHeight;
    return 'loading-indicator';
}

// Remove Loading Indicator
function removeLoadingIndicator(id) {
    const loading = document.getElementById(id);
    if (loading) {
        loading.remove();
    }
}

// Add Follow-up Input
function addFollowUpInput() {
    const followUpSection = document.createElement('div');
    followUpSection.className = 'follow-up-section';
    
    const label = document.createElement('label');
    label.textContent = 'Follow-up Message';
    
    const input = document.createElement('textarea');
    input.className = 'follow-up-input';
    input.placeholder = 'Enter your follow-up message here...';
    input.rows = 4;
    
    const button = document.createElement('button');
    button.className = 'btn btn-red follow-up-btn';
    button.textContent = 'Send Follow-up';
    
    button.addEventListener('click', () => {
        // Get the message before removing the element
        const message = input.value.trim();
        if (message) {
            // Remove the follow-up section first to prevent issues
            followUpSection.remove();
            // Send the message directly as a string
            sendMessage(message);
        }
    });
    
    // Enter key to send
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            // Get message and send directly
            const message = input.value.trim();
            if (message) {
                followUpSection.remove();
                sendMessage(message);
            }
        }
    });
    
    followUpSection.appendChild(label);
    followUpSection.appendChild(input);
    followUpSection.appendChild(button);
    
    followUpContainer.appendChild(followUpSection);
    
    // Focus on the new input
    input.focus();
}

// Clear Conversation
async function clearConversation() {
    if (confirm('Are you sure you want to clear the conversation?')) {
        try {
            const response = await fetch(`${API_BASE}/clear`, {
                method: 'POST'
            });
            
            if (response.ok) {
                conversationHistory = [];
                outputArea.innerHTML = '';
                followUpContainer.innerHTML = '';
                currentConversationId = null;
            }
        } catch (error) {
            alert(`Error clearing conversation: ${error.message}`);
        }
    }
}

// New Conversation
function newConversation() {
    if (conversationHistory.length > 0) {
        if (confirm('Start a new conversation? Current conversation will be cleared.')) {
            clearConversation();
        }
    }
}

// Open Save Modal
function openSaveModal() {
    if (conversationHistory.length === 0) {
        alert('No conversation to save.');
        return;
    }
    
    conversationName.value = '';
    saveModal.style.display = 'block';
    conversationName.focus();
}

// Save Conversation
async function saveConversation() {
    const name = conversationName.value.trim();
    
    if (!name) {
        alert('Please enter a conversation name.');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/conversations`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                messages: conversationHistory
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentConversationId = data.id;
            saveModal.style.display = 'none';
            alert('Conversation saved successfully!');
        } else {
            alert(`Error: ${data.error || 'Unknown error'}`);
        }
    } catch (error) {
        alert(`Error saving conversation: ${error.message}`);
    }
}

// Open Load Modal
async function openLoadModal() {
    try {
        const response = await fetch(`${API_BASE}/conversations`);
        const data = await response.json();
        
        if (response.ok) {
            displayConversations(data.conversations);
            conversationModal.style.display = 'block';
        } else {
            alert(`Error: ${data.error || 'Unknown error'}`);
        }
    } catch (error) {
        alert(`Error loading conversations: ${error.message}`);
    }
}

// Display Conversations
function displayConversations(conversations) {
    conversationList.innerHTML = '';
    
    if (conversations.length === 0) {
        conversationList.innerHTML = '<p style="color: #666; text-align: center;">No saved conversations</p>';
        return;
    }
    
    conversations.forEach(conv => {
        const item = document.createElement('div');
        item.className = 'conversation-item';
        
        const title = document.createElement('h3');
        title.textContent = conv.name;
        
        const info = document.createElement('p');
        info.textContent = `${conv.message_count} messages • ${new Date(conv.timestamp).toLocaleString()}`;
        
        item.appendChild(title);
        item.appendChild(info);
        
        item.addEventListener('click', () => {
            loadConversation(conv.id);
        });
        
        conversationList.appendChild(item);
    });
}

// Load Conversation
async function loadConversation(conversationId) {
    try {
        const response = await fetch(`${API_BASE}/conversations/${conversationId}`);
        const data = await response.json();
        
        if (response.ok) {
            // Clear current conversation
            conversationHistory = [];
            outputArea.innerHTML = '';
            followUpContainer.innerHTML = '';
            
            // Load conversation data
            currentConversationId = data.id;
            conversationHistory = data.messages || [];
            
            // Display messages
            conversationHistory.forEach(msg => {
                addMessageToOutput(msg.role, msg.content, msg.metadata);
            });
            
            // Close modal
            conversationModal.style.display = 'none';
            
            // Add follow-up input if there are messages
            if (conversationHistory.length > 0) {
                addFollowUpInput();
            }
        } else {
            alert(`Error: ${data.error || 'Unknown error'}`);
        }
    } catch (error) {
        alert(`Error loading conversation: ${error.message}`);
    }
}

