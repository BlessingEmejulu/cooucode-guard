import pytest
from analysis_engine.tokenizer import Tokenizer
from analysis_engine.fingerprinting import Fingerprinter
from analysis_engine.ai_pattern_detector import AIPatternDetector

def test_tokenizer_normalization():
    py_code = """
# Test comment
def compute(value_one, value_two):
    result = value_one + value_two
    return result
"""
    tokens = Tokenizer.tokenize(py_code, "python", normalize_identifiers=True)
    assert "KW_DEF" in tokens
    assert "KW_RETURN" in tokens
    assert any(t.startswith("ID_") for t in tokens)

def test_winnowing_fingerprinting():
    code_a = """
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
"""
    code_b = """
def search_items(items, key):
    for idx in range(len(items)):
        if items[idx] == key:
            return idx
    return -1
"""
    fps_a = Fingerprinter.generate_fingerprints(code_a, "python", k=6, window_size=4)
    fps_b = Fingerprinter.generate_fingerprints(code_b, "python", k=6, window_size=4)
    assert len(fps_a) > 0
    assert len(fps_b) > 0

    score, shared = Fingerprinter.compute_fingerprint_similarity(code_a, code_b, "python", k=6, window_size=4)
    assert score >= 70.0, f"Expected high fingerprint similarity, got {score}"

def test_ai_pattern_detector():
    ai_sample = """
\"\"\"
Module: Binary Search Implementation
\"\"\"

def binary_search(arr, target):
    \"\"\"
    Performs binary search on a sorted array.
    :param arr: List of integers
    :param target: Integer to locate
    :return: Index or -1
    \"\"\"
    # Step 1: Initialize pointer variables
    left_pointer_index = 0
    right_pointer_index = len(arr) - 1
    
    # Step 2: Loop through until pointers cross
    while left_pointer_index <= right_pointer_index:
        mid_point_index = (left_pointer_index + right_pointer_index) // 2
        
        # Check if target is found
        if arr[mid_point_index] == target:
            # Return the final result
            return mid_point_index
        elif arr[mid_point_index] < target:
            left_pointer_index = mid_point_index + 1
        else:
            right_pointer_index = mid_point_index - 1
            
    # Return -1 when not found
    return -1

# Example usage driver code
if __name__ == "__main__":
    test_array = [1, 3, 5, 7, 9]
    print(binary_search(test_array, 5))
"""
    result = AIPatternDetector.analyze(ai_sample, "python")
    assert result["ai_pattern_score"] >= 50.0
    assert len(result["indicators"]) >= 2
    assert "disclaimer" in result
