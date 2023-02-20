from pygments.lexers.python import NumPyLexer
from inspect import getmembers, isfunction, ismethod, ismodule, isclass
from sphinx.application import Sphinx
from typing import Type
import types


def get_pkg_funcs(pkg: types.ModuleType):
    # Get funcs/meths defined in pkg.__init__
    funcs_meths = get_funcs(pkg)
    modules = getmembers(pkg, ismodule)
    # Get funcs/meths of each module in pkg
    for name, module in modules:
        funcs_meths += get_funcs(module)
        classes = getmembers(module, isclass)
        for class_name, _class in classes:
            funcs_meths += get_funcs(_class)
    # Set of all funcs/meths contained in modules used by package
    return set(funcs_meths)


def get_funcs(of):
    members = getmembers(of, isfunction or ismethod)
    return list(dict(members))


class TDKMethLexer(NumPyLexer):
    """Adds syntax highlighting for a python Package's methods

    """
    name = 'TDK'
    url = 'https://github.com/TDKorn'
    aliases = ['tdk']

    EXTRA_KEYWORDS = NumPyLexer.EXTRA_KEYWORDS


def get_pkg_lexer(pkg_name: str) -> Type[TDKMethLexer]:
    pkg = __import__(pkg_name)
    funcs = get_pkg_funcs(pkg)
    TDKMethLexer.EXTRA_KEYWORDS = TDKMethLexer.EXTRA_KEYWORDS.union(funcs)
    return TDKMethLexer


def setup(app: Sphinx):
    pkg_name = app.config._raw_config['pkg_name']
    app.add_lexer('python', get_pkg_lexer(pkg_name))
