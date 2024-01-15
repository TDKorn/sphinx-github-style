import types
from pathlib import Path
from typing import Type, Optional
from pygments.lexers.python import NumPyLexer
from inspect import getmembers, isfunction, ismethod, ismodule, isclass


def is_module_in_package(object):
    """Predicate to determine if an object is a module within the project's top level package"""
    return ismodule(object) and object.__name__.startswith(TDKMethLexer.TOP_LEVEL)


def is_class_in_package(object):
    """Predicate to determine if an object is a class within the project's top level package"""
    return isclass(object) and object.__module__.startswith(TDKMethLexer.TOP_LEVEL)


def get_pkg_funcs(pkg_module: types.ModuleType, funcs_meths=set(), processed_modules=set()):
    funcs_meths.update(get_funcs(pkg_module))
    processed_modules.add(pkg_module)

    for class_name, _class in getmembers(pkg_module, is_class_in_package):
        funcs_meths.update(get_funcs(_class))

    for mod_name, mod in getmembers(pkg_module, is_module_in_package):
        if mod in processed_modules:
            continue

        try:
             mod_path = Path(mod.__file__)
        except AttributeError:
            continue  # It's a built-in module

        if mod_path.name == '__init__.py':  # If it's a subpackage, call recursively to process all submodules
            get_pkg_funcs(mod, funcs_meths, processed_modules)

        else:  # If it's not a subpackage, get all funcs/meths defined in it
            funcs_meths.update(get_funcs(mod))
            processed_modules.add(mod)

    return funcs_meths


def get_funcs(of):
    members = getmembers(of, lambda obj: isfunction(obj) or ismethod(obj))
    return set(dict(members))


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


