import re
from typing import Dict, Any, List

class AIPatternDetector:
    """
    Analyzes source code for heuristic markers indicative of AI-generated or AI-assisted programming code.
    
    Disclaimer: AI pattern detection is a heuristic indicator and must not be considered
    as definitive proof that AI was used.
    """

    GENERIC_AI_COMMENT_PATTERNS = [
        r'\bstep\s*\d+[:\-]',
        r'\bhelper\s*function\b',
        r'\binitialize\s*(variables?|data|list|array|map|counter)\b',
        r'\bloop\s*through\b',
        r'\biterate\s*over\b',
        r'\bcheck\s*if\s*(the\s*)?(input|value|list|condition)\s*is\b',
        r'\bhandle\s*(edge\s*cases?|base\s*cases?|errors?)\b',
        r'\bbase\s*case\b',
        r'\breturn\s*the\s*(final\s*)?(result|output|value|answer|sum)\b',
        r'\btime\s*complexity\b',
        r'\bspace\s*complexity\b',
        r'\bexample\s*usage\b',
        r'\bdriver\s*(code|program)\b',
        r'\btest\s*cases?\b',
        r'\bcreate\s*an\s*instance\s*of\b',
        r'\bmain\s*execution\b',
        r'\bcalculate\s*the\b',
        r'\bfunction\s*to\s*(calculate|compute|find|determine|check|validate|sort|search)\b'
    ]

    AI_DOCSTRING_PATTERNS = [
        r':param\s+\w+:',
        r':return:',
        r'@param\s+\w+',
        r'@return',
        r'Args:\s*\n',
        r'Returns:\s*\n',
        r'Raises:\s*\n',
        r'Parameters\n\s*---',
        r'Returns\n\s*---'
    ]

    @classmethod
    def analyze(cls, source_code: str, language: str) -> Dict[str, Any]:
        if not source_code.strip():
            return {
                "ai_pattern_score": 0.0,
                "classification": "Low indication",
                "indicators": [],
                "details": {
                    "generic_comments_count": 0,
                    "docstring_density": 0,
                    "naming_uniformity": 0,
                    "boilerplate_score": 0
                },
                "disclaimer": "AI pattern detection provides heuristic indicators for lecturer review only and does not provide definitive proof."
            }

        lines = source_code.splitlines()
        total_lines = len(lines)
        indicators: List[str] = []
        score_components = []

        # 1. Heuristic: Generic AI-Style Explanatory Comments
        comment_lines = []
        full_comments_text = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith(('#', '//', '/*', '*')):
                comment_lines.append(stripped)
                full_comments_text.append(stripped.lower())

        comment_count = len(comment_lines)
        comment_ratio = comment_count / max(1, total_lines)
        
        generic_comment_matches = 0
        all_comments_str = " ".join(full_comments_text)
        for pattern in cls.GENERIC_AI_COMMENT_PATTERNS:
            found = re.findall(pattern, all_comments_str, flags=re.IGNORECASE)
            generic_comment_matches += len(found)

        if generic_comment_matches >= 3:
            score_components.append(30.0)
            indicators.append(f"Frequent generic step-by-step explanatory comments ({generic_comment_matches} markers detected)")
        elif generic_comment_matches >= 1:
            score_components.append(15.0)
            indicators.append("Contains common AI-style step/initialization comments")
        else:
            score_components.append(0.0)

        # 2. Heuristic: Verbose Standardized Docstrings in Academic Code
        docstring_matches = 0
        for pattern in cls.AI_DOCSTRING_PATTERNS:
            if re.search(pattern, source_code, flags=re.IGNORECASE):
                docstring_matches += 1

        if docstring_matches >= 2:
            score_components.append(25.0)
            indicators.append("Highly standardized structured docstring format (Args/Returns/Param annotations)")
        elif docstring_matches == 1:
            score_components.append(12.0)
            indicators.append("Formal API docstring structure present")
        else:
            score_components.append(0.0)

        # 3. Heuristic: Extreme Comment-to-Code Density (> 35% comments with high regularity)
        if comment_ratio > 0.35 and total_lines > 15:
            score_components.append(20.0)
            indicators.append(f"Unusually high comment-to-code density ({round(comment_ratio * 100, 1)}%)")
        elif comment_ratio > 0.20:
            score_components.append(10.0)
        else:
            score_components.append(0.0)

        # 4. Heuristic: Overly Descriptive Descriptive Identifier Naming Patterns
        identifier_pattern = re.compile(r'\b[a-z]+(?:_[a-z]+){3,}\b|\b[a-z]+(?:[A-Z][a-z]+){3,}\b')
        long_identifiers = identifier_pattern.findall(source_code)
        if len(long_identifiers) >= 4:
            score_components.append(15.0)
            indicators.append("High prevalence of overly verbose, ultra-descriptive variable/function identifiers")
        elif len(long_identifiers) >= 2:
            score_components.append(8.0)
        else:
            score_components.append(0.0)

        # 5. Heuristic: Perfect Example Driver / Complexity Footer
        has_complexity_note = bool(re.search(r'(time\s*complexity|space\s*complexity|o\(n|o\(1|o\(log)', all_comments_str, re.IGNORECASE))
        has_example_driver = bool(re.search(r'(#\s*example\s*usage|//\s*example\s*usage|if\s*__name__\s*==\s*[\'"]__main__[\'"])', source_code, re.IGNORECASE))

        if has_complexity_note and has_example_driver:
            score_components.append(15.0)
            indicators.append("Includes formal algorithmic complexity annotation and clean turnkey driver harness")
        elif has_complexity_note:
            score_components.append(10.0)
            indicators.append("Includes formal asymptotic complexity annotation in comments")
        else:
            score_components.append(0.0)

        # Aggregate heuristic score (0 - 100)
        total_score = sum(score_components)
        final_score = min(100.0, max(0.0, round(total_score, 1)))

        if final_score >= 60.0:
            classification = "High indication"
        elif final_score >= 30.0:
            classification = "Moderate indication"
        else:
            classification = "Low indication"

        if not indicators:
            indicators.append("Standard human coding structure and idiom distribution")

        return {
            "ai_pattern_score": final_score,
            "classification": classification,
            "indicators": indicators,
            "details": {
                "generic_comments_count": generic_comment_matches,
                "docstring_annotations": docstring_matches,
                "comment_ratio_pct": round(comment_ratio * 100, 1),
                "verbose_identifiers": len(long_identifiers),
                "has_complexity_annotation": has_complexity_note
            },
            "disclaimer": "AI pattern detection provides heuristic indicators for lecturer review only and does not provide definitive proof that AI was used."
        }
