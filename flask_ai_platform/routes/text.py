from flask import Blueprint, request, jsonify
from models.nlp_tools import detect_ai_text
from utils.helpers import format_response

text_bp = Blueprint('text_bp', __name__)

@text_bp.route('/detect', methods=['POST'])
def detect():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify(format_response(False, "No text provided")), 400
        
    text = data['text']
    result = detect_ai_text(text)
    
    return jsonify(format_response(True, "Analysis complete", result))
