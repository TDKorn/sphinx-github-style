import sys
import inspect
from pathlib import Path
from functools import cached_property
from sphinx.errors import ExtensionError
from typing import Dict, Optional, Callable
from sphinx_github_style.utils.git import get_head, get_last_tag, get_repo_dir


def get_linkcode_revision(blob: str) -> str:
    """Get the blob to link to on GitHub

    .. note::

       The value of ``blob`` can be any of ``"head"``, ``"last_tag"``, or ``"{blob}"``

       * ``head`` (default): links to the most recent commit hash; if this commit is tagged, uses the tag instead
       * ``last_tag``: links to the most recent commit tag on the currently checked out branch
       * ``blob``: links to any blob you want, for example ``"master"`` or ``"v2.0.1"``
    """
    if blob == "head":
        return get_head()
    if blob == 'last_tag':
        return get_last_tag()
    # Link to the branch/tree/blob you provided, ex. "master"
    return blob


def get_linkcode_url(blob: Optional[str] = None, context: Optional[Dict] = None, url: Optional[str] = None) -> str:
    """Get the template URL for linking to highlighted GitHub source code with :mod:`sphinx.ext.linkcode`

    Formatted into the final link by a ``linkcode_resolve()`` function

    :param blob: The Git blob to link to
    :param context: The :external+sphinx:confval:`html_context` dictionary
    :param url: The base URL of the repository (ex. ``https://github.com/TDKorn/sphinx-github-style``)
    """
    if url is None:
        if context is None or not all(context.get(key) for key in ("github_user", "github_repo")):
            raise ExtensionError(
                "sphinx-github-style: config value ``linkcode_url`` is missing")
        else:
            print(
                "sphinx-github-style: config value ``linkcode_url`` is missing. "
                "Creating link from ``html_context`` values..."
            )
            url = f"https://github.com/{context['github_user']}/{context['github_repo']}"

    blob = get_linkcode_revision(blob) if blob else context.get('github_version')

    if blob is not None:
        url = url.strip("/") + f"/blob/{blob}/"  # URL should be "https://github.com/user/repo"
    else:
        raise ExtensionError(
            "sphinx-github-style: must provide a blob or GitHub version to link to")

    return url + "{filepath}#L{linestart}-L{linestop}"


def get_linkcode_resolve(linkcode_url: str, repo_dir: Optional[Path] = None) -> Callable:
    """Defines and returns a ``linkcode_resolve`` function for your package

    Used by default if ``linkcode_resolve`` isn't defined in ``conf.py``

    :param linkcode_url: The template URL to use when resolving cross-references with :mod:`sphinx.ext.linkcode`
    :param repo_dir: The root directory of the Git repository.
    """
    if repo_dir is None:
        repo_dir = get_repo_dir()

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
            except AttributeError:
                return None

        if isinstance(obj, property):
            obj = obj.fget
        elif isinstance(obj, cached_property):
            obj = obj.func

        try:
            modpath = inspect.getsourcefile(inspect.unwrap(obj))
            filepath = Path(modpath).relative_to(repo_dir)
            if filepath is None:
                return
        except Exception:
            return None

        try:
            source, lineno = inspect.getsourcelines(obj)
        except Exception:
            return None

        linestart, linestop = lineno, lineno + len(source) - 1

        # Example: https://github.com/TDKorn/my-magento/blob/docs/magento/models/model.py#L28-L59
        final_link = linkcode_url.format(
            filepath=filepath.as_posix(),
            linestart=linestart,
            linestop=linestop
        )
        print(f"Final Link for {fullname}: {final_link}")
        return final_link

    return linkcode_resolve
