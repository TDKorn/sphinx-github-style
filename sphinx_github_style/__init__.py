__version__ = "0.0.1b1"
__author__ = 'Adam Korn <hello@dailykitten.net>'

from sphinx.application import Sphinx


def setup(app: Sphinx):
    # imports defined inside setup function, so that the __version__ can be loaded,
    # even if Sphinx is not yet installed.
    from sphinx.writers.text import STDINDENT

    from .github_style import TDKStyle
    from .meth_lexer import TDKMethLexer
    from .add_linkcode_class import add_linkcode_node_class

    app.require_sphinx('1.4')
    app.add_lexer('tdk', TDKMethLexer)
    app.add_css_file('_static/github_linkcode.css')
    app.connect('doctree-resolved', add_linkcode_node_class)
    app.add_config_value('linkcode_link_text', '[source]', '')

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
