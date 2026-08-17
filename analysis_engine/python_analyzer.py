import ast
from typing import List, Dict, Any, Tuple

class PythonASTVisitor(ast.NodeVisitor):
    def __init__(self):
        self.node_sequence: List[str] = []
        self.structural_features = {
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
        self.current_depth = 0
        self.identifiers: List[str] = []
        self.function_names: List[str] = []
        self.blocks: List[Dict[str, Any]] = []

    def generic_visit(self, node):
        self.current_depth += 1
        if self.current_depth > self.structural_features["max_depth"]:
            self.structural_features["max_depth"] = self.current_depth

        node_name = type(node).__name__
        self.node_sequence.append(node_name)

        if isinstance(node, ast.FunctionDef):
            self.structural_features["functions"] += 1
            self.function_names.append(node.name)
            if hasattr(node, 'lineno') and hasattr(node, 'end_lineno') and node.end_lineno:
                self.blocks.append({
                    "type": "function",
                    "name": node.name,
                    "start_line": node.lineno,
                    "end_line": node.end_lineno
                })
        elif isinstance(node, ast.ClassDef):
            self.structural_features["classes"] += 1
            if hasattr(node, 'lineno') and hasattr(node, 'end_lineno') and node.end_lineno:
                self.blocks.append({
                    "type": "class",
                    "name": node.name,
                    "start_line": node.lineno,
                    "end_line": node.end_lineno
                })
        elif isinstance(node, (ast.For, ast.While)):
            self.structural_features["loops"] += 1
            if hasattr(node, 'lineno') and hasattr(node, 'end_lineno') and node.end_lineno:
                self.blocks.append({
                    "type": "loop",
                    "start_line": node.lineno,
                    "end_line": node.end_lineno
                })
        elif isinstance(node, (ast.If, getattr(ast, 'Match', ast.AST))):
            self.structural_features["conditionals"] += 1
        elif isinstance(node, ast.Call):
            self.structural_features["function_calls"] += 1
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            self.structural_features["variables"] += 1
            self.identifiers.append(node.id)
        elif isinstance(node, ast.Return):
            self.structural_features["returns"] += 1
        elif isinstance(node, ast.Try):
            self.structural_features["try_blocks"] += 1

        super().generic_visit(node)
        self.current_depth -= 1

class PythonAnalyzer:
    """
    Analyzes Python source code using Python's built-in `ast` module.
    Extracts structural AST tokens, normalized representations, and code blocks.
    """

    @classmethod
    def parse_ast(cls, source_code: str) -> Tuple[bool, Any, str]:
        """Parses Python source code into an AST object."""
        try:
            tree = ast.parse(source_code)
            return True, tree, ""
        except SyntaxError as e:
            return False, None, f"Syntax Error: {e.msg} at line {e.lineno}"
        except Exception as e:
            return False, None, f"AST Parsing failed: {str(e)}"

    @classmethod
    def extract_structure(cls, source_code: str) -> Dict[str, Any]:
        """
        Extracts structural features, AST node sequence, and structural blocks.
        Gracefully handles malformed Python code.
        """
        success, tree, error_msg = cls.parse_ast(source_code)
        if not success or tree is None:
            # Fallback for syntax errors: build a basic token sequence
            from analysis_engine.tokenizer import Tokenizer
            tokens = Tokenizer.tokenize(source_code, "python", normalize_identifiers=True)
            return {
                "success": False,
                "error": error_msg,
                "node_sequence": tokens,
                "structural_features": {
                    "functions": 0, "classes": 0, "loops": 0, "conditionals": 0,
                    "function_calls": 0, "variables": 0, "returns": 0, "try_blocks": 0,
                    "max_depth": 1
                },
                "blocks": [],
                "function_names": []
            }

        visitor = PythonASTVisitor()
        visitor.visit(tree)

        return {
            "success": True,
            "error": None,
            "node_sequence": visitor.node_sequence,
            "structural_features": visitor.structural_features,
            "blocks": visitor.blocks,
            "function_names": visitor.function_names
        }

    @classmethod
    def get_normalized_ast_string(cls, source_code: str) -> str:
        """Returns a string representation of AST nodes without names/literals."""
        res = cls.extract_structure(source_code)
        return " -> ".join(res["node_sequence"])
