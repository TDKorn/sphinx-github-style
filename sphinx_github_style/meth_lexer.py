from pygments.lexers.python import NumPyLexer
from inspect import getmembers, getmodule, isfunction, ismethod, ismodule, isclass
from sphinx.application import Sphinx
import sphinx_github_style
import types


class TDKMethLexer(NumPyLexer):
    """Adds syntax highlighting for a python Package's methods

    """
    name = 'TDK'
    url = 'https://github.com/TDKorn'
    aliases = ['tdk']

    def __int__(self):
        funcs = TDKMethLexer.get_pkg_funcs(sphinx_github_style)
        funcs.update(NumPyLexer.EXTRA_KEYWORDS)
        TDKMethLexer.EXTRA_KEYWORDS = funcs
        print(TDKMethLexer.EXTRA_KEYWORDS)
        print(self.EXTRA_KEYWORDS)

    @staticmethod
    def get_funcs(of):
        members = getmembers(of, isfunction or ismethod)
        return list(dict(members))

    @staticmethod
    def get_pkg_funcs(pkg: types.ModuleType):
        # Get funcs/meths defined in pkg.__init__
        funcs_meths = TDKMethLexer.get_funcs(pkg)
        modules = getmembers(pkg, ismodule)
        # Get funcs/meths of each module in pkg
        for name, module in modules:
            funcs_meths += TDKMethLexer.get_funcs(module)
            classes = getmembers(module, isclass)
            for class_name, _class in classes:
                funcs_meths += TDKMethLexer.get_funcs(_class)
        # Set of all funcs/meths contained in modules used by package
        return set(funcs_meths)


def setup(app: Sphinx):
    app.add_lexer('python', TDKMethLexer)
