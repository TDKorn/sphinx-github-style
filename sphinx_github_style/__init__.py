import os
import sys
import sphinx
import inspect
import subprocess
import pkg_resources
from pathlib import Path
from sphinx.application import Sphinx
from sphinx.errors import ExtensionError
from typing import Dict, Any, Optional, Callable


__version__ = "0.0.1b16"
__author__ = 'Adam Korn <hello@dailykitten.net>'


from .add_linkcode_class import add_linkcode_node_class
from .meth_lexer import TDKMethLexer
from .github_style import TDKStyle


def setup(app: Sphinx) -> Dict[str, Any]:
    modpath = os.path.abspath('../')
    modname = os.path.basename(modpath)
    pkg = pkg_resources.require(modname)[0]
    pkg_name = pkg.get_metadata('top_level.txt').strip()

    app.connect("builder-inited", add_static_path)

    app.add_config_value('pkg_name', pkg_name, 'html')
    app.add_config_value('linkcode_blob', 'head', True)

    app.setup_extension('sphinx_github_style.add_linkcode_class')
    app.setup_extension('sphinx_github_style.github_style')
    app.setup_extension('sphinx_github_style.meth_lexer')
    app.setup_extension('sphinx.ext.linkcode')

    html_context = getattr(app.config, 'html_context', {})
    html_context['github_version'] = get_linkcode_revision(app)
    setattr(app.config, 'html_context', html_context)

    linkcode_url = get_linkcode_url(app)
    linkcode_func = get_conf_val(app, "linkcode_resolve")

    if not callable(linkcode_func):
        print(
            "Function `linkcode_resolve` not found in ``conf.py``; "
            "using default function from ``sphinx_github_style``"
        )
        linkcode_func = get_linkcode_resolve(
            linkcode_url, pkg_name, modpath
        )

    app.config.linkcode_resolve = linkcode_func
    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}


def add_static_path(app) -> None:
    """Add the path for the ``_static`` folder"""
    app.config.html_static_path.append(
        str(Path(__file__).parent.joinpath("_static").absolute())
    )


def get_linkcode_revision(app: Sphinx) -> str:
    """Get the blob to link to on GitHub

    .. note::

       The generated links depend on  the ``conf.py`` value of ``linkcode_blob``,
       which can be any of ``"head"``, ``"last_tag"``, or ``"{blob}"``

       * ``head`` (default): links to the most recent commit hash; if this commit is tagged, uses the tag instead
       * ``last_tag``: links to the most recently tagged commit; if no tags exist, uses ``head``
       * ``blob``: links to any blob you want, for example ``"master"`` or ``"v2.0.1"``
    """
    blob = get_conf_val(app, "linkcode_blob")
    if blob == "head":
        return get_head()
    if blob == 'last_tag':
        return get_last_tag()
    # Link to the branch/tree/blob you provided, ex. "master"
    return blob


def get_head(errors: bool = False) -> Optional[str]:
    """Gets the most recent commit hash or tag

    :raises subprocess.CalledProcessError: if the commit can't be found and ``errors`` is ``True``
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
        if errors:
            raise e
        else:
            return print("Failed to get head")  # so no head?


def get_last_tag() -> str:
    """Get the most recent commit tag

    :raises RuntimeError: if there are no tagged commits
    """
    try:
        cmd = "git describe --tags --abbrev=0"
        return subprocess.check_output(cmd.split(" ")).strip().decode('utf-8')

    except subprocess.CalledProcessError as e:
        raise RuntimeError("No tags exist for the repo...(?)") from e


def get_linkcode_url(app: Sphinx) -> str:
    """Get the template URL for linking to highlighted GitHub source code

    Formatted into the final link by ``linkcode_resolve()``
    """
    context = get_conf_val(app, "html_context")
    url = get_conf_val(app, "linkcode_url")

    if url is None:
        if context is None or not all(context.get(key) for key in ("github_user", "github_repo")):
            raise ExtensionError(
                "sphinx-github-style: config value ``linkcode_url`` is missing")
        else:
            print(
                "sphinx-github-style: config value ``linkcode_url`` is missing. "
                "Creating link from ``html_context`` values..."
            )
            blob = context['github_version']    # Added by setup() above
            url = f"https://github.com/{context['github_user']}/{context['github_repo']}/{blob}/"

    else:
        # URL should be "https://github.com/user/repo"
        url = url.strip("/") + f"/blob/{get_linkcode_revision(app)}/"

    url += "{filepath}#L{linestart}-L{linestop}"
    return url


def get_linkcode_resolve(linkcode_url: str, pkg_name: str, modpath: str) -> Callable:
    """Defines and returns a ``linkcode_resolve`` function for your package

    Used by default if ``linkcode_resolve`` isn't defined in ``conf.py``
    """
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

    return linkcode_resolve


def get_conf_val(app: Sphinx, attr: str, default: Any = None) -> Any:
    """Retrieve values from ``conf.py``

    Currently unclear why non-default ``conf.py`` values aren't being updated in the config attributes (?)
    So checking for values in the ``_raw_config`` dict first, since they *do* get updated
    """
    return app.config._raw_config.get(attr, getattr(app.config, attr, default))

