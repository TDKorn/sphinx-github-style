import sphinx
from pathlib import Path
from typing import Dict, Any
from sphinx.application import Sphinx
from .utils.sphinx import get_conf_val, set_conf_val
from .utils.linkcode import get_linkcode_url, get_linkcode_revision, get_linkcode_resolve

__version__ = "1.2.0"
__author__ = 'Adam Korn <hello@dailykitten.net>'

from .add_linkcode_class import add_linkcode_node_class
from .github_style import GitHubStyle
from .lexer import GitHubLexer


def setup(app: Sphinx) -> Dict[str, Any]:
    app.setup_extension('sphinx.ext.linkcode')
    app.connect("builder-inited", add_static_path)
    app.connect('doctree-resolved', add_linkcode_node_class)

    app.add_config_value('linkcode_blob', 'head', True)
    app.add_config_value('linkcode_link_text', 'View on GitHub', 'html')

    linkcode_blob = get_conf_val(app, "linkcode_blob")
    linkcode_url = get_linkcode_url(
        blob=get_linkcode_revision(linkcode_blob),
        url=get_conf_val(app, 'linkcode_url'),
        context=get_conf_val(app, 'html_context'),
    )
    linkcode_func = get_conf_val(app, "linkcode_resolve")

    if not callable(linkcode_func):
        print(
            "Function `linkcode_resolve` not found in ``conf.py``; "
            "using default function from ``sphinx_github_style``"
        )
        linkcode_func = get_linkcode_resolve(linkcode_url)
        set_conf_val(app, 'linkcode_resolve', linkcode_func)

    app.add_lexer('python', GitHubLexer)
    app.add_css_file('github_style.css')
    app.config.pygments_style = 'sphinx_github_style.GitHubStyle'

    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}


def add_static_path(app) -> None:
    """Add the path for the ``_static`` folder"""
    app.config.html_static_path.append(
        str(Path(__file__).parent.joinpath("_static").absolute())
    )
