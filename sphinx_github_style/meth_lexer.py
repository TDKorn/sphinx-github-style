from pygments.lexers.python import NumPyLexer
from inspect import getmembers, getmodule, isfunction, ismethod, ismodule, isclass
from sphinx.application import Sphinx
import types
import sphinx_github_style

def get_pkg_funcs(pkg: types.ModuleType):
    funcs_meths = get_funcs(pkg)  # Get funcs/meths defined in pkg.__init__
    modules = getmembers(pkg, ismodule)  # Modules of package
    for name, module in modules:
        funcs_meths += get_funcs(module)  # Get standalone funcs defined in module
        classes = getmembers(module, isclass)  # Get classes in module
        for class_name, _class in classes:
            if getmodule(_class).__name__.startswith(
                    pkg.__name__):  # If class is defined in the module, get its funcs/meths
                funcs_meths += get_funcs(_class)
    return set(funcs_meths)


def get_funcs(of):
    members = getmembers(of, isfunction or ismethod)
    return list(dict(members))


funcs = get_pkg_funcs(sphinx_github_style)


class TDKMethLexer(NumPyLexer):
    name = 'TDK'
    url = 'https://github.com/TDKorn'
    aliases = ['tdk']

    EXTRA_KEYWORDS = NumPyLexer.EXTRA_KEYWORDS.union(funcs)


def setup(app: Sphinx):
    app.add_lexer('python', TDKMethLexer)
