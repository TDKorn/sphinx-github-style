.. |.linkcode_resolve| replace:: ``linkcode_resolve()``
.. _.linkcode_resolve: :func:`~.linkcode_resolve`
.. |.add_linkcode_node_class| replace:: ``add_linkcode_node_class()``
.. _.add_linkcode_node_class: :func:`~.add_linkcode_node_class`


.. raw:: html

   <div align="center">


.. image:: docs/source/_static/logo_square_grey_blue.png
   :alt: Sphinx GitHub Style: Magento 2 REST API wrapper
   :width: 25%

.. raw:: html

   <h1>sphinx-github-style</h1>



.. |RTD|_

.. image:: https://img.shields.io/pypi/v/sphinx-github-style?color=eb5202
   :target: https://pypi.org/project/sphinx-github-style/
   :alt: PyPI Version

.. image:: https://img.shields.io/badge/GitHub-sphinx--github--theme-4f1abc
   :target: https://github.com/tdkorn/sphinx-github-style
   :alt: GitHub Repository

.. image:: https://static.pepy.tech/personalized-badge/sphinx-github-style?period=total&units=none&left_color=grey&right_color=blue&left_text=Downloads
    :target: https://pepy.tech/project/my-magento

.. image:: https://readthedocs.org/projects/sphinx-github-style/badge/?version=latest
    :target: https://sphinx-github-style.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. raw:: html

   </div>
   <br/>
   <br/>


About
~~~~~~~~~

``sphinx-github-style`` is a 
Sphinx extension that adds GitHub source code links and syntax highlighting to your documentation

Sample
========

A "View on GitHub" link will be added to your API documentation.
It can be used in addition to or instead of the links added by ``sphinx.ext.viewcode``:

.. image:: https://user-images.githubusercontent.com/96394652/220267328-76b573ea-1c18-4490-9eaf-36ed9ca5a9c0.png
   :alt: sphinx github style adds a "View on GitHub" link

These link to the highlighted code in your GitHub repo:

.. parse gh code
.. image:: https://user-images.githubusercontent.com/96394652/220267628-10cbda6d-7f51-4e66-bdff-23410cbfacc4.png


``sphinx-github-style`` also contains a Pygments style to highlight code blocks in your documentation similar to GitHub's syntax highlighting dark theme:

.. parse docs code
.. image:: https://user-images.githubusercontent.com/96394652/220267065-f371a152-0abe-402e-b350-d5171d933931.png


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


Configuration Variables
=========================

You can also add any of the following configuration values to your ``conf.py``

.. code-block:: python

    linkcode_blob: str = any('last_tag', 'head')


The blob to link to on GitHub

* Either ``"head"``, ``"last_tag"``, or ``"{blob}"``  (default is ``"head"``)

  - ``head`` (default): links to the most recent commit
  - ``last_tag``: links to the most recently tagged commit; if no tags exist, uses ``head``
  - ``blob``: links to any blob you want, for example ``"master"`` or ``"v2.0.1"`



.. code-block:: python

   linkcode_url: str

The link to your GitHub repository formatted as ``https://github.com/user/repo``
- If not provided, will attempt to create the link from the ``html_context`` dict


.. code-block:: python

    linkcode_link_text: str = "View on GitHub"

The text to use for the linkcode link


.. code-block:: python

   linkcode_resolve: types.FunctionType

A ``linkcode_resolve()`` function to use for resolving the link target

* Uses default :func:`~.linkcode_resolve` if not specified (recommended)


Components
~~~~~~~~~~~~~


|.linkcode_resolve|_
|.add_linkcode_node_class|_

* TDKStyle - Pygments Style for syntax highlighting similar to Github Pretty Lights Dark Theme
* TDKMethLexor - Pygments Lexor to add syntax highlighting to methods
* |.linkcode_resolve|_ - to link to GitHub source code using ``sphinx.ext.linkcode``
* |.add_linkcode_node_class|_ - adds a new ``linkcode-link`` class, allowing for CSS styling separately from ``viewcode`` links
* ``github_style.css`` - CSS styling for linkcode links (icon + text)


Config Values


.. code-block:: python

    linkcode_blob: str = any('last_tag', 'head')
    linkcode_link_text: str = "View on GitHub"
    linkcode_url: str = "https://github.com/tdkorn/sphinx-github-style"
    linkcode_resolve: func = None


linkcode_default_blob: str = any('last_tag', 'master', 'head')


