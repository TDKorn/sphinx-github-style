import builtins
from pathlib import Path
from types import ModuleType
from typing import Type, Optional, Set
from pygments.lexers.python import NumPyLexer
from inspect import getmembers, isfunction, ismethod, ismodule, isclass, isbuiltin, ismethoddescriptor


def is_module_in_package(object, top_level):
    """Predicate to determine if an object is a module within a top level package"""
    return ismodule(object) and object.__name__.startswith(top_level)


def is_class_in_package(object, top_level):
    """Predicate to determine if an object is a class within a top level package"""
    return isclass(object) and object.__module__.startswith(top_level)


def get_pkg_funcs(pkg_module: ModuleType, top_level: str, funcs_meths: Set[str] = set(), processed_modules: Set[ModuleType] = set()) -> Set[str]:
    """Finds all functions and methods that are defined within a package and its subpackages.

    For external modules that are imported into the package, only the functions and methods
    that are directly within the module are included.

    :param pkg_module: the package's top-level module
    :param top_level: the name of the top-level module
    :param funcs_meths: a set of function/method names
    :param processed_modules: a set of already processed modules
    :return: a set containing the names of all found functions and methods
    """
    funcs_meths.update(get_funcs(pkg_module))
    processed_modules.add(pkg_module)

    for class_name, _class in getmembers(pkg_module, isclass):
        funcs_meths.update(get_funcs(_class))

    for mod_name, mod in getmembers(pkg_module, ismodule):
        if mod in processed_modules:
            continue

        processed_modules.add(mod)
    
        try:
             mod_path = Path(mod.__file__)
        except AttributeError:  # It's a built-in module
            funcs_meths.update(get_funcs(mod))
            continue

        if is_module_in_package(mod, top_level):
            if mod_path.name == '__init__.py':  # If it's a subpackage, call recursively on submodules
                get_pkg_funcs(mod, top_level, funcs_meths, processed_modules)
            else:
                funcs_meths.update(get_funcs(mod))

        else:  # For external modules, avoid recursion into submodules
            get_funcs_from_external_module(mod, funcs_meths)

    return funcs_meths


def get_funcs_from_external_module(module: ModuleType, funcs_meths: Set[str]):
    """Adds functions/methods contained within an imported external module"""
    funcs_meths.update(get_funcs(module))
    top_level = module.__name__

    for class_name, _class in getmembers(module, lambda obj: is_class_in_package(obj, top_level)):
        funcs_meths.update(get_funcs(_class))

    return funcs_meths


def get_builtin_funcs():
    funcs_meths = set(dict(getmembers(builtins, isbuiltin)))

    for class_name, _class in getmembers(builtins, isclass):
        methods = getmembers(_class, ismethoddescriptor)
        funcs_meths.update(set(dict(methods)))

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
    EXTRA_KEYWORDS = get_builtin_funcs()

    @classmethod
    def get_pkg_lexer(cls, pkg_name: Optional[str] = None) -> Type["TDKMethLexer"]:
        if pkg_name:
            cls.TOP_LEVEL = pkg_name

        if not cls.TOP_LEVEL:
            raise ValueError('Must provide a package name')

        pkg = __import__(cls.TOP_LEVEL)
        funcs = get_pkg_funcs(pkg, cls.TOP_LEVEL)
        cls.EXTRA_KEYWORDS.update(funcs)
        return cls


