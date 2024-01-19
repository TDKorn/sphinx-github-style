.. |.~.get_linkcode_resolve| replace:: ``get_linkcode_resolve()``
.. _.~.get_linkcode_resolve: https://sphinx-github-style.readthedocs.io/en/latest/modules.html#sphinx_github_style.__init__.get_linkcode_resolve
.. |linkcode_blob| replace:: ``linkcode_blob``
.. _linkcode_blob: https://sphinx-github-style.readthedocs.io/en/latest/index.html#confval-linkcode_blob
.. |linkcode_link_text| replace:: ``linkcode_link_text``
.. _linkcode_link_text: https://sphinx-github-style.readthedocs.io/en/latest/index.html#confval-linkcode_link_text
.. |linkcode_resolve| replace:: ``linkcode_resolve``
.. _linkcode_resolve: https://sphinx-github-style.readthedocs.io/en/latest/index.html#confval-linkcode_resolve
.. |linkcode_url| replace:: ``linkcode_url``
.. _linkcode_url: https://sphinx-github-style.readthedocs.io/en/latest/index.html#confval-linkcode_url
.. |sphinx+html_context| replace:: ``html_context``
.. _sphinx+html_context: https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_context
.. |.sphinx.ext.linkcode| replace:: ``sphinx.ext.linkcode``
.. _.sphinx.ext.linkcode: https://www.sphinx-doc.org/en/master/usage/extensions/linkcode.html#module-sphinx.ext.linkcode
.. |.sphinx.ext.viewcode| replace:: ``sphinx.ext.viewcode``
.. _.sphinx.ext.viewcode: https://www.sphinx-doc.org/en/master/usage/extensions/viewcode.html#module-sphinx.ext.viewcode
.. |top_level| replace:: ``top_level``
.. _top_level: https://sphinx-github-style.readthedocs.io/en/latest/index.html#confval-top_level

..  Title: Sphinx Github Style
..  Description: A Sphinx extension to add GitHub source code links and syntax highlighting
..  Author: TDKorn (Adam Korn)

.. meta::
   :title: Sphinx Github Style
   :description: A Sphinx extension to add GitHub source code links and syntax highlighting


.. |.github_style| replace:: ``github_style.css``
.. _.github_style: https://github.com/tdkorn/sphinx-github-style/tree/v1.0.4/sphinx_github_style/_static/github_style.css





.. raw:: html

   <div align="center">


.. image:: https://raw.githubusercontent.com/TDKorn/sphinx-github-style/master/docs/source/_static/logo_square_grey_blue.png
   :alt: Sphinx GitHub Style: GitHub Integration and Pygments Style for Sphinx Documentation
   :width: 25%



.. raw:: html

   <h1>Sphinx Github Style</h1>


GitHub source code links and syntax highlighting for Sphinx documentation


.. |docs| replace:: **Explore the docs »**
.. _docs: https://sphinx-github-style.readthedocs.io/en/latest/

|docs|_




.. image:: https://img.shields.io/pypi/v/sphinx-github-style?color=eb5202
   :target: https://pypi.org/project/sphinx-github-style/
   :alt: PyPI Version

.. image:: https://img.shields.io/badge/GitHub-sphinx--github--style-4f1abc
   :target: https://github.com/tdkorn/sphinx-github-style/
   :alt: GitHub Repository

.. image:: https://static.pepy.tech/personalized-badge/sphinx-github-style?period=total&units=none&left_color=grey&right_color=blue&left_text=Downloads
    :target: https://pepy.tech/project/sphinx-github-style/

.. image:: https://readthedocs.org/projects/sphinx-github-style/badge/?version=latest
    :target: https://sphinx-github-style.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. raw:: html

   </div>
   <br/>
   <br/>



About
~~~~~~~~~~~~~

``sphinx-github-style`` is a Sphinx extension that links your documentation to GitHub source code.
It also adds syntax highlighting for code blocks similar to GitHub's pretty lights dark theme.

...


GitHub Source Code Links
===============================


Using |.sphinx.ext.linkcode|_,  a ``View on GitHub`` link is added to the documentation of every class, method, function, and property:





.. image:: https://raw.githubusercontent.com/TDKorn/sphinx-github-style/master/docs/source/_static/github_link.png
   :alt: sphinx-github-style adds a "View on GitHub" link


They link to and highlight the corresponding code block in your GitHub repository:



.. image:: https://raw.githubusercontent.com/TDKorn/sphinx-github-style/master/docs/source/_static/github_linked_code.png
   :alt: The linked corresponding highlighted source code block on GitHub



.. raw:: html

   <table>
       <tr align="left">
           <th>

📝 Note

.. raw:: html

   </th>
   <tr><td>

These links can be `styled with CSS <https://sphinx-github-style.readthedocs.io/en/latest/add_linkcode_class.html>`_ and used with/instead
of the links added by |.sphinx.ext.viewcode|_

.. raw:: html

   </td></tr>
   </table>



Syntax Highlighting
====================

``sphinx-github-style`` also contains a ``Pygments`` style to highlight code blocks similar to GitHub:



.. image:: https://raw.githubusercontent.com/TDKorn/sphinx-github-style/master/docs/source/_static/syntax_highlighting.png
   :alt: A code block highlighted by the Pygments style. It looks identical to GitHub.



Installation
~~~~~~~~~~~~~~~~

To install using ``pip``::

 pip install sphinx-github-style


Configuration
~~~~~~~~~~~~~~~

Add the extension to your ``conf.py``

.. code-block:: python

   extensions = [
       "sphinx_github_style",
   ]

Optional Configuration Variables
===================================

Add any (or none) of the following configuration variables to your ``conf.py``




|top_level|_
 The name of the package's top-level module. For this repo, it would be ``sphinx_github_style``

  **Type:** ``str``

|

|linkcode_blob|_
 The blob to link to on GitHub - any of ``"head"``, ``"last_tag"``, or ``"{blob}"``

  **Type:** ``str``

  **Default:** ``"head"``

 * ``"head"`` (default): links to the most recent commit hash; if this commit is tagged, uses the tag instead
 * ``"last_tag"``: links to the most recent commit tag on the currently checked out branch
 * ``"blob"``: links to any blob you want, for example ``"master"`` or ``"v2.0.1"``

|

|linkcode_url|_
 The link to your GitHub repository formatted as ``https://github.com/user/repo``

  **Type:** ``str``

  **Default:** ``f"https://github.com/{html_context['github_user']}/{html_context['github_repo']}/{html_context['github_version']}"``

 * If not provided, will attempt to create the link from the |sphinx+html_context|_ dict

|

|linkcode_link_text|_
 The text to use for the linkcode link

  **Type:** ``str``

  **Default:** ``"View on GitHub"``

|

|linkcode_resolve|_
 A ``linkcode_resolve()`` function to use when resolving the link target with |.sphinx.ext.linkcode|_

  **Type:** ``Callable``

  **Default:** Return value from |.~.get_linkcode_resolve|_

