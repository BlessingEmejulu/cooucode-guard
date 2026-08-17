import re
from typing import List, Dict, Any, Tuple

try:
    import javalang
    JAVALANG_AVAILABLE = True
except ImportError:
    JAVALANG_AVAILABLE = False

class JavaAnalyzer:
    """
    Analyzes Java source code using `javalang` when available,
    with a resilient structural grammar parser fallback.
    """

    @classmethod
    def extract_structure(cls, source_code: str) -> Dict[str, Any]:
        """
        Extracts structural features, AST node sequences, and structural blocks from Java code.
        """
        if JAVALANG_AVAILABLE:
            try:
                return cls._extract_with_javalang(source_code)
            except Exception:
                # If javalang fails on incomplete snippets or syntax errors, use fallback
                return cls._extract_with_fallback(source_code)
        else:
            return cls._extract_with_fallback(source_code)

    @classmethod
    def _extract_with_javalang(cls, source_code: str) -> Dict[str, Any]:
        tree = javalang.parse.parse(source_code)
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
            "max_depth": 0
        }
        function_names: List[str] = []

        for path, node in tree:
            depth = len(path)
            if depth > features["max_depth"]:
                features["max_depth"] = depth

            node_name = type(node).__name__
            node_sequence.append(node_name)

            if isinstance(node, (javalang.tree.MethodDeclaration, javalang.tree.ConstructorDeclaration)):
                features["functions"] += 1
                function_names.append(node.name)
                start_line = getattr(node.position, 'line', 1) if node.position else 1
                blocks.append({
                    "type": "method",
                    "name": node.name,
                    "start_line": start_line,
                    "end_line": start_line + 10 # Estimated if exact end is unavailable
                })
            elif isinstance(node, (javalang.tree.ClassDeclaration, javalang.tree.InterfaceDeclaration)):
                features["classes"] += 1
                start_line = getattr(node.position, 'line', 1) if node.position else 1
                blocks.append({
                    "type": "class",
                    "name": node.name,
                    "start_line": start_line,
                    "end_line": start_line + 20
                })
            elif isinstance(node, (javalang.tree.ForStatement, javalang.tree.WhileStatement, javalang.tree.DoStatement)):
                features["loops"] += 1
            elif isinstance(node, (javalang.tree.IfStatement, javalang.tree.SwitchStatement)):
                features["conditionals"] += 1
            elif isinstance(node, javalang.tree.MethodInvocation):
                features["function_calls"] += 1
            elif isinstance(node, (javalang.tree.VariableDeclarator, javalang.tree.LocalVariableDeclaration)):
                features["variables"] += 1
            elif isinstance(node, javalang.tree.ReturnStatement):
                features["returns"] += 1
            elif isinstance(node, javalang.tree.TryStatement):
                features["try_blocks"] += 1

        return {
            "success": True,
            "error": None,
            "node_sequence": node_sequence,
            "structural_features": features,
            "blocks": blocks,
            "function_names": function_names
        }

    @classmethod
    def _extract_with_fallback(cls, source_code: str) -> Dict[str, Any]:
        """
        Robust structural lexical parser for Java syntax when javalang is not present or syntax errors occur.
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
            "max_depth": 0
        }
        function_names: List[str] = []

        class_pattern = re.compile(r'\b(class|interface|enum)\s+([a-zA-Z_]\w*)')
        method_pattern = re.compile(r'\b(?:public|private|protected|static|final|native|synchronized|\s)+[\w<>\[\]]+\s+([a-zA-Z_]\w*)\s*\([^)]*\)\s*(?:throws\s+[\w,\s]+)?\{')
        loop_pattern = re.compile(r'\b(for|while|do)\b')
        if_pattern = re.compile(r'\b(if|switch)\b')
        try_pattern = re.compile(r'\b(try|catch|finally)\b')
        return_pattern = re.compile(r'\breturn\b')
        call_pattern = re.compile(r'\b([a-zA-Z_]\w*)\s*\(')

        current_depth = 0
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('//') or stripped.startswith('/*'):
                continue

            open_braces = line.count('{')
            close_braces = line.count('}')
            current_depth = max(0, current_depth + open_braces - close_braces)
            if current_depth > features["max_depth"]:
                features["max_depth"] = current_depth

            # Class match
            c_match = class_pattern.search(line)
            if c_match:
                features["classes"] += 1
                node_sequence.append("ClassDeclaration")
                blocks.append({
                    "type": "class",
                    "name": c_match.group(2),
                    "start_line": i,
                    "end_line": min(len(lines), i + 25)
                })

            # Method match
            m_match = method_pattern.search(line)
            if m_match and m_match.group(1) not in {'if', 'for', 'while', 'switch', 'catch'}:
                features["functions"] += 1
                fname = m_match.group(1)
                function_names.append(fname)
                node_sequence.append("MethodDeclaration")
                blocks.append({
                    "type": "method",
                    "name": fname,
                    "start_line": i,
                    "end_line": min(len(lines), i + 15)
                })

            if loop_pattern.search(line):
                features["loops"] += 1
                node_sequence.append("LoopStatement")

            if if_pattern.search(line):
                features["conditionals"] += 1
                node_sequence.append("IfStatement")

            if try_pattern.search(line):
                features["try_blocks"] += 1
                node_sequence.append("TryStatement")

            if return_pattern.search(line):
                features["returns"] += 1
                node_sequence.append("ReturnStatement")

            calls = call_pattern.findall(line)
            for call in calls:
                if call not in {'if', 'for', 'while', 'switch', 'catch', 'super', 'this'}:
                    features["function_calls"] += 1
                    node_sequence.append("MethodInvocation")

        # If node sequence is still very sparse, add token representation
        if len(node_sequence) < 5:
            tokens = Tokenizer.tokenize(source_code, "java", normalize_identifiers=True)
            node_sequence.extend(tokens)

        return {
            "success": True,
            "error": None,
            "node_sequence": node_sequence,
            "structural_features": features,
            "blocks": blocks,
            "function_names": function_names
        }
