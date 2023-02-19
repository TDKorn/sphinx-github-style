import sphinx
from sphinx.application import Sphinx
from typing import Dict, Any


def setup(app: Sphinx) -> Dict[str, Any]:
    # imports defined inside setup function, so that the __version__ can be loaded,
    # even if Sphinx is not yet installed.
    __version__ = "0.0.1b1"
    __author__ = 'Adam Korn <hello@dailykitten.net>'

    from .github_style import TDKStyle
    from .meth_lexer import TDKMethLexer
    from .add_linkcode_class import add_linkcode_node_class

    app.connect('doctree-resolved', add_linkcode_node_class)
    # app.connect('build-finished', save_generated_rst_files)
    app.add_config_value('linkcode_link_text', '[source]', 'html')
    app.add_css_file('github_linkcode.css')
    app.add_lexer('TDK', TDKMethLexer)

    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}
