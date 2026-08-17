import math
from typing import List, Dict, Any, Tuple
from analysis_engine.python_analyzer import PythonAnalyzer
from analysis_engine.java_analyzer import JavaAnalyzer
from analysis_engine.cpp_analyzer import CppAnalyzer

class ASTSimilarity:
    """
    Computes structural AST similarity between two source code files.
    Combines:
    1. AST Node Sequence Longest Common Subsequence (LCS) similarity.
    2. AST Structural Feature Vector Cosine similarity.
    3. AST Subtree/Block topological similarity.
    """

    @classmethod
    def analyze_source(cls, source_code: str, language: str) -> Dict[str, Any]:
        lang = (language or "").lower()
        if "python" in lang:
            return PythonAnalyzer.extract_structure(source_code)
        elif "java" in lang:
            return JavaAnalyzer.extract_structure(source_code)
        elif "c++" in lang or "cpp" in lang or "c" in lang:
            return CppAnalyzer.extract_structure(source_code)
        else:
            return PythonAnalyzer.extract_structure(source_code)

    @classmethod
    def compute_lcs_similarity(cls, seq1: List[str], seq2: List[str]) -> float:
        """Computes normalized Longest Common Subsequence ratio between two sequences."""
        if not seq1 or not seq2:
            return 100.0 if not seq1 and not seq2 else 0.0

        # Memory-optimized LCS for sequences
        len1, len2 = len(seq1), len(seq2)
        dp = [0] * (len2 + 1)

        for item1 in seq1:
            prev = 0
            for j in range(1, len2 + 1):
                temp = dp[j]
                if item1 == seq2[j - 1]:
                    dp[j] = prev + 1
                else:
                    dp[j] = max(dp[j], dp[j - 1])
                prev = temp

        lcs_len = dp[len2]
        return round((2.0 * lcs_len / (len1 + len2)) * 100.0, 2)

    @classmethod
    def compute_feature_cosine_similarity(cls, f1: Dict[str, Any], f2: Dict[str, Any]) -> float:
        """Calculates cosine similarity between structural feature vectors."""
        all_keys = set(f1.keys()).union(set(f2.keys()))
        vec1 = [f1.get(k, 0) for k in all_keys if isinstance(f1.get(k, 0), (int, float))]
        vec2 = [f2.get(k, 0) for k in all_keys if isinstance(f2.get(k, 0), (int, float))]

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))

        if norm1 == 0 and norm2 == 0:
            return 100.0
        if norm1 == 0 or norm2 == 0:
            return 0.0

        cosine = dot_product / (norm1 * norm2)
        return round(min(1.0, max(0.0, cosine)) * 100.0, 2)

    @classmethod
    def compute_ast_similarity(
        cls,
        source_a: str,
        source_b: str,
        language: str
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Calculates composite AST similarity score and returns details.
        """
        struct_a = cls.analyze_source(source_a, language)
        struct_b = cls.analyze_source(source_b, language)

        seq_a = struct_a.get("node_sequence", [])
        seq_b = struct_b.get("node_sequence", [])
        lcs_score = cls.compute_lcs_similarity(seq_a, seq_b)

        feat_a = struct_a.get("structural_features", {})
        feat_b = struct_b.get("structural_features", {})
        cosine_score = cls.compute_feature_cosine_similarity(feat_a, feat_b)

        # Composite AST Score: 60% LCS on node sequence + 40% Structural Cosine
        ast_composite = round(0.60 * lcs_score + 0.40 * cosine_score, 2)
        ast_composite = min(100.0, max(0.0, ast_composite))

        details = {
            "lcs_score": lcs_score,
            "cosine_score": cosine_score,
            "features_a": feat_a,
            "features_b": feat_b,
            "blocks_a": struct_a.get("blocks", []),
            "blocks_b": struct_b.get("blocks", [])
        }

        return ast_composite, details
