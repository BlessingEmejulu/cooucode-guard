import pytest
from analysis_engine.python_analyzer import PythonAnalyzer
from analysis_engine.java_analyzer import JavaAnalyzer
from analysis_engine.cpp_analyzer import CppAnalyzer
from analysis_engine.ast_similarity import ASTSimilarity
from analysis_engine.similarity import SimilarityEngine
from analysis_engine.tree_matching import TreeMatcher

def test_python_ast_extraction():
    code = """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
"""
    result = PythonAnalyzer.extract_structure(code)
    assert result["success"] is True
    assert result["structural_features"]["functions"] == 1
    assert result["structural_features"]["loops"] == 2
    assert result["structural_features"]["conditionals"] == 1
    assert len(result["node_sequence"]) > 5

def test_java_analyzer():
    java_code = """
public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }
    public int multiply(int a, int b) {
        int result = 0;
        for (int i = 0; i < b; i++) {
            result += a;
        }
        return result;
    }
}
"""
    result = JavaAnalyzer.extract_structure(java_code)
    assert result["success"] is True
    assert result["structural_features"]["classes"] >= 1
    assert result["structural_features"]["functions"] >= 1

def test_cpp_analyzer():
    cpp_code = """
#include <iostream>
#include <vector>

class VectorMath {
public:
    int sum(const std::vector<int>& v) {
        int total = 0;
        for (int x : v) {
            total += x;
        }
        return total;
    }
};
"""
    result = CppAnalyzer.extract_structure(cpp_code)
    assert result["success"] is True
    assert result["structural_features"]["classes"] >= 1

def test_ast_similarity_identical_logic():
    code_a = """
def calculate_factorial(n):
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
"""
    # Renamed variables and slight spacing changes
    code_b = """
def compute_fact(num):
    if num <= 1:
        return 1
    ans = 1
    for count in range(2, num + 1):
        ans = ans * count
    return ans
"""
    score, details = ASTSimilarity.compute_ast_similarity(code_a, code_b, "python")
    assert score >= 75.0, f"Expected high AST similarity for identical structural logic, got {score}"

def test_matching_blocks_detection():
    code_a = """
def step_one():
    x = 10
    y = 20
    return x + y

def step_two():
    print("finished")
"""
    code_b = """
def other():
    pass

def step_one():
    x = 10
    y = 20
    return x + y
"""
    blocks = TreeMatcher.find_matching_blocks(code_a, code_b, "python", min_block_lines=2)
    assert len(blocks) >= 1
    assert blocks[0]["similarity"] >= 75.0
