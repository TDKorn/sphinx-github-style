sphinx-github-style
######################

Github Pygments Style and Sphinx Integration

Components
~~~~~~~~~~~~~~
.. |.linkcode_resolve| replace:: ``~.linkcode_resolve()``
.. _.linkcode_resolve: :func:`~.linkcode_resolve`
.. |.add_linkcode_node_class| replace:: ``~.add_linkcode_node_class()``
.. _.add_linkcode_node_class: :func:`~.add_linkcode_node_class`

|.linkcode_resolve|_
|.add_linkcode_node_class|_

* TDKStyle.py - Highlights code similar to Github Pretty Lights Dark 
* TDKMethLexor - Highlights methods in code blocks
* :func:`~.add_linkcode_node_class` - Updates ``linkcode`` nodes a new ``linkcode-link`` class to use for CSS styling separately from ``viewcode`` links
* Add default :func:`~.linkcode_resolve`
* ``github_style``.css - Linkcode link icon + text


Config Values
~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: python

    linkcode_default_blob: str = any('last_tag', 'master', 'head')
    linkcode_link_text: str = "View on GitHub"
    linkcode_url: str = "https://github.com/tdkorn/sphinx-github-style"
    linkcode_resolve: func = None


linkcode_default_blob: str = any('last_tag', 'master', 'head')

* Default is "master"
* How blob is chosen
    - If head is a tag, uses the tag
    - If head is not a tag, then
        - If default blob is "last_tag" -> Retrieve most recent tag; if no tags exist, uses master
        - If default blob is "head" -> uses last commit hash; if wasn't able to get head, uses "master"
        - If default blob is "master" -> uses "master"


