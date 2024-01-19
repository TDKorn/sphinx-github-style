# docs/source/conf.py
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
#
# List of Options from RTD:
# https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html
#

# ================================== Imports ==================================

import os
import sys
import pkg_resources


# ============================== Build Environment ==============================

# Build behaviour is dependent on environment
on_rtd = os.environ.get('READTHEDOCS') == 'True'

# Configure paths
root = os.path.abspath('../../')
sys.path.append(os.path.abspath('.'))
sys.path.insert(0, root)

# on_rtd = True  # Uncomment for testing RTD builds locally


# ============================ Project information ============================

author = 'Adam Korn'
copyright = '2023, Adam Korn'
project = 'sphinx-github-style'
repo = project

# Package Info
pkg = pkg_resources.require(project)[0]
pkg_name = pkg.get_metadata('top_level.txt').strip()

# Simplify things by using the installed version
version = pkg.version
release = version

# ======================== General configuration ============================

# Doc with root toctree
master_doc = 'contents'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Source File type
source_suffix = [
    '.rst',
    # '*.ipynb',
]

# LaTeX settings
latex_elements = {  # Less yucky looking font
    'preamble': r'''
\usepackage[utf8]{inputenc}
\usepackage{charter}
\usepackage[defaultsans]{lato}
\usepackage{inconsolata}
''',
}

# ============================ HTML Theme Settings ============================

# The theme to use for HTML and HTML Help pages.
html_theme = 'sphinx_rtd_theme'

# Theme Options
# https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html#theme-options
#
html_theme_options = {
    # Add the [+] signs to nav
    'collapse_navigation': False,
    # Prev/Next buttons also placed at the top bc it'd be cruel not to
    'prev_next_buttons_location': 'both',
}

html_logo = "_static/logo_square.ico"

# Set the "Edit on GitHub" link to use the current commit
html_context = {
    'display_github': True,
    'github_user': 'TDKorn',
    'github_repo': repo,
}

if 'html' not in sys.argv:
    pygments_style = 'sphinx'

if not on_rtd:
    site_url = "https://tdkorn.github.io/sphinx-github-style/"

html_baseurl = "https://sphinx-github-style.readthedocs.io/en/latest/"

sitemap_url_scheme = "{link}"
# ============================ Extensions ====================================

# Add any Sphinx extension module names here, as strings
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.viewcode',
    'sphinx.ext.linkcode',
    'sphinx_github_style',
    'sphinx_inlinecode',
    'sphinx_sitemap',
    'sphinx_readme',
]

# ====================== Extra Settings for Extensions ========================

# ~~~~ InterSphinx ~~~~
# Add references to Python, Requests docs
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'requests': ('https://requests.readthedocs.io/en/latest/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}

# ~~~~ AutoSectionLabel ~~~~
# Make sure the target is unique
autosectionlabel_prefix_document = True

# ~~~~ Autodoc ~~~~
# Order based on source
autodoc_member_order = 'bysource'
#
# Remove typehints from method signatures and put in description instead
autodoc_typehints = 'description'
#
# Only add typehints for documented parameters (and all return types)
#  ->  Prevents parameters being documented twice for both the class and __init__
autodoc_typehints_description_target = 'documented_params'
#
# Shorten type hints
python_use_unqualified_type_names = True


# ~~~~ Sphinx GitHub Style ~~~~
#
# Blob to use when linking to GitHub source code
if on_rtd:
    linkcode_blob = 'last_tag'
else:
    # For gh-pages use master
    linkcode_blob = 'master'
    # For sphinx_readme image links in README
    readme_blob = 'last_tag'

# Text to use for the linkcode link
linkcode_link_text = "View on GitHub"

# Source URL template; formatted + returned by linkcode_resolve
linkcode_url = f"https://github.com/{html_context['github_user']}/{repo}"


# ~~~~ Sphinx README ~~~~
#
# Blob to use when linking to GitHub source code
readme_src_files = 'README.rst'

readme_docs_url_type = 'html'

# Settings to uncomment when generating PyPi README

# readme_tags = ["pypi"]
#
# readme_raw_directive = False
#
# readme_inline_markup = False


# ---- Skip and Setup Method -------------------------------------------------


def skip(app, what, name, obj, would_skip, options):
    """Include __init__ as a documented method

    For classes:

        >>> if not obj.__qualname__.startswith("ClassName"):
        >>>     return False
    """
    if name in ('__init__',):
        return False
    return would_skip


def setup(app):
    from sphinx.domains.python import PyField
    from sphinx.util.docfields import Field
    from sphinx.locale import _

    app.connect('autodoc-skip-member', skip)
    app.add_css_file("custom.css")
    app.add_object_type(
        'confval',
        'confval',
        objname='configuration value',
        indextemplate='pair: %s; configuration value',
        doc_field_types=[
            PyField(
                'type',
                label=_('Type'),
                has_arg=False,
                names=('type',),
                bodyrolename='class'
            ),
            Field(
                'default',
                label=_('Default'),
                has_arg=False,
                names=('default',),
            ),
        ]
    )