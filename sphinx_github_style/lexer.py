import builtins
from pathlib import Path
from types import ModuleType
from pygments.token import Name, Keyword
from pygments.lexers.python import PythonLexer
from typing import Type, Optional, Set, Any, Dict
from inspect import getmembers, isfunction, ismethod, ismodule, isclass, isbuiltin, ismethoddescriptor


def is_module_in_package(object: Any, top_level: str) -> bool:
    """Predicate to determine if an object is a module within a top level package"""
    return ismodule(object) and object.__name__.startswith(top_level)


def is_class_in_package(object: Any, top_level: str) -> bool:
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

        try:
             mod_path = Path(mod.__file__)
        except AttributeError:  # It's a built-in module
            funcs_meths.update(get_funcs(mod))
            processed_modules.add(mod)
            continue

        if is_module_in_package(mod, top_level):
            if mod_path.name == '__init__.py':  # If it's a subpackage, call recursively on submodules
                get_pkg_funcs(mod, top_level, funcs_meths, processed_modules)
            else:
                funcs_meths.update(get_funcs(mod))

        else:  # For external modules, avoid recursion into submodules
            get_funcs_from_external_module(mod, funcs_meths)

        processed_modules.add(mod)

    return funcs_meths


def get_funcs_from_external_module(module: ModuleType, funcs_meths: Set[str]) -> Set[str]:
    """Adds functions/methods contained directly within an imported external module"""
    funcs_meths.update(get_funcs(module))
    top_level = module.__name__

    for class_name, _class in getmembers(module, lambda obj: is_class_in_package(obj, top_level)):
        funcs_meths.update(get_funcs(_class))

    return funcs_meths


def get_funcs(of: Any) -> Set[str]:
    """Returns the names of all members of the provided object that are functions or methods"""
    members = getmembers(of, lambda obj: isfunction(obj) or ismethod(obj))
    return set(dict(members))


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

    TOP_LEVEL = None
    FUNCS = BUILTINS['funcs']
    CLASSES = BUILTINS['classes']

    @classmethod
    def get_pkg_lexer(cls, pkg_name: Optional[str] = None) -> Type["TDKLexer"]:
        """Returns a lexer capable of highlighting all funcs/methods/classes/type hints within the provided package

        :param pkg_name: the name of the package's top-level module
        """
        if pkg_name:
            cls.TOP_LEVEL = pkg_name

        if not cls.TOP_LEVEL:
            raise ValueError('Must provide a package name')

        pkg = __import__(cls.TOP_LEVEL)

        # Add names of all funcs/meths in the package
        funcs = get_pkg_funcs(pkg, cls.TOP_LEVEL)
        cls.FUNCS.update(funcs)
        return cls

    def get_tokens_unprocessed(self, text):
        """Override to add better syntax highlighting"""
        tokens = list(PythonLexer.get_tokens_unprocessed(self, text))

        for token_idx, (index, token, value) in enumerate(tokens):
            if token is Name.Builtin and value in self.CLASSES:
                if tokens[token_idx+1][-1] == '(':
                    yield index, Name.Builtin, value  # Highlight as function call
                else:
                    yield index, Name.Builtin.Pseudo, value  # Highlight as type hint

            elif token is Name and value in self.FUNCS:
                if tokens[token_idx+1][-1] == '(':
                    yield index, Keyword.Pseudo, value
                else:
                    yield index, Name, value

            elif token is Name and value[0].isupper():
                yield index, Name.Class, value

            else:
                yield index, token, value
