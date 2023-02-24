..  Title: Sphinx Github Style
..  Description: A Sphinx extension to add GitHub source code links and syntax highlighting
..  Author: TDKorn (Adam Korn)

.. |.get_linkcode_resolve| replace:: get_linkcode_resolve()
.. _.get_linkcode_resolve: https://github.com/TDKorn/sphinx-github-style/blob/v1.0.0/sphinx_github_style/__init__.py#L150-L207
.. |.add_linkcode_node_class| replace:: add_linkcode_node_class()
.. _.add_linkcode_node_class: https://github.com/TDKorn/sphinx-github-style/blob/v1.0.0/sphinx_github_style/add_linkcode_class.py#L9-L24
.. |.TDKStyle| replace:: TDKStyle
.. _.TDKStyle: https://github.com/TDKorn/sphinx-github-style/blob/v1.0.0/sphinx_github_style/github_style.py#L44-L139
.. |.TDKMethLexor| replace:: TDKMethLexor
.. _.TDKMethLexor: https://github.com/TDKorn/sphinx-github-style/blob/v1.0.0/sphinx_github_style/meth_lexer.py#L28-L43
.. |.github_style| replace:: github_style.css
.. _.github_style: https://github.com/tdkorn/sphinx-github-style/blob/v1.0.0/sphinx_github_style/_static/github_style.css
.. |RTD| replace:: ReadTheDocs
.. _RTD: https://sphinx-github-style.readthedocs.io/en/latest/
.. |Note| replace:: 📝 **Note**
.. |docs| replace:: **Explore the docs »**
.. _docs: https://sphinx-github-style.readthedocs.io/en/latest/


sphinx-github-style
-------------------

.. image:: https://i.imgur.com/v348dOW.png
   :alt: Sphinx GitHub Style: GitHub Integration and Pygments Style for Sphinx Documentation
   :width: 50%
   :align: center

GitHub source code links and syntax highlighting for Sphinx docs

|docs|_

|

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

|

About
~~~~~~~~~~~~~

``sphinx-github-style`` is a Sphinx extension that makes your docs look like and link to GitHub

...


GitHub Source Code Links
===============================

.. |linkcode| replace:: ``sphinx.ext.linkcode``
.. _linkcode: https://www.sphinx-doc.org/en/master/usage/extensions/linkcode.html

**Using** |linkcode|_, a ``View on GitHub`` **link is added to the documentation of every class, method and function:**

.. image:: https://user-images.githubusercontent.com/96394652/220941352-f5530a56-d338-4b90-b83a-4b22b0f632fe.png
   :alt: sphinx github style adds a "View on GitHub" link

**They link to and highlight the corresponding code block in your GitHub repo:**

.. image:: https://user-images.githubusercontent.com/96394652/220945912-447173db-2ac7-4e00-bec5-3859753bf687.png


|

+--------------------------------------------+
| |Note|                                     |
+============================================+
| These links can be used with/instead of    |
| the links added by ``sphinx.ext.viewcode`` |
|                                            |
| * They use a newly added ``linkcode-link`` |
|   class which can be styled using CSS      |
+--------------------------------------------+

|


Syntax Highlighting
=====================

``sphinx-github-style`` **also contains a** ``Pygments`` **style to highlight code in your documentation similar to GitHub:**


.. image:: https://user-images.githubusercontent.com/96394652/220946796-bf7aa236-964d-48e7-83e2-142aac00b0dd.png


|

Installation
~~~~~~~~~~~~~~~~

To install using ``pip``::

 pip install sphinx-github-style

|

Configuration
~~~~~~~~~~~~~~~

Add the extension to your ``conf.py``

.. code-block:: python

   extensions = [
       "sphinx_github_style",
   ]

...

Configuration Variables
=========================

Add any of the following configuration variables to your ``conf.py``

``linkcode_blob``
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   linkcode_blob: str = "head"


The blob to link to on GitHub - any of ``"head"``, ``"last_tag"``, or ``"{blob}"``

* ``head`` (default): links to the most recent commit hash; if this commit is tagged, uses the tag instead
* ``last_tag``: links to the most recently tagged commit; if no tags exist, uses ``head``
* ``blob``: links to any blob you want, for example ``"master"`` or ``"v2.0.1"``


...

``linkcode_url``
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   linkcode_url: str = f"https://github.com/{html_context['github_user']}/{html_context['github_repo']}/{html_context['github_version']}"

The link to your GitHub repository formatted as ``https://github.com/user/repo``

* If not provided, will attempt to create the link from the ``html_context`` dict

...

``linkcode_link_text``
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   linkcode_link_text: str = "View on GitHub"


The text to use for the linkcode link

...

``linkcode_resolve``
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   linkcode_resolve: types.FunctionType

A ``linkcode_resolve()`` function to use for resolving the link target

* Uses default function from |.get_linkcode_resolve|_ if not specified (recommended)

|

Noteworthy Components
~~~~~~~~~~~~~~~~~~~~~

* |.TDKStyle|_ - Pygments Style for syntax highlighting similar to Github Pretty Lights Dark Theme
* |.TDKMethLexor|_ - Pygments Lexor to add syntax highlighting to methods
* |.get_linkcode_resolve|_ - to link to GitHub source code using ``sphinx.ext.linkcode``
* |.add_linkcode_node_class|_ - adds a new ``linkcode-link`` class, allowing for CSS styling separately from ``viewcode`` links
* |.github_style|_ - CSS styling for linkcode links (icon + text)

|

Documentation
~~~~~~~~~~~~~~~~

Full documentation can be found on |RTD|_