import builtins
from typing import Set, Dict
from pygments.token import Name, Keyword
from pygments.lexers.python import PythonLexer
from inspect import getmembers, isclass, isbuiltin, ismethoddescriptor


def get_builtins() -> Dict[str, Set]:
    """Returns a dictionary containing names of built-in functions, classes, and methods"""
    funcs_meths = set(dict(getmembers(builtins, isbuiltin)))
    classes = set()

    for class_name, _class in getmembers(builtins, isclass):
        methods = getmembers(_class, ismethoddescriptor)
        funcs_meths.update(dict(methods))
        classes.add(class_name)

    return {
        'funcs': funcs_meths,
        'classes': classes
    }


BUILTINS = get_builtins()


class TDKLexer(PythonLexer):
    """A Pygments Lexer that adds syntax highlighting for the methods, classes, type hints, etc. in a Python package"""

    name = 'TDK'
    url = 'https://github.com/TDKorn'
    aliases = ['tdk']

    def get_tokens_unprocessed(self, text):
        """Override to add better syntax highlighting"""
        tokens = list(PythonLexer.get_tokens_unprocessed(self, text))

        for token_idx, (index, token, value) in enumerate(tokens):
            # Highlight builtins as either function calls or type hints
            if token is Name.Builtin and value in BUILTINS['classes']:
                if tokens[token_idx+1][-1] == '(':
                    yield index, Name.Builtin, value
                else:
                    yield index, Name.Builtin.Pseudo, value

            elif token is Name:
                if value[0].isupper():  # Highlight as class
                    yield index, Name.Class, value
                elif tokens[token_idx+1][-1] == '(':  # Highlight as function
                    yield index, Keyword.Pseudo, value
                else:
                    yield index, Name, value

            else:
                yield index, token, value
