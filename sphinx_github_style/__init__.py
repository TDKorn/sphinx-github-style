import os
import sys
import sphinx
import inspect
import subprocess
import pkg_resources
from pathlib import Path
from typing import Dict, Any, Optional
from sphinx.application import Sphinx
from sphinx.errors import ExtensionError

__version__ = "0.0.1b8"
__author__ = 'Adam Korn <hello@dailykitten.net>'

from .add_linkcode_class import add_linkcode_node_class
from .meth_lexer import TDKMethLexer
from .github_style import TDKStyle


def setup(app: Sphinx) -> Dict[str, Any]:
    modpath = os.path.abspath('../')
    modname = os.path.basename(modpath)
    pkg = pkg_resources.require(modname)[0]
    pkg_name = pkg.get_metadata('top_level.txt').strip()

    app.connect("builder-inited", get_static_path)
    # app.connect('build-finished', save_generated_rst_files)

    app.add_config_value('pkg_name', pkg_name, 'html')
    app.add_config_value('linkcode_blob', 'master', True)

    app.setup_extension('sphinx_github_style.add_linkcode_class')
    app.setup_extension('sphinx_github_style.github_style')
    app.setup_extension('sphinx_github_style.meth_lexer')
    app.setup_extension('sphinx.ext.linkcode')

    app.config.html_context['github_version'] = get_linkcode_revision(app)

    linkcode_url = get_linkcode_url(app)
    linkcode_func = getattr(app.config, 'linkcode_resolve', None)

    if not linkcode_func or not callable(linkcode_func):
        print("Function `linkcode_resolve` is not given in conf.py; "
              "using default function from ``sphinx_github_style``")

        def linkcode_resolve(domain, info):
            """Returns a link to the source code on GitHub, with appropriate lines highlighted

            :By:
                Adam Korn (https://github.com/tdkorn)
            :Adapted From:
                nlgranger/SeqTools (https://github.com/nlgranger/seqtools/blob/master/docs/conf.py)
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
                except Exception:
                    return None

            try:
                filepath = os.path.relpath(inspect.getsourcefile(obj), modpath)
                if filepath is None:
                    return
            except Exception:
                return None

            try:
                source, lineno = inspect.getsourcelines(obj)
            except OSError:
                print(f'failed to get source lines for {obj}')
                return None
            else:
                linestart, linestop = lineno, lineno + len(source) - 1

            # Fix links with "../../../" or "..\\..\\..\\"
            filepath = '/'.join(filepath[filepath.find(pkg_name):].split('\\'))

            # Example: https://github.com/TDKorn/my-magento/blob/docs/magento/models/model.py#L28-L59
            final_link = linkcode_url.format(
                filepath=filepath,
                linestart=linestart,
                linestop=linestop
            )
            print(f"Final Link for {fullname}: {final_link}")
            return final_link

        linkcode_func = linkcode_resolve

    app.config.linkcode_resolve = linkcode_func
    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}


def get_static_path(app):
    app.config.html_static_path.append(
        str(Path(__file__).parent.joinpath("_static").absolute())
    )


def get_linkcode_url(app: Sphinx) -> str:
    """Template for linking to highlighted GitHub source code

    Formatted into a final link by :meth:`~.linkcode_resolve`
    """
    if (url := app.config._raw_config.get("linkcode_url")) is None:
        raise ExtensionError("Config value ``linkcode_url`` is missing")
    url = f"{url.rstrip('/')}/blob/{get_linkcode_revision(app)}/"
    url += "{filepath}#L{linestart}-L{linestop}"
    return url


def get_linkcode_revision(app: Sphinx):
    """Get the blob to link to on GitHub

    .. admonition:: Linkcode Blobs

       The generated links will use the conf.py value of ``linkcode_blob``

       * ``"head"`` - most recent commit hash; if this commit is tagged, uses the tag instead
       * ``"last_tag" - the most recently tagged commit
       *  "{blob}" - any blob (ex. ``"master"``, ``"v2.1.0b0"``)
    """
    blob = getattr(app.config, "linkcode_blob", "master")
    if blob == "head":
        return get_head()
    if blob == 'last_tag':
        return get_last_tag()
    # Link to the branch/tree/blob you provided, ex. "master"
    return blob


def get_head(errors: bool = False) -> Optional[str]:
    """Gets the most recent commit hash or tag

    :raises subprocess.CalledProcessError: if the commit can't be found and ``errors`` is set to ``True``
    """
    cmd = "git log -n1 --pretty=%H"
    try:
        # get most recent commit hash
        head = subprocess.check_output(cmd.split()).strip().decode('utf-8')

        # if head is a tag, use tag as reference
        cmd = "git describe --exact-match --tags " + head
        try:
            tag = subprocess.check_output(cmd.split(" ")).strip().decode('utf-8')
            return tag

        except subprocess.CalledProcessError:
            return head

    except subprocess.CalledProcessError as e:
        # Raise error
        if errors:
            raise RuntimeError from e
        else:
            return None


def get_last_tag():
    """Get the most recent commit tag"""
    try:
        cmd = "git describe --tags --abbrev=0"
        return subprocess.check_output(cmd.split(" ")).strip().decode('utf-8')

    except subprocess.CalledProcessError as e:
        raise RuntimeError("No tags exist for the repo...(?)") from e
