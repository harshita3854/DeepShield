import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.nlp_tools import check_grammar

test_text = "Their is a error in this sentence."
print("Checking text:", test_text)
result = check_grammar(test_text)
print("\nResult:")
print("Original:", result.get("original"))
print("Corrected:", result.get("corrected"))
print("Errors found:")
for error in result.get("errors", []):
    print(f" - Error: '{error['error']}' -> Suggestion: '{error['suggestion']}' ({error['message']})")
