import sphinx
from sphinx.locale import _
from sphinx.application import Sphinx
from docutils.nodes import Node, Text
from docutils import nodes
from typing import Any, Dict


def add_linkcode_node_class(app: Sphinx, doctree: Node, docname: str) -> None:
    """Changes every :class:`~.Node` added by linkcode to use the ``"linkcode-link"`` class

    This creates separation from the nodes added by ``sphinx.ext.viewcode``, allowing
    for different link text and CSS styling

    Sets the link text to ``linkcode_link_text``, or ``"[source]"`` if not provided
    """
    env = app.builder.env
    link_text = getattr(env.config, 'linkcode_link_text')

    for node in list(doctree.findall(nodes.inline)):
        if 'viewcode-link' in node['classes']:
            if node.parent.get('internal', None) is False:
                node['classes'] = ['linkcode-link']
                node.children = [Text(_(f'{link_text}'))]


def setup(app: Sphinx) -> Dict[str, Any]:
    app.connect('doctree-resolved', add_linkcode_node_class)
    app.add_config_value('linkcode_link_text', 'View on GitHub', '')
    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}
