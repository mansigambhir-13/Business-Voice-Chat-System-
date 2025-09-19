"""
API Integration for Small Calls System
Professional Voice Cloning with snorTTS-Indic-v0
"""

from flask import Flask, request, jsonify, send_file
import io
import base64
import logging
from typing import Dict, Any
import time
import os
import tempfile

# Import your voice cloner (assuming app.py is in same directory)
import sys
sys.path.append('.')
from app import SnorTTSVoiceCloner

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max request

# Initialize voice cloner
voice_cloner = SnorTTSVoiceCloner()
voice_cloner.load_model()

class BusinessCallIntegration:
    """
    Professional API for Small Calls Integration
    80% Quality Target for Client Calls
    """
    
    def __init__(self):
        self.call_history = []
        self.quality_stats = {
            'total_calls': 0,
            'avg_quality': 0.0,
            'success_rate': 0.0
        }
    
    def log_call(self, text: str, quality: float, success: bool):
        """Log call for monitoring and optimization"""
        self.call_history.append({
            'timestamp': time.time(),
            'text': text[:100] + '...' if len(text) > 100 else text,
            'quality': quality,
            'success': success
        })
        
        # Update stats
        self.quality_stats['total_calls'] += 1
        self.quality_stats['avg_quality'] = (
            (self.quality_stats['avg_quality'] * (self.quality_stats['total_calls'] - 1) + quality) 
            / self.quality_stats['total_calls']
        )
        
        success_count = sum(1 for call in self.call_history if call['success'])
        self.quality_stats['success_rate'] = success_count / len(self.call_history)

# Initialize call integration
call_integration = BusinessCallIntegration()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model': 'snorTTS-Indic-v0',
        'quality_target': '80%',
        'stealth_mode': 'active'
    })

@app.route('/api/business-voice', methods=['POST'])
def generate_business_voice():
    """
    Main API endpoint for business voice generation
    
    Request:
    {
        "text": "Hello, this is regarding your account update.",
        "language": "english",  # optional: english, hindi, mixed
        "quality_target": 0.80,  # optional: 0.0-1.0
        "format": "wav"  # optional: wav, mp3
    }
    
    Response:
    {
        "success": true,
        "quality_score": 0.85,
        "audio_base64": "UklGRiQAAABXQVZFZm10...",
        "message": "Voice generated successfully"
    }
    """
    try:
        # Validate request
        if not request.json:
            return jsonify({
                'success': False,
                'error': 'JSON request required'
            }), 400
        
        data = request.json
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({
                'success': False,
                'error': 'Text is required'
            }), 400
        
        if len(text) > 1000:
            return jsonify({
                'success': False,
                'error': 'Text too long (max 1000 characters)'
            }), 400
        
        # Extract parameters
        language = data.get('language', 'english')
        quality_target = data.get('quality_target', 0.80)
        audio_format = data.get('format', 'wav')
        
        logger.info(f"Generating voice for: '{text[:50]}...' in {language}")
        
        # Generate voice
        audio_bytes, quality_score = voice_cloner.generate_voice(text, language)
        
        if not audio_bytes:
            call_integration.log_call(text, 0.0, False)
            return jsonify({
                'success': False,
                'error': 'Voice generation failed'
            }), 500
        
        # Check quality target
        meets_target = quality_score >= quality_target
        
        # Convert audio to base64
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        # Log call
        call_integration.log_call(text, quality_score, meets_target)
        
        # Response
        response = {
            'success': True,
            'quality_score': round(quality_score, 3),
            'meets_target': meets_target,
            'quality_target': quality_target,
            'audio_base64': audio_base64,
            'format': audio_format,
            'language': language,
            'message': 'Voice generated successfully for business call'
        }
        
        if not meets_target:
            response['warning'] = f'Quality {quality_score:.1%} below target {quality_target:.1%}'
        
        logger.info(f"Voice generated successfully: {quality_score:.1%} quality")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Voice generation error: {str(e)}")
        call_integration.log_call(text if 'text' in locals() else '', 0.0, False)
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/api/business-voice/file', methods=['POST'])
def generate_business_voice_file():
    """
    Generate voice and return as audio file
    Same parameters as /api/business-voice but returns audio file directly
    """
    try:
        # Validate request  
        if not request.json:
            return jsonify({'error': 'JSON request required'}), 400
        
        data = request.json
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        language = data.get('language', 'english')
        
        # Generate voice
        audio_bytes, quality_score = voice_cloner.generate_voice(text, language)
        
        if not audio_bytes:
            return jsonify({'error': 'Voice generation failed'}), 500
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_file_path = tmp_file.name
        
        # Log call
        call_integration.log_call(text, quality_score, True)
        
        # Return file
        return send_file(
            tmp_file_path,
            mimetype='audio/wav',
            as_attachment=True,
            download_name=f'business_voice_{int(time.time())}.wav'
        )
        
    except Exception as e:
        logger.error(f"File generation error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/demo-phrases', methods=['GET'])
def get_demo_phrases():
    """Get pre-built business demo phrases"""
    demo_phrases = {
        "account_updates": [
            "Hello, this is regarding your account update.",
            "Your account has been successfully verified and is now active.",
            "We have processed your recent transaction and updated your balance."
        ],
        "service_notifications": [
            "Thank you for choosing our company for your business needs.",
            "We have an important service update to share with you today.", 
            "Your service request has been completed successfully."
        ],
        "follow_up_calls": [
            "I'm calling to follow up on our previous conversation.",
            "We wanted to ensure you're satisfied with our recent service.",
            "Is there anything else we can help you with today?"
        ],
        "professional_greetings": [
            "Good morning, thank you for taking the time to speak with us.",
            "We appreciate your business and continued partnership.",
            "This is a courtesy call to update you on your service status."
        ]
    }
    
    return jsonify({
        'success': True,
        'demo_phrases': demo_phrases,
        'total_categories': len(demo_phrases),
        'total_phrases': sum(len(phrases) for phrases in demo_phrases.values())
    })

@app.route('/api/stats', methods=['GET'])
def get_system_stats():
    """Get system statistics and performance metrics"""
    return jsonify({
        'success': True,
        'model_info': {
            'name': 'snorTTS-Indic-v0',
            'quality_target': '80%',
            'languages': ['english', 'hindi', 'mixed'],
            'stealth_mode': 'active'
        },
        'performance_stats': call_integration.quality_stats,
        'recent_calls': call_integration.call_history[-10:] if call_integration.call_history else []
    })

@app.route('/api/test-phrases', methods=['POST'])
def test_call_quality():
    """
    Test multiple phrases for call quality
    
    Request:
    {
        "phrases": ["Hello, this is...", "Thank you for..."],
        "language": "english",
        "quality_target": 0.80
    }
    """
    try:
        data = request.json
        phrases = data.get('phrases', [])
        language = data.get('language', 'english')
        quality_target = data.get('quality_target', 0.80)
        
        if not phrases:
            return jsonify({'error': 'Phrases list is required'}), 400
        
        results = []
        total_quality = 0
        
        for phrase in phrases:
            audio_bytes, quality_score = voice_cloner.generate_voice(phrase, language)
            
            result = {
                'phrase': phrase[:100] + '...' if len(phrase) > 100 else phrase,
                'quality_score': round(quality_score, 3),
                'meets_target': quality_score >= quality_target,
                'success': audio_bytes is not None
            }
            
            results.append(result)
            if audio_bytes:
                total_quality += quality_score
                call_integration.log_call(phrase, quality_score, True)
        
        avg_quality = total_quality / len([r for r in results if r['success']]) if results else 0
        
        return jsonify({
            'success': True,
            'results': results,
            'summary': {
                'total_phrases': len(phrases),
                'avg_quality': round(avg_quality, 3),
                'phrases_meeting_target': len([r for r in results if r['meets_target']]),
                'success_rate': len([r for r in results if r['success']]) / len(results)
            }
        })
        
    except Exception as e:
        logger.error(f"Batch testing error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'available_endpoints': [
            '/health',
            '/api/business-voice',
            '/api/business-voice/file', 
            '/api/demo-phrases',
            '/api/stats',
            '/api/test-phrases'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # Development server
    app.run(debug=True, host='0.0.0.0', port=5000)
    
    # For production, use:
    # gunicorn -w 4 -b 0.0.0.0:5000 api_integration:app