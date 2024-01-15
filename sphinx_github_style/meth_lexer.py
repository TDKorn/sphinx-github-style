import types
from typing import Type, Optional
from pygments.lexers.python import NumPyLexer
from inspect import getmembers, isfunction, ismethod, ismodule, isclass


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
    """Adds syntax highlighting for methods and functions within a python Package

    """
    name = 'TDK'
    url = 'https://github.com/TDKorn'
    aliases = ['tdk']
    TOP_LEVEL = None

    @classmethod
    def get_pkg_lexer(cls, pkg_name: Optional[str] = None) -> Type["TDKMethLexer"]:
        if pkg_name:
            cls.TOP_LEVEL = pkg_name

        if not cls.TOP_LEVEL:
            raise ValueError('Must provide a package name')

        pkg = __import__(cls.TOP_LEVEL)
        funcs = get_pkg_funcs(pkg)
        cls.EXTRA_KEYWORDS = funcs
        return cls


