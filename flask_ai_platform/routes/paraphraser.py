from flask import Blueprint, request, jsonify
from models.nlp_tools import paraphrase_text
from utils.helpers import format_response

paraphraser_bp = Blueprint('paraphraser_bp', __name__)

@paraphraser_bp.route('/', methods=['POST'])
def paraphrase():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify(format_response(False, "No text provided")), 400
        
    text = data['text']
    result = paraphrase_text(text)
    
    return jsonify(format_response(True, "Paraphrasing complete", {"paraphrased": result}))
