from flask import Blueprint, request, jsonify
from models.nlp_tools import summarize_text
from utils.helpers import format_response

summarizer_bp = Blueprint('summarizer_bp', __name__)

@summarizer_bp.route('/', methods=['POST'])
def summarize():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify(format_response(False, "No text provided")), 400
        
    text = data['text']
    result = summarize_text(text)
    
    return jsonify(format_response(True, "Summarization complete", {"summary": result}))
