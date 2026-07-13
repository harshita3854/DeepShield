import os
import random
import cv2
import numpy as np

# Try loading TensorFlow, similarly to existing Django code
try:
    import tensorflow as tf
    # Assume model is stored in models_store at the root space
    # (Since we are in flask_ai_platform/models, base_dir is flask_ai_platform)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Try root models_store first (parent directory), then fallback to local models_store
    model_path = os.path.join(os.path.dirname(base_dir), 'models_store', 'deepfake_detector_model.h5')
    if not os.path.exists(model_path):
        model_path = os.path.join(base_dir, 'models_store', 'deepfake_detector_model.h5')
    
    if os.path.exists(model_path):
        MODEL = tf.keras.models.load_model(model_path)
    else:
        MODEL = None
except ImportError:
    MODEL = None

def preprocess_image(image_path):
    """
    Reads the image using OpenCV, resizes to 224x224, and normalizes it.
    Returns expanding dimensions to match CNN input (1, 224, 224, 3)
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read image with OpenCV")
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=0) # Add batch dimension: (1, 224, 224, 3)
    return img

def predict_image(image_path):
    """
    Predicts if the image is Real or AI-Generated using the trained CNN.
    Returns: (Prediction_String, Confidence_Percentage)
    """
    if MODEL:
        try:
            processed_img = preprocess_image(image_path)
            prediction_prob = MODEL.predict(processed_img)[0][0]
            
            # Since sigmoid was used, typically > 0.5 is Class 1 (e.g. Fake)
            # Assuming Class 0: Real, Class 1: Fake
            if prediction_prob > 0.5:
                confidence = round(prediction_prob * 100, 2)
                return 'AI-Generated', confidence
            else:
                confidence = round((1 - prediction_prob) * 100, 2)
                return 'Real', confidence
                
        except Exception as e:
            print(f"Error during prediction: {e}")
            pass # Fallback to mock

    # --- MOCK LOGIC: Used if model doesn't exist yet ---
    print(f"** Using Mock Prediction for: {os.path.basename(image_path)} (TensorFlow model not found) **")
    is_fake = random.choice([True, False])
    confidence = round(random.uniform(70.0, 99.9), 2)
    
    if is_fake:
        prediction = 'AI-Generated'
    else:
        prediction = 'Real'
        
    return prediction, confidence
