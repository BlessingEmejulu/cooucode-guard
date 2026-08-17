import re
from typing import List, Dict, Any

class CppAnalyzer:
    """
    Analyzes C++ source code.
    Extracts structural AST tokens, grammar signatures, and functional blocks.
    """

    @classmethod
    def extract_structure(cls, source_code: str) -> Dict[str, Any]:
        """
        Extracts structural features, normalized AST tokens, and blocks for C++ code.
        """
        from analysis_engine.tokenizer import Tokenizer

        lines = source_code.splitlines()
        node_sequence: List[str] = []
        blocks: List[Dict[str, Any]] = []
        features = {
            "functions": 0,
            "classes": 0,
            "loops": 0,
            "conditionals": 0,
            "function_calls": 0,
            "variables": 0,
            "returns": 0,
            "try_blocks": 0,
            "templates": 0,
            "max_depth": 0
        }
        function_names: List[str] = []

        class_pattern = re.compile(r'\b(class|struct)\s+([a-zA-Z_]\w*)')
        function_pattern = re.compile(
            r'\b(?:inline|virtual|static|constexpr|const|void|int|double|float|char|auto|bool|long|short|unsigned|std::\w+|\w+(?:<[^>]+>)?)\s+([a-zA-Z_]\w*)\s*\([^)]*\)\s*(?:const)?\s*\{'
        )
        loop_pattern = re.compile(r'\b(for|while|do)\b')
        if_pattern = re.compile(r'\b(if|switch)\b')
        try_pattern = re.compile(r'\b(try|catch)\b')
        return_pattern = re.compile(r'\breturn\b')
        template_pattern = re.compile(r'\btemplate\s*<')
        call_pattern = re.compile(r'\b([a-zA-Z_]\w*)\s*\(')

        current_depth = 0
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('#'):
                continue

            open_braces = line.count('{')
            close_braces = line.count('}')
            current_depth = max(0, current_depth + open_braces - close_braces)
            if current_depth > features["max_depth"]:
                features["max_depth"] = current_depth

            if template_pattern.search(line):
                features["templates"] += 1
                node_sequence.append("TemplateDeclaration")

            c_match = class_pattern.search(line)
            if c_match:
                features["classes"] += 1
                node_sequence.append("ClassSpecifier")
                blocks.append({
                    "type": "class",
                    "name": c_match.group(2),
                    "start_line": i,
                    "end_line": min(len(lines), i + 25)
                })

            f_match = function_pattern.search(line)
            if f_match:
                fname = f_match.group(1)
                if fname not in {'if', 'for', 'while', 'switch', 'catch', 'main', 'template'}:
                    features["functions"] += 1
                    function_names.append(fname)
                    node_sequence.append("FunctionDefinition")
                    blocks.append({
                        "type": "function",
                        "name": fname,
                        "start_line": i,
                        "end_line": min(len(lines), i + 15)
                    })

            if loop_pattern.search(line):
                features["loops"] += 1
                node_sequence.append("IterationStatement")

            if if_pattern.search(line):
                features["conditionals"] += 1
                node_sequence.append("SelectionStatement")

            if try_pattern.search(line):
                features["try_blocks"] += 1
                node_sequence.append("TryBlock")

            if return_pattern.search(line):
                features["returns"] += 1
                node_sequence.append("JumpStatement")

            calls = call_pattern.findall(line)
            for call in calls:
                if call not in {'if', 'for', 'while', 'switch', 'catch', 'sizeof', 'main'}:
                    features["function_calls"] += 1
                    node_sequence.append("CallExpression")

        tokens = Tokenizer.tokenize(source_code, "cpp", normalize_identifiers=True)
        if len(node_sequence) < 5:
            node_sequence.extend(tokens)

        return {
            "success": True,
            "error": None,
            "node_sequence": node_sequence,
            "structural_features": features,
            "blocks": blocks,
            "function_names": function_names
        }
