.. |.github_style| replace:: ``github_style.css``
.. _.github_style: https://github.com/tdkorn/sphinx-github-style/tree/v1.0.0/sphinx_github_style/_static/github_style.css

CSS Styling for Linkcode Links
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: sphinx_github_style.add_linkcode_class
   :members:
   :undoc-members:
   :exclude-members: setup


The |.github_style|_ StyleSheet
==================================

Links are styled as follows:


.. literalinclude:: ../../sphinx_github_style/_static/github_style.css
   :language: css



To make the ``viewcode-link`` links match with the ``linkcode-link`` links,
add the following to your ``custom.css`` file:

.. code-block:: css

    /* Change viewcode "[source]" link position and colour to match linkcode */
    .rst-content .viewcode-back, .rst-content .viewcode-link {
        color: #00e;
        padding-left: 12px;
    }