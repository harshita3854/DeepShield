import random
import time
import language_tool_python

_lt_tool = None

def _get_lt_tool():
    global _lt_tool
    if _lt_tool is None:
        try:
            # First initialization will automatically download LanguageTool server files if not present
            _lt_tool = language_tool_python.LanguageTool('en-US')
        except Exception as e:
            print(f"Error initializing language_tool_python: {e}")
    return _lt_tool

def detect_ai_text(text):
    """
    Dummy logic for AI text detection.
    Can be replaced with HuggingFace/OpenAI models.
    """
    words = text.split()
    if len(words) < 5:
        return {"prediction": "Too short to evaluate", "confidence": 0}
    
    # Simulate processing delay
    time.sleep(1)
    
    is_ai = random.random() > 0.5
    confidence = round(random.uniform(60.0, 99.5), 2)
    
    return {
        "prediction": "AI-Generated" if is_ai else "Human-Written",
        "confidence": confidence
    }

def summarize_text(text):
    """
    Dummy logic for summarizing text.
    """
    if not text.strip():
        return "No text provided to summarize."
        
    time.sleep(1)
    
    sentences = text.split('.')
    if len(sentences) <= 2:
        return text  # Too short
    
    return sentences[0] + ". " + sentences[1] + ". (Summary generated)"

def paraphrase_text(text):
    """
    Dummy logic for paraphrasing text.
    """
    if not text.strip():
        return "No text provided to paraphrase."
        
    time.sleep(1)
    
    return text.replace(" is ", " seems to be ").replace(" very ", " extremely ") + " (Paraphrased version)"

def check_grammar(text):
    """
    Checks grammar and spelling using language-tool-python.
    Falls back to mock logic if the tool is unavailable.
    """
    if not text.strip():
        return {"original": text, "corrected": text, "errors": []}
        
    tool = _get_lt_tool()
    if tool is not None:
        try:
            matches = tool.check(text)
            errors = []
            for m in matches:
                error_text = m.matched_text
                suggestion = m.replacements[0] if m.replacements else ""
                errors.append({
                    "error": error_text,
                    "suggestion": suggestion,
                    "message": m.message
                })
            
            corrected = tool.correct(text)
            return {
                "original": text,
                "corrected": corrected,
                "errors": errors
            }
        except Exception as e:
            print(f"Error running language_tool_python: {e}")
            
    # --- Fallback Mock Logic ---
    time.sleep(1)
    errors = []
    if "their is" in text.lower():
        errors.append({"error": "their is", "suggestion": "there is", "message": "Possible spelling mistake"})
    
    return {
        "original": text,
        "corrected": text.replace("their", "there"),  # basic mock
        "errors": errors
    }
