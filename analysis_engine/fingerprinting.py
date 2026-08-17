import hashlib
from typing import List, Tuple, Set, Dict, Any
from analysis_engine.tokenizer import Tokenizer

class Fingerprinter:
    """
    Implements the Winnowing algorithm for robust source code fingerprinting.
    Selects minimum hash values over sliding windows of k-grams.
    """

    DEFAULT_K = 12 # k-gram length
    DEFAULT_WINDOW = 8 # window size

    @classmethod
    def hash_kgram(cls, kgram: str) -> int:
        """Generates a 64-bit integer hash from a k-gram string."""
        return int(hashlib.md5(kgram.encode('utf-8')).hexdigest()[:16], 16)

    @classmethod
    def generate_fingerprints(
        cls,
        source_code: str,
        language: str,
        k: int = DEFAULT_K,
        window_size: int = DEFAULT_WINDOW
    ) -> List[Tuple[int, int]]:
        """
        Extracts fingerprints as a list of (hash_value, token_position) tuples.
        """
        tokens = Tokenizer.tokenize(source_code, language, normalize_identifiers=True)
        if len(tokens) < k:
            # If too short, hash the entire token sequence as a single fingerprint
            if tokens:
                return [(cls.hash_kgram(" ".join(tokens)), 0)]
            return []

        # 1. Generate k-grams and their hashes
        kgram_hashes: List[Tuple[int, int]] = []
        for i in range(len(tokens) - k + 1):
            kgram_str = " ".join(tokens[i : i + k])
            h = cls.hash_kgram(kgram_str)
            kgram_hashes.append((h, i))

        if len(kgram_hashes) < window_size:
            # If fewer k-grams than window size, take the minimum
            min_h = min(kgram_hashes, key=lambda x: (x[0], -x[1]))
            return [min_h]

        # 2. Winnowing algorithm over sliding windows
        fingerprints: List[Tuple[int, int]] = []
        min_pos = -1

        for i in range(len(kgram_hashes) - window_size + 1):
            window = kgram_hashes[i : i + window_size]
            # Select rightmost minimum to break ties deterministically
            current_min = min(window, key=lambda x: (x[0], -x[1]))
            if current_min[1] != min_pos:
                fingerprints.append(current_min)
                min_pos = current_min[1]

        return fingerprints

    @classmethod
    def compute_fingerprint_similarity(
        cls,
        source_a: str,
        source_b: str,
        language: str,
        k: int = DEFAULT_K,
        window_size: int = DEFAULT_WINDOW
    ) -> Tuple[float, Set[int]]:
        """
        Calculates Jaccard similarity between the fingerprint sets of two source files.
        Returns (similarity_score [0..100], shared_hashes).
        """
        fps_a = cls.generate_fingerprints(source_a, language, k, window_size)
        fps_b = cls.generate_fingerprints(source_b, language, k, window_size)

        hashes_a = {fp[0] for fp in fps_a}
        hashes_b = {fp[0] for fp in fps_b}

        if not hashes_a and not hashes_b:
            return 100.0 if not source_a.strip() and not source_b.strip() else 0.0, set()
        if not hashes_a or not hashes_b:
            return 0.0, set()

        intersection = hashes_a.intersection(hashes_b)
        union = hashes_a.union(hashes_b)

        # Jaccard index
        jaccard = len(intersection) / len(union) if union else 0.0

        # Also compute containment (max of intersection / len(A) and intersection / len(B))
        containment_a = len(intersection) / len(hashes_a) if hashes_a else 0.0
        containment_b = len(intersection) / len(hashes_b) if hashes_b else 0.0
        containment_score = max(containment_a, containment_b)

        # Harmonic/weighted blend between Jaccard and containment
        final_score = round((0.6 * jaccard + 0.4 * containment_score) * 100.0, 2)
        return min(100.0, max(0.0, final_score)), intersection
