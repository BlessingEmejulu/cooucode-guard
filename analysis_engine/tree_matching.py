import difflib
import re
from typing import List, Dict, Any, Tuple
from analysis_engine.tokenizer import Tokenizer

class TreeMatcher:
    """
    Identifies matching code blocks, aligned functions, and line-level overlaps
    between two source code files.
    """

    @classmethod
    def normalize_line_for_matching(cls, line: str) -> str:
        """Normalizes a single code line by removing comments and extra spaces."""
        cleaned = re.sub(r'#.*$', '', line)
        cleaned = re.sub(r'//.*$', '', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned

    @classmethod
    def find_matching_blocks(
        cls,
        source_a: str,
        source_b: str,
        language: str,
        min_block_lines: int = 2
    ) -> List[Dict[str, Any]]:
        """
        Locates exact and normalized matching blocks between two source files.
        Returns a list of dictionaries with line ranges and similarity metrics:
        [{'start_a': int, 'end_a': int, 'start_b': int, 'end_b': int, 'similarity': float, 'block_type': str, 'description': str}]
        """
        lines_a = source_a.splitlines()
        lines_b = source_b.splitlines()

        norm_a = [cls.normalize_line_for_matching(l) for l in lines_a]
        norm_b = [cls.normalize_line_for_matching(l) for l in lines_b]

        # Use SequenceMatcher on normalized non-empty lines
        matcher = difflib.SequenceMatcher(None, norm_a, norm_b)
        matching_blocks: List[Dict[str, Any]] = []

        for block in matcher.get_matching_blocks():
            a_idx, b_idx, size = block.a, block.b, block.size
            if size < min_block_lines:
                continue

            # Calculate density of non-empty matched lines
            matched_content_a = [lines_a[a_idx + i] for i in range(size) if norm_a[a_idx + i]]
            if len(matched_content_a) < min_block_lines:
                continue

            start_a = a_idx + 1
            end_a = a_idx + size
            start_b = b_idx + 1
            end_b = b_idx + size

            # Calculate token similarity of the block
            sub_code_a = "\n".join(lines_a[a_idx : a_idx + size])
            sub_code_b = "\n".join(lines_b[b_idx : b_idx + size])

            toks_a = Tokenizer.tokenize(sub_code_a, language, normalize_identifiers=True)
            toks_b = Tokenizer.tokenize(sub_code_b, language, normalize_identifiers=True)

            intersection = len(set(toks_a).intersection(set(toks_b)))
            union = len(set(toks_a).union(set(toks_b))) if (toks_a or toks_b) else 1
            block_sim = round((intersection / union) * 100.0, 2) if union else 100.0

            # Determine type of matching block
            if sub_code_a.strip() == sub_code_b.strip():
                b_type = "Exact Match"
                desc = f"Identical code segment ({size} lines)"
            elif "def " in sub_code_a or "class " in sub_code_a or "public " in sub_code_a:
                b_type = "Structural Construct"
                desc = f"Matching function / class construct ({size} lines)"
            else:
                b_type = "Normalized Logic"
                desc = f"Similar statement flow / algorithm ({size} lines)"

            matching_blocks.append({
                "start_a": start_a,
                "end_a": end_a,
                "start_b": start_b,
                "end_b": end_b,
                "size": size,
                "similarity": max(block_sim, 75.0), # Blocks that aligned cleanly have high confidence
                "block_type": b_type,
                "description": desc,
                "snippet_a": sub_code_a[:200] + ("..." if len(sub_code_a) > 200 else ""),
                "snippet_b": sub_code_b[:200] + ("..." if len(sub_code_b) > 200 else "")
            })

        # Sort blocks by size descending
        matching_blocks.sort(key=lambda x: x["size"], reverse=True)
        return matching_blocks

    @classmethod
    def get_annotated_lines(
        cls,
        source_code: str,
        matching_ranges: List[Tuple[int, int]] # List of (start_line, end_line) 1-indexed
    ) -> List[Dict[str, Any]]:
        """Annotates each line of code with whether it is part of a match."""
        lines = source_code.splitlines()
        annotated = []

        for line_num, text in enumerate(lines, 1):
            is_matched = any(start <= line_num <= end for start, end in matching_ranges)
            annotated.append({
                "line_number": line_num,
                "text": text,
                "is_matched": is_matched
            })

        return annotated
