import os
import sys
import inspect
import subprocess
import pkg_resources
from typing import Dict, Any
from sphinx.application import Sphinx
import sphinx

__version__ = "0.0.1b4"
__author__ = 'Adam Korn <hello@dailykitten.net>'


from .github_style import TDKStyle
from .meth_lexer import TDKMethLexer
from .add_linkcode_class import add_linkcode_node_class


def setup(app: Sphinx) -> Dict[str, Any]:
    # Package Info
    modpath = os.path.abspath('../')
    modname = os.path.basename(modpath)
    pkg = pkg_resources.require(modname)[0]
    pkg_name = pkg.get_metadata('top_level.txt').strip()

    app.connect('doctree-resolved', add_linkcode_node_class)
    # app.connect('build-finished', save_generated_rst_files)

    app.add_config_value('linkcode_link_text', '[source]', 'html')
    app.add_config_value('linkcode_default_blob', 'master', 'html')

    app.add_css_file('github_linkcode.css')
    app.add_lexer('TDK', TDKMethLexer)

    app.setup_extension('sphinx.ext.linkcode')

    app.config.pygments_style = 'sphinx_github_style.TDKStyle'
    app.config.html_context['github_version'] = get_linkcode_revision(app)

    linkcode_url = get_linkcode_url(app)
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
            return None

        obj = submod
        for part in fullname.split('.'):
            try:
                obj = getattr(obj, part)
                print(obj)
            except Exception:
                return None

        try:
            filepath = os.path.relpath(inspect.getsourcefile(obj), modpath)
            if filepath is None:
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
        print("Filepath: ", filepath)
        filepath = '/'.join(filepath[filepath.find(pkg_name):].split('\\'))

        # Example of final link: # https://github.com/tdkorn/my-magento/blob/sphinx-docs/magento/utils.py#L355-L357
        final_link = linkcode_url.format(
            filepath=filepath,
            linestart=linestart,
            linestop=linestop
        )
        print(f"Final Link for {fullname}: {final_link}")

        # Use the link to replace directives with links in the README for GitHub/PyPi
        # if not on_rtd:
        #     for rst_src in rst_sources:
        #         replace_autodoc_refs_with_linkcode(
        #             info=info,
        #             link=final_link,
        #             rst_src=rst_src
        #         )
        return final_link

    app.config.linkcode_resolve = linkcode_resolve
    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}


def get_linkcode_revision(app: Sphinx):
    # Get the blob to link to on GitHub
    linkcode_revision = "master"

    try:
        # lock to commit number
        cmd = "git log -n1 --pretty=%H"
        head = subprocess.check_output(cmd.split()).strip().decode('utf-8')
        linkcode_revision = head

        # if we are on master's HEAD, use master as reference
        cmd = "git log --first-parent master -n1 --pretty=%H"
        master = subprocess.check_output(cmd.split()).strip().decode('utf-8')
        if head == master:
            linkcode_revision = "master"

        # if we have a tag, use tag as reference
        cmd = "git describe --exact-match --tags " + head
        tag = subprocess.check_output(cmd.split(" ")).strip().decode('utf-8')
        linkcode_revision = tag


    except subprocess.CalledProcessError:
        if app.config._raw_config.get('linkcode_default_blob') == 'last_tag':
            # Get the most recent tag to link to on GitHub
            try:
                cmd = "git describe --tags --abbrev=0"
                last_tag = subprocess.check_output(cmd.split(" ")).strip().decode('utf-8')
                linkcode_revision = last_tag

            except subprocess.CalledProcessError:
                linkcode_revision = "master"

    return linkcode_revision


def get_linkcode_url(app):
    if not (url := app.config._raw_config.get("linkcode_url")):
       raise ValueError("conf.py missing value for ``linkcode_url``")

    # Source link template; formatted by linkcode_resolve
    return f"{url.rstrip('/')}/blob/{get_linkcode_revision(app)}/" + \
           "{filepath}#L{linestart}-L{linestop}"

