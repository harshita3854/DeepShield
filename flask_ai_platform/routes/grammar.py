from flask import Blueprint, request, jsonify
from models.nlp_tools import check_grammar
from utils.helpers import format_response

grammar_bp = Blueprint('grammar_bp', __name__)

@grammar_bp.route('/', methods=['POST'])
def grammar():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify(format_response(False, "No text provided")), 400
        
    text = data['text']
    result = check_grammar(text)
    
    return jsonify(format_response(True, "Grammar check complete", result))
