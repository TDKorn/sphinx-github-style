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
import re
import sys
import inspect
import subprocess
import pkg_resources

root = os.path.abspath('../../')
modpath = root
modname = os.path.basename(modpath)

# ============================== Build Environment ==============================

# Build behaviour is dependent on environment
on_rtd = os.environ.get('READTHEDOCS') == 'True'

# Configure paths
sys.path.append(os.path.abspath('.'))
sys.path.insert(0, root)

# on_rtd = True  # Uncomment for testing RTD builds locally


# ============================ Project information ============================

author = 'Adam Korn'
copyright = '2023, Adam Korn'
project = 'sphinx-github-style'
repo = project

# Package Info
pkg = pkg_resources.require(modname)[0]
pkg_name = pkg.get_metadata('top_level.txt').strip()

# Simplify things by using the installed version
version = pkg_resources.require(modname)[0].version
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
from sphinx_github_style.github_style import TDKStyle
# Add custom Pygments style if HTML
if 'html' in sys.argv:
    pygments_style = 'sphinx_github_style.github_style.TDKStyle'
else:
    pygments_style = 'sphinx'

# ============================ Extensions ====================================

# Add any Sphinx extension module names here, as strings
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.viewcode',
    'sphinx.ext.linkcode',
    'sphinx_github_style',
]

# ====================== Extra Settings for Extensions ========================

# ~~~~ InterSphinx ~~~~
# Add references to Python, Requests docs
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'requests': ('https://requests.readthedocs.io/en/latest/', None),
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

# Shorten type hints
python_use_unqualified_type_names = True


# ~~~~~~~~ Readcode Settings ~~~~~~~~~
#
def read(file):
    with open(file, 'r', encoding='utf-8') as f:
        return f.read()


# Source file(s) to convert for GitHub README/PyPi description
#
rst_files = []
# list(map(
#     os.path.abspath,
#     ('README.rst', 'README_PyPi.rst', 'changelog.rst')))

# Mapping of {"abs/path/to/file.rst": "File contents"}
#
readcode_sources = {rst_file: read(rst_file) for rst_file in rst_files}

# Directory to save the final converted output to
#
readcode_build_dir = root
#
# [Optional] dict of {'ref': 'external_link'} to replace relative links
# like :ref:`ref` with an `ref <external_link>`_ (ex. for PyPi)
#
readcode_refs = {
    "string": "https://domain.com"
}

linkcode_default_blob = 'last_tag'

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

# html_logo = "_static/logo.png"

# ============================ Linkcode Extension Settings ============================
#
#
#                     Adapted from https://github.com/nlgranger/SeqTools
#
#
# The text to use for linkcode source code links (from sphinx-github-style)
linkcode_link_text = "View on GitHub"

# Get the blob to link to on GitHub
#
linkcode_revision = "master"

try:
    # lock to commit number
    cmd = "git log -n1 --pretty=%H"
    head = subprocess.check_output(cmd.split()).strip().decode('utf-8')
    linkcode_revision = head

    # if we have a tag, use tag as reference
    cmd = "git describe --exact-match --tags " + head
    tag = subprocess.check_output(cmd.split(" ")).strip().decode('utf-8')
    linkcode_revision = tag

except subprocess.CalledProcessError:
    try:
        if linkcode_default_blob == 'last_tag':
            cmd = "git describe --tags --abbrev=0"
            tag = subprocess.check_output(cmd.split(" ")).strip().decode('utf-8')
            linkcode_revision = tag

    except subprocess.CalledProcessError:
        pass



# Set the "Edit on GitHub" link to use the current commit
html_context = {
    'display_github': True,
    'github_user': 'TDKorn',
    'github_repo': repo,
    'github_version': f'{linkcode_revision}/docs/source/'
}

# Source URL template; formatted + returned by linkcode_resolve
linkcode_url = f"https://github.com/tdkorn/{repo}/blob/" \
               + linkcode_revision + "/{filepath}#L{linestart}-L{linestop}"
user = html_context['github_user']
l="https://github.com/{user}/{repo}/tree/{linkcode_revision}/{pkg}/{file}.py#L{start}-L{finish}}"

def linkcode_resolve(domain, info):
    """Returns a link to the source code on GitHub, with appropriate lines highlighted

    Adapted from https://github.com/nlgranger
    """
    if domain != 'py' or not info['module']:
        return None

    modname = info['module']
    fullname = info['fullname']

    submod = sys.modules.get(modname)
    if submod is None:
        print(f'No submodule found for {fullname}')
        return None

    obj = submod
    for part in fullname.split('.'):
        try:
            obj = getattr(obj, part)
            print(obj)
        except Exception:
            print(f'error getting part? obj = {obj}, part = {part})')
            return None

    try:
        filepath = os.path.relpath(inspect.getsourcefile(obj), modpath)
        if filepath is None:
            print(f'No filepath found for {obj} in module {modpath}...?')
            return
    except Exception as e:
        return print(  # ie. None
            f'Exception raised while trying to retrieve module path for {obj}:',
            e, sep='\n'
        )

    try:
        source, lineno = inspect.getsourcelines(obj)
    except OSError:
        print(f'failed to get source lines for {obj}')
        return None
    else:
        linestart, linestop = lineno, lineno + len(source) - 1

    # Format link using the filepath of the source file plus the line numbers
    # Fix links with "../../../" or "..\\..\\..\\"
    filepath = '/'.join(filepath[filepath.find(modname):].split('\\'))

    # Example of final link: # https://github.com/tdkorn/my-magento/blob/sphinx-docs/magento/utils.py#L355-L357
    final_link = linkcode_url.format(
        filepath=filepath,
        linestart=linestart,
        linestop=linestop
    )
    print(f"Final Link for {fullname}: {final_link}")

    # Use the link to replace directives with links in the README for GitHub/PyPi
    if not on_rtd:
        for rst_src in readcode_sources:
            replace_autodoc_refs_with_linkcode(
                info=info,
                link=final_link,
                rst_src=rst_src
            )
    return final_link


def replace_autodoc_refs_with_linkcode(info: dict, link: str, rst_src: str):
    """Replaces Sphinx autodoc cross-references in a .rst file with linkcode links to highlighted GitHub source code

    Essentially turns your GitHub README into Sphinx-like documentation contained fully within the repository


    =================================  By https://github.com/TDKorn  =====================================


    For example, :meth:`~.InstaClient.get_user` would be rendered in HTML as an outlined "get_user()" link
    that contains an internal reference to the corresponding documentation entry (assuming it exists)

    We love it, it's great. Fr. But it's ugly and useless on GitHub and PyPi. Literally so gross.

    This function replaces cross-references in the ``rst_src`` file with the links generated by linkcode,
    which take you to the source file and highlight the full definition of the class/method/function/target

    .. note:: links are of the format https://github.com/user/repo/blob/branch/package/file.py#L30-L35

        For example,
        `get_user() <https://github.com/TDKorn/insta-tweet/blob/master/InstaTweet/instaclient.py#L48-L71>`_


    :param info: the info dict from linkcode_resolve
    :param link: link to the highlighted GitHub source code, generated by linkcode
    :param rst_src: the .rst file to use as the initial source of content
    """
    # Get raw rst from rst_sources dict
    rst = readcode_sources[rst_src]

    # Use the linkcode data that was provided to see what the reference target is
    # Ex:  Class.[method] // module.[function] // [function]
    ref_name = info['fullname'].split('.')[-1]

    # The rst could have :meth:`~.method` or :meth:`~.Class.method` or :class:`~.Class` or...
    # Regardless, there's :directive:`[~][module|class][.]target` where [] is optional
    pattern = rf":\w+:`~?\.?\w?\.{ref_name}`"

    # See if there's any reference in the rst, and figure out what it is
    if match := re.findall(pattern, rst):
        directive = match[0].split(':')[1]
    else:
        return None

    # Format the name of methods
    if directive == 'meth':
        ref_name += "()"

    # Format the link -> `method() <https://www.github.com/.../file.py#L10-L19`_
    rst_link = f"`{ref_name} <{link}>`_"

    # Then take the link and sub that hoe in!!
    readcode_sources[rst_src] = re.sub(pattern, rst_link, rst)

    print(f'Added reST links for {ref_name}: {rst_link}')
    return {'info': info, 'rst_link': rst_link}


# ---- Methods for "build-finished" Core Event ----------------------


def replace_rst_refs(rst: str, refs: dict) -> str:
    """Post-processes the generated rst, replacing :ref: with external links (ex. for PyPi)

    :param rst: the text of the .rst file
    :param refs: dict of {'reference': 'external_link'}
    :return: the processed rst text
    """
    for ref, external_link in refs.items():
        rst = re.sub(
            pattern=rf":ref:`{ref}`",
            repl=f"`{ref} <{external_link}>`_",
            string=rst
        )
    return rst


def replace_rst_images(rst: str) -> str:
    """Post-processes the generated rst, replacing relative image paths with external RTD links

    Probably temporary until I write a proper function that adjusts the paths when moving to ``rst_out``

    :param rst: the text of the .rst file
    :return: the processed rst text
    """
    return re.sub(
        # pattern .. image:: {..}/_static/(filename.ext)
        pattern=r".. image:: \S+_static/(\w+\.\w{3,4})",
        repl=r".. image:: https://instatweet.readthedocs.io/en/latest/_images/\1",
        string=rst
    )


def save_generated_rst_files(app, exception):
    """Saves the final rst text to files in the ``rst_out_dir``"""
    if not os.path.exists(readcode_build_dir):
        os.mkdir(readcode_build_dir)

    outdir = os.path.abspath(readcode_build_dir)

    for src, rst in readcode_sources.items():
        rst = replace_rst_images(rst)
        if readcode_refs:
            rst = replace_rst_refs(rst, readcode_refs)
        with open(out := os.path.join(outdir, src),
                  'w', encoding='utf-8') as f:
            f.write(rst)
        print(f'Saved `readcode` file for {src}: {out}')

def change_directives(rst):
    """set default_role to 'py:obj' -> remove all :[class |

    :return:
    """
    pattern = r':(\bmod\b|\bfunc\b|\bclass\b|\bmeth\b|\battr\b):'
    return re.sub(pattern, '', rst)


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
    # if not on_rtd:  # and full remake was done?
    #     app.connect('build-finished', save_generated_rst_files)
    app.connect('autodoc-skip-member', skip)
    app.add_css_file("github_linkcode.css")
