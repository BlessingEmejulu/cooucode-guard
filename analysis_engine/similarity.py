import difflib
from typing import Dict, Any, Tuple, List
from analysis_engine.tokenizer import Tokenizer
from analysis_engine.fingerprinting import Fingerprinter
from analysis_engine.ast_similarity import ASTSimilarity
from analysis_engine.tree_matching import TreeMatcher
from analysis_engine.ai_pattern_detector import AIPatternDetector

class SimilarityEngine:
    """
    Weighted multi-layered similarity engine for source code plagiarism detection.
    Aggregates AST Structural (45%), Token (25%), Fingerprint (20%), and Normalized Text (10%).
    """

    WEIGHT_AST = 0.45
    WEIGHT_TOKEN = 0.25
    WEIGHT_FINGERPRINT = 0.20
    WEIGHT_NORMALIZED_TEXT = 0.10

    @classmethod
    def calculate_token_similarity(cls, source_a: str, source_b: str, language: str) -> float:
        """Calculates Jaccard and LCS similarity over normalized token streams."""
        toks_a = Tokenizer.tokenize(source_a, language, normalize_identifiers=True)
        toks_b = Tokenizer.tokenize(source_b, language, normalize_identifiers=True)

        if not toks_a and not toks_b:
            return 100.0 if not source_a.strip() and not source_b.strip() else 0.0
        if not toks_a or not toks_b:
            return 0.0

        # Token Jaccard
        set_a = set(toks_a)
        set_b = set(toks_b)
        jaccard = len(set_a.intersection(set_b)) / len(set_a.union(set_b)) if (set_a or set_b) else 1.0

        # Token Sequence Matcher Ratio
        matcher = difflib.SequenceMatcher(None, toks_a, toks_b)
        seq_ratio = matcher.ratio()

        # Combined Token Score
        score = (0.5 * jaccard + 0.5 * seq_ratio) * 100.0
        return round(min(100.0, max(0.0, score)), 2)

    @classmethod
    def calculate_normalized_text_similarity(cls, source_a: str, source_b: str, language: str) -> float:
        """Calculates similarity on comment-stripped and whitespace-normalized source."""
        clean_a = Tokenizer.normalize_whitespace(Tokenizer.strip_comments_and_docstrings(source_a, language))
        clean_b = Tokenizer.normalize_whitespace(Tokenizer.strip_comments_and_docstrings(source_b, language))

        if not clean_a and not clean_b:
            return 100.0
        if not clean_a or not clean_b:
            return 0.0

        matcher = difflib.SequenceMatcher(None, clean_a.splitlines(), clean_b.splitlines())
        return round(matcher.ratio() * 100.0, 2)

    @classmethod
    def classify_risk(cls, score: float) -> str:
        """Classifies similarity score into standardized risk levels."""
        if score >= 80.0:
            return "Critical"
        elif score >= 60.0:
            return "High"
        elif score >= 30.0:
            return "Moderate"
        else:
            return "Low"

    @classmethod
    def compare_pair(
        cls,
        source_a: str,
        source_b: str,
        language: str
    ) -> Dict[str, Any]:
        """
        Executes complete multi-dimensional comparison between two code submissions.
        """
        # 1. AST Similarity
        ast_sim, ast_details = ASTSimilarity.compute_ast_similarity(source_a, source_b, language)

        # 2. Token Similarity
        token_sim = cls.calculate_token_similarity(source_a, source_b, language)

        # 3. Fingerprint Similarity (Winnowing)
        fingerprint_sim, shared_hashes = Fingerprinter.compute_fingerprint_similarity(source_a, source_b, language)

        # 4. Normalized Text Similarity
        norm_sim = cls.calculate_normalized_text_similarity(source_a, source_b, language)

        # 5. Weighted Overall Similarity
        overall_score = round(
            (cls.WEIGHT_AST * ast_sim) +
            (cls.WEIGHT_TOKEN * token_sim) +
            (cls.WEIGHT_FINGERPRINT * fingerprint_sim) +
            (cls.WEIGHT_NORMALIZED_TEXT * norm_sim),
            2
        )
        overall_score = min(100.0, max(0.0, overall_score))

        # 6. Matching Blocks
        matching_blocks = TreeMatcher.find_matching_blocks(source_a, source_b, language)

        return {
            "overall_similarity": overall_score,
            "ast_similarity": ast_sim,
            "token_similarity": token_sim,
            "fingerprint_similarity": fingerprint_sim,
            "normalized_similarity": norm_sim,
            "risk_level": cls.classify_risk(overall_score),
            "shared_fingerprints_count": len(shared_hashes),
            "matching_blocks": matching_blocks,
            "ast_details": ast_details
        }
