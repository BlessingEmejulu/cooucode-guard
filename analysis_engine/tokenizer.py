import re
import token as py_token
import tokenize
from io import StringIO
from typing import List, Tuple, Dict, Any

class Tokenizer:
    """
    Language-aware tokenizer and normalizer for Python, Java, and C++.
    Supports comment stripping, identifier normalization, and token-sequence generation.
    """

    PYTHON_KEYWORDS = {
        'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break',
        'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal',
        'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'
    }

    JAVA_KEYWORDS = {
        'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char',
        'class', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum',
        'extends', 'final', 'finally', 'float', 'for', 'goto', 'if', 'implements',
        'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new',
        'package', 'private', 'protected', 'public', 'return', 'short', 'static',
        'strictfp', 'super', 'switch', 'synchronized', 'this', 'throw', 'throws',
        'transient', 'try', 'void', 'volatile', 'while', 'record', 'var', 'yield'
    }

    CPP_KEYWORDS = {
        'alignas', 'alignof', 'and', 'and_eq', 'asm', 'auto', 'bitand', 'bitor',
        'bool', 'break', 'case', 'catch', 'char', 'char8_t', 'char16_t', 'char32_t',
        'class', 'compl', 'concept', 'const', 'consteval', 'constexpr', 'constinit',
        'const_cast', 'continue', 'co_await', 'co_return', 'co_yield', 'decltype',
        'default', 'delete', 'do', 'double', 'dynamic_cast', 'else', 'enum',
        'explicit', 'export', 'extern', 'false', 'float', 'for', 'friend', 'goto',
        'if', 'inline', 'int', 'long', 'mutable', 'namespace', 'new', 'noexcept',
        'not', 'not_eq', 'nullptr', 'operator', 'or', 'or_eq', 'private', 'protected',
        'public', 'register', 'reinterpret_cast', 'requires', 'return', 'short',
        'signed', 'sizeof', 'static', 'static_assert', 'static_cast', 'struct',
        'switch', 'template', 'this', 'thread_local', 'throw', 'true', 'try',
        'typedef', 'typeid', 'typename', 'union', 'unsigned', 'using', 'virtual',
        'void', 'volatile', 'wchar_t', 'while', 'xor', 'xor_eq', 'include', 'define'
    }

    @classmethod
    def get_keywords(cls, language: str) -> set:
        lang = (language or "").lower()
        if "python" in lang:
            return cls.PYTHON_KEYWORDS
        elif "java" in lang:
            return cls.JAVA_KEYWORDS
        elif "c++" in lang or "cpp" in lang or "c" in lang:
            return cls.CPP_KEYWORDS
        return cls.PYTHON_KEYWORDS.union(cls.JAVA_KEYWORDS).union(cls.CPP_KEYWORDS)

    @classmethod
    def strip_comments_and_docstrings(cls, code: str, language: str) -> str:
        """Removes single-line and multi-line comments from source code."""
        lang = (language or "").lower()
        if "python" in lang:
            return cls._strip_python_comments(code)
        else:
            return cls._strip_c_style_comments(code)

    @classmethod
    def _strip_python_comments(cls, source: str) -> str:
        try:
            io_obj = StringIO(source)
            out = []
            prev_toktype = py_token.INDENT
            last_lineno = -1
            last_col = 0
            tokgen = tokenize.generate_tokens(io_obj.readline)
            for toktype, ttext, (slineno, scol), (elineno, ecol), ltext in tokgen:
                if slineno > last_lineno:
                    last_col = 0
                if scol > last_col:
                    out.append(" " * (scol - last_col))
                if toktype == py_token.COMMENT:
                    pass
                elif toktype == py_token.STRING:
                    if prev_toktype in (py_token.INDENT, py_token.NEWLINE, tokenize.NL):
                        # likely docstring
                        pass
                    else:
                        out.append(ttext)
                else:
                    out.append(ttext)
                prev_toktype = toktype
                last_lineno = elineno
                last_col = ecol
            return "".join(out)
        except Exception:
            # Fallback regex
            source = re.sub(r'#.*$', '', source, flags=re.MULTILINE)
            source = re.sub(r'(\'\'\'[\s\S]*?\'\'\'|"""[\s\S]*?""")', '', source)
            return source

    @classmethod
    def _strip_c_style_comments(cls, source: str) -> str:
        # Strip /* ... */ multi-line and // single-line comments
        pattern = r'(//.*?$)|(/\*.*?\*/)'
        return re.sub(pattern, '', source, flags=re.MULTILINE | re.DOTALL)

    @classmethod
    def normalize_whitespace(cls, code: str) -> str:
        """Normalizes multiple whitespaces and trims empty lines."""
        lines = [line.strip() for line in code.splitlines()]
        lines = [line for line in lines if line]
        return "\n".join(lines)

    @classmethod
    def tokenize(cls, code: str, language: str, normalize_identifiers: bool = True) -> List[str]:
        """
        Converts source code into a standardized list of tokens.
        If normalize_identifiers=True, replaces non-keyword identifiers with 'ID'.
        """
        stripped = cls.strip_comments_and_docstrings(code, language)
        keywords = cls.get_keywords(language)

        # Regex for tokens: words (keywords or identifiers), numbers, operators/delimiters
        token_pattern = re.compile(
            r'([a-zA-Z_]\w*)|'                 # identifiers / keywords
            r'(\d+\.?\d*(?:[eE][+-]?\d+)?)|'   # numbers
            r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|'  # string literals
            r'(==|!=|<=|>=|\+\+|--|&&|\|\||<<|>>|\+=|-=|\*=|/=|%=|->|::|[\+\-\*/%=\<\>&\|\^\!~?:;,\.\[\]\(\)\{\}])' # symbols
        )

        tokens = []
        identifier_map: Dict[str, str] = {}
        id_counter = 1

        for match in token_pattern.finditer(stripped):
            val = match.group(0)
            if not val:
                continue

            if val in keywords:
                tokens.append(f"KW_{val.upper()}")
            elif re.match(r'^[a-zA-Z_]\w*$', val):
                if normalize_identifiers:
                    if val not in identifier_map:
                        identifier_map[val] = f"ID_{id_counter}"
                        id_counter += 1
                    tokens.append(identifier_map[val])
                else:
                    tokens.append(f"ID_{val}")
            elif re.match(r'^\d', val):
                tokens.append("NUM")
            elif val.startswith('"') or val.startswith("'"):
                tokens.append("STR")
            else:
                tokens.append(f"SYM_{val}")

        return tokens

    @classmethod
    def get_token_frequency(cls, tokens: List[str]) -> Dict[str, int]:
        freq = {}
        for tok in tokens:
            freq[tok] = freq.get(tok, 0) + 1
        return freq
