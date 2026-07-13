from flask import Blueprint, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
from models.image_detector import predict_image
from utils.helpers import format_response, allowed_file

image_bp = Blueprint('image_bp', __name__)

@image_bp.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify(format_response(False, "No image file provided")), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify(format_response(False, "No selected file")), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Call AI model
        try:
            prediction, confidence = predict_image(filepath)
            
            # Clean up the file after prediction if you want to avoid saving forever
            # os.remove(filepath)
            
            return jsonify(format_response(True, "Analysis complete", {
                "prediction": prediction,
                "confidence": confidence
            }))
        except Exception as e:
            return jsonify(format_response(False, f"Error processing image: {str(e)}")), 500
            
    return jsonify(format_response(False, "Invalid file format")), 400
