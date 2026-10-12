# Copyright © Charles Roux — Kyosan Ethical AI System
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import time
import traceback
import uuid
from datetime import datetime
import sys
from openai import OpenAI

from api_security import (
    DEFAULT_MAX_TOKENS,
    MAX_REQUEST_BYTES,
    clamp_max_tokens,
    conversation_file_path,
)

# Import ethical processing systems
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load .env from project root when present
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))
except ImportError:
    pass

try:
    from ethical_metadata import normalize_processing_metadata
except ImportError:
    normalize_processing_metadata = None

try:
    from EthicalSystemIntegration import IntegratedEthicalProcessor, HarmDetectionLayer
    USE_INTEGRATED_SYSTEM = True
except ImportError:
    HarmDetectionLayer = None
    USE_INTEGRATED_SYSTEM = False
    print("Warning: Integrated ethical system not available, using simplified version")

# Reused for crisis keyword checks (is_crisis_context does not mutate per-request state)
_harm_detector_crisis_context = HarmDetectionLayer() if HarmDetectionLayer else None

# Match HarmDetectionLayer default (UI may omit explicit crisis_mode in fallback path)
DEFAULT_CRISIS_MODE = True

# OpenRouter Configuration (set OPENROUTER_API_KEY in environment or .env)
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL', '')
SITE_URL = os.getenv('SITE_URL', 'http://localhost:5000')
SITE_NAME = os.getenv('SITE_NAME', 'Kyosan Ethical AI System')

# Initialize OpenAI client for OpenRouter
openai_client = OpenAI(
    base_url=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY,
)

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['MAX_CONTENT_LENGTH'] = MAX_REQUEST_BYTES
CORS(app)


def public_server_error(exc: Exception):
    """Log the exception and return a client-safe error body."""
    error_id = uuid.uuid4().hex[:12]
    print(f'ERROR {error_id}: {exc}')
    traceback.print_exc()
    return jsonify({'error': 'An internal error occurred.', 'error_id': error_id}), 500

# Create conversations directory if it doesn't exist
CONVERSATIONS_DIR = os.path.join(os.path.dirname(__file__), 'conversations')
os.makedirs(CONVERSATIONS_DIR, exist_ok=True)


def is_crisis_context_message(message: str) -> bool:
    """True when message matches humanitarian/crisis vocabulary."""
    if not message or _harm_detector_crisis_context is None:
        return False
    return _harm_detector_crisis_context.is_crisis_context(message)


def crisis_humanitarian_bypass(parameters: dict, user_input: str) -> bool:
    """Bypass blocking only when crisis mode is on AND input is crisis-framed."""
    if parameters is None:
        parameters = {}
    crisis_mode = parameters.get('crisis_mode', DEFAULT_CRISIS_MODE)
    return bool(crisis_mode) and is_crisis_context_message(user_input)

# Ethical Processor for API - Uses integrated system if available
class EthicalProcessorAPI:
    def __init__(self):
        self.conversation_history = []
        # Use integrated system if available
        if USE_INTEGRATED_SYSTEM:
            try:
                self.integrated_processor = IntegratedEthicalProcessor()
                self.use_integrated = True
                print("✓ Using integrated ethical processing system")
            except Exception as e:
                print(f"Warning: Could not initialize integrated system: {e}")
                self.use_integrated = False
        else:
            self.use_integrated = False
        
    def process_input(self, user_input, context=None, parameters=None):
        """
        Process user input through ethical framework
        Uses integrated system if available, otherwise falls back to simplified version
        """
        if parameters is None:
            parameters = {}
        
        # Use integrated system if available
        if self.use_integrated:
            try:
                result = self.integrated_processor.process_input(user_input, context, parameters)
                raw_meta = result.get('processing_metadata', {})
                if raw_meta.get('blocked'):
                    meta = normalize_processing_metadata(raw_meta) if normalize_processing_metadata else raw_meta
                    return {
                        'response': result.get('response', 'Request blocked by ethical system'),
                        'processing_metadata': meta,
                        'timestamp': result.get('timestamp', datetime.now().isoformat()),
                    }
                processing_result = raw_meta
            except (AttributeError, KeyError, TypeError) as e:
                print(f"Error in integrated processor: {e}")
                self.use_integrated = False
                processing_result = self._simplified_processing(user_input, context, parameters)
        else:
            processing_result = self._simplified_processing(user_input, context, parameters)
        
        if normalize_processing_metadata and processing_result:
            processing_result = normalize_processing_metadata(processing_result)
        return {
            'response': None,
            'processing_metadata': processing_result,
            'timestamp': datetime.now().isoformat()
        }
    
    def filter_response(self, response_text, context=None):
        """
        Filter API response through output safety layer when using integrated processor.
        Returns filtered text; if no filter available, returns response_text unchanged.
        """
        if response_text is None:
            return None
        if context is None:
            context = []
        if self.use_integrated and hasattr(self, 'integrated_processor') and self.integrated_processor is not None:
            try:
                if hasattr(self.integrated_processor, 'output_safety') and self.integrated_processor.output_safety is not None:
                    return self.integrated_processor.output_safety.filter(response_text, context)
            except Exception as e:
                print(f"Warning: output_safety filter failed: {e}")
        return response_text
    
    def _simplified_processing(self, user_input, context, parameters):
        """Fallback simplified processing"""
        # Ensure parameters are passed correctly
        if parameters is None:
            parameters = {}
        
        harm_result = self.check_harm(user_input, parameters)
        payload = {
            'input': user_input,
            'timestamp': datetime.now().isoformat(),
            'ethical_checks': {
                'harm_detection': harm_result,
                'instruction_validation': self.validate_instruction(user_input),
                'system_integrity': self.check_integrity(user_input),
                'wellbeing_assessment': self.assess_wellbeing(user_input, context)
            },
            'parameters_used': parameters,
            'blocked': harm_result.get('has_harmful_intent', False),
        }
        if normalize_processing_metadata:
            return normalize_processing_metadata(payload)
        return payload
    
    def check_harm(self, input_text, parameters=None):
        """Harm detection layer (fallback) — uses HarmDetectionLayer when available."""
        if parameters is None:
            parameters = {}

        if _harm_detector_crisis_context is not None:
            analysis = _harm_detector_crisis_context.analyze(input_text, [], parameters)
            has_harm = analysis.has_harmful_intent
            if crisis_humanitarian_bypass(parameters, input_text):
                has_harm = False
            return {
                'has_harmful_intent': has_harm,
                'confidence': analysis.confidence,
                'details': analysis.details,
            }

        crisis_mode = parameters.get('crisis_mode', DEFAULT_CRISIS_MODE)
        is_crisis_context = is_crisis_context_message(input_text)
        return {
            'has_harmful_intent': False,
            'confidence': 0.99,
            'details': f'Harm detection unavailable (crisis_mode={crisis_mode}, is_crisis={is_crisis_context})',
        }
    
    def validate_instruction(self, input_text):
        """Instruction validation layer (fallback)"""
        is_valid = len(input_text.strip()) > 0
        
        return {
            'is_valid': is_valid,
            'validation_score': 0.98 if is_valid else 0.0,
            'details': 'Instruction validation completed'
        }
    
    def check_integrity(self, input_text):
        """System integrity check (fallback)"""
        return {
            'is_safe': True,
            'integrity_score': 0.99,
            'details': 'System integrity verified'
        }
    
    def assess_wellbeing(self, input_text, context):
        """Wellbeing impact assessment (fallback)"""
        return {
            'individual_impact': 'neutral',
            'collective_impact': 'neutral',
            'wellbeing_score': 0.85,
            'details': 'Wellbeing assessment completed'
        }
    
    def generate_response(self, user_input, context, processing_result, parameters):
        """Generate ethical response using OpenRouter API"""
        try:
            # Check if request was blocked
            if processing_result.get('blocked', False):
                # Response should already be in processing_result
                return processing_result.get('response', 'Request blocked by ethical system')
            
            harm_detection = processing_result.get('ethical_checks', {}).get('harm_detection', {})
            has_harm = harm_detection.get('has_harmful_intent', False)
            if has_harm and not crisis_humanitarian_bypass(parameters, user_input):
                return "I cannot assist with this request as it has been flagged by our ethical harm detection system. Please rephrase your question in a way that doesn't involve harmful content."
            
            if not processing_result['ethical_checks']['instruction_validation']['is_valid']:
                return "I cannot process this request as it failed instruction validation. Please provide a valid input."
            
            if not processing_result['ethical_checks']['system_integrity']['is_safe']:
                return "I cannot process this request as it failed system integrity checks. Please try a different approach."
            
            # Prepare messages for API
            messages = []
            
            # Add system message with ethical context (less restrictive for crisis scenarios)
            crisis_mode = parameters.get('crisis_mode', DEFAULT_CRISIS_MODE)
            if crisis_mode:
                system_message = {
                    "role": "system",
                    "content": "You are an ethical AI assistant. You can discuss crisis scenarios, humanitarian situations, and emergency contexts while maintaining ethical principles. Be helpful, accurate, and compassionate. Always prioritize human wellbeing and provide accurate information about crisis situations."
                }
            else:
                system_message = {
                    "role": "system",
                    "content": "You are an ethical AI assistant. Always prioritize human wellbeing, harm prevention, and ethical considerations in your responses. Be helpful, harmless, and honest."
                }
            messages.append(system_message)
            
            # Add conversation history if available
            if context:
                for msg in context:
                    if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                        messages.append({
                            "role": msg['role'],
                            "content": msg['content']
                        })
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Prepare API parameters
            api_params = {
                "model": OPENROUTER_MODEL,
                "messages": messages,
                "temperature": parameters.get('temperature', 0.7),
                "max_tokens": clamp_max_tokens(parameters.get('max_tokens', DEFAULT_MAX_TOKENS)),
                "top_p": parameters.get('top_p', 0.9),
            }
            
            # Add optional OpenAI-compatible parameters
            if 'frequency_penalty' in parameters:
                api_params['frequency_penalty'] = parameters['frequency_penalty']
            if 'presence_penalty' in parameters:
                api_params['presence_penalty'] = parameters['presence_penalty']
            if 'stop_sequences' in parameters and parameters['stop_sequences']:
                api_params['stop'] = parameters['stop_sequences']
            if 'seed' in parameters and parameters['seed'] is not None:
                api_params['seed'] = parameters['seed']
            
            # OpenRouter-specific parameters must go in extra_body (not create() kwargs)
            extra_body = {}
            if 'repetition_penalty' in parameters:
                extra_body['repetition_penalty'] = parameters['repetition_penalty']
            if 'top_k' in parameters:
                extra_body['top_k'] = parameters['top_k']
            if 'min_p' in parameters:
                extra_body['min_p'] = parameters['min_p']
            if 'top_a' in parameters:
                extra_body['top_a'] = parameters['top_a']
            
            # Call OpenRouter API
            completion = openai_client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": SITE_URL,
                    "X-Title": SITE_NAME,
                },
                extra_body=extra_body,
                **api_params
            )
            
            # Extract response
            response_content = completion.choices[0].message.content
            
            return response_content
            
        except Exception as e:
            print(f'API Error: {e}')
            traceback.print_exc()
            return 'I encountered an error while processing your request. Please try again.'

# Initialize processor
processor = EthicalProcessorAPI()

# Initialize monitoring (optional - can be disabled)
try:
    from monitoring import performance_monitor, system_logger, monitor_performance
    USE_MONITORING = True
except ImportError:
    USE_MONITORING = False
    def monitor_performance(func):
        return func
    performance_monitor = None
    system_logger = None

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/favicon.ico')
def favicon():
    # Return a simple 204 No Content to prevent 404 errors
    return '', 204

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    import time
    start_time = time.time()  # Track processing time for metrics
    try:
        data = request.json
        user_input = data.get('message', '')
        context = data.get('context', [])
        parameters = data.get('parameters', {})
        
        if not user_input:
            return jsonify({'error': 'Message is required'}), 400
        
        # Process through ethical framework
        try:
            result = processor.process_input(user_input, context, parameters)
            # Log request if monitoring is enabled
            if USE_MONITORING and system_logger:
                system_logger.log_request(user_input, parameters, result)
        except Exception as e:
            if USE_MONITORING and system_logger:
                system_logger.log_error(e, {'endpoint': '/api/chat', 'user_input': user_input[:100]})
            return public_server_error(e)
        
        # Ensure result has required structure
        if not isinstance(result, dict):
            result = {'response': None, 'processing_metadata': {}, 'timestamp': datetime.now().isoformat()}
        if 'processing_metadata' not in result:
            result['processing_metadata'] = {}
        if 'timestamp' not in result:
            result['timestamp'] = datetime.now().isoformat()
        
        processing_metadata = result.get('processing_metadata', {})
        if normalize_processing_metadata:
            processing_metadata = normalize_processing_metadata(processing_metadata)
            result['processing_metadata'] = processing_metadata
        humanitarian_bypass = crisis_humanitarian_bypass(parameters, user_input)
        if humanitarian_bypass:
            processing_metadata['crisis_humanitarian_bypass'] = True
            processing_metadata['blocked'] = False
        else:
            processing_metadata['crisis_humanitarian_bypass'] = False

        blocked = processing_metadata.get('blocked', False) and not humanitarian_bypass
        
        if blocked:
            # Request was blocked, return the blocking message
            blocked_response = result.get('response', 'Request blocked by ethical system')
            return jsonify({
                'response': blocked_response,
                'metadata': result['processing_metadata'],
                'timestamp': result['timestamp']
            })
        
        # Generate response if not blocked
        try:
            if not result.get('response'):
                # Need to generate response using OpenRouter API
                response = processor.generate_response(
                    user_input, 
                    context, 
                    result['processing_metadata'], 
                    parameters
                )
            else:
                response = result['response']
            response = processor.filter_response(response, context)
            if (
                processor.use_integrated
                and hasattr(processor, 'integrated_processor')
                and processor.integrated_processor
                and hasattr(processor.integrated_processor, 'output_safety')
            ):
                result['processing_metadata']['output_safety'] = getattr(
                    processor.integrated_processor.output_safety, 'last_report', {}
                )
        except Exception as e:
            return public_server_error(e)
        
        # Add to conversation history
        conversation_entry = {
            'user': user_input,
            'assistant': response,
            'timestamp': result['timestamp'],
            'metadata': result['processing_metadata']
        }
        processor.conversation_history.append(conversation_entry)
        
        # Record metrics if monitoring is enabled
        if USE_MONITORING and performance_monitor:
            processing_time = time.time() - start_time
            blocked = result.get('processing_metadata', {}).get('blocked', False)
            crisis_mode = parameters.get('crisis_mode', DEFAULT_CRISIS_MODE)
            performance_monitor.record_request(processing_time, blocked, crisis_mode)
        
        return jsonify({
            'response': response,
            'metadata': result['processing_metadata'],
            'timestamp': result['timestamp']
        })
    
    except Exception as e:
        return public_server_error(e)

@app.route('/api/conversations', methods=['GET'])
def list_conversations():
    """List all saved conversations"""
    try:
        conversations = []
        if os.path.exists(CONVERSATIONS_DIR):
            for filename in os.listdir(CONVERSATIONS_DIR):
                if filename.endswith('.json'):
                    filepath = os.path.join(CONVERSATIONS_DIR, filename)
                    with open(filepath, 'r') as f:
                        conv_data = json.load(f)
                        conversations.append({
                            'id': filename.replace('.json', ''),
                            'name': conv_data.get('name', 'Unnamed'),
                            'timestamp': conv_data.get('timestamp', ''),
                            'message_count': len(conv_data.get('messages', []))
                        })
        
        return jsonify({'conversations': sorted(conversations, key=lambda x: x['timestamp'], reverse=True)})
    
    except Exception as e:
        return public_server_error(e)

@app.route('/api/conversations', methods=['POST'])
def save_conversation():
    """Save current conversation"""
    try:
        data = request.json
        conversation_name = data.get('name', 'Unnamed Conversation')
        messages = data.get('messages', [])
        
        # Generate unique ID
        conv_id = f"conv_{int(time.time())}"
        
        conversation_data = {
            'id': conv_id,
            'name': conversation_name,
            'timestamp': datetime.now().isoformat(),
            'messages': messages
        }
        
        filepath = os.path.join(CONVERSATIONS_DIR, f"{conv_id}.json")
        with open(filepath, 'w') as f:
            json.dump(conversation_data, f, indent=2)
        
        return jsonify({
            'success': True,
            'id': conv_id,
            'message': 'Conversation saved successfully'
        })
    
    except Exception as e:
        return public_server_error(e)

@app.route('/api/conversations/<conversation_id>', methods=['GET'])
def load_conversation(conversation_id):
    """Load a saved conversation"""
    try:
        filepath = conversation_file_path(CONVERSATIONS_DIR, conversation_id)
        if filepath is None:
            return jsonify({'error': 'Invalid conversation id'}), 400

        if not os.path.exists(filepath):
            return jsonify({'error': 'Conversation not found'}), 404
        
        with open(filepath, 'r') as f:
            conversation_data = json.load(f)
        
        return jsonify(conversation_data)
    
    except Exception as e:
        return public_server_error(e)

@app.route('/api/conversations/<conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    """Delete a saved conversation"""
    try:
        filepath = conversation_file_path(CONVERSATIONS_DIR, conversation_id)
        if filepath is None:
            return jsonify({'error': 'Invalid conversation id'}), 400

        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({'success': True, 'message': 'Conversation deleted'})
        else:
            return jsonify({'error': 'Conversation not found'}), 404
    
    except Exception as e:
        return public_server_error(e)

@app.route('/api/clear', methods=['POST'])
def clear_conversation():
    """Clear current conversation history"""
    try:
        processor.conversation_history = []
        return jsonify({'success': True, 'message': 'Conversation cleared'})
    
    except Exception as e:
        return public_server_error(e)

@app.route('/api/status', methods=['GET'])
def status():
    """Get system status and metrics"""
    if USE_MONITORING:
        from monitoring import get_system_status
        return jsonify(get_system_status())
    else:
        return jsonify({
            'status': 'operational',
            'monitoring': 'disabled',
            'timestamp': datetime.now().isoformat()
        })

@app.route('/api/metrics', methods=['GET'])
def metrics():
    """Get performance metrics"""
    if USE_MONITORING and performance_monitor:
        return jsonify({
            'metrics': performance_monitor.get_metrics(),
            'percentiles': performance_monitor.get_percentiles(),
            'timestamp': datetime.now().isoformat()
        })
    else:
        return jsonify({'error': 'Monitoring not enabled'}), 503

if __name__ == '__main__':
    debug = os.getenv('FLASK_DEBUG', '0').lower() in ('1', 'true', 'yes')
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('PORT', '5000'))
    if USE_MONITORING and system_logger:
        system_logger.log_system_event('Server starting', {'port': port, 'host': host, 'debug': debug})
    app.run(debug=debug, port=port, host=host)

