import subprocess
from pathlib import Path
from sphinx.errors import ExtensionError


def get_head() -> str:
    """Gets the most recent commit hash or tag

    :return: The SHA or tag name of the most recent commit, or "master" if the call to git fails.
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

    except subprocess.CalledProcessError:
        print("Failed to get head")  # so no head?
        return "master"


def get_last_tag() -> str:
    """Get the most recent commit tag on the currently checked out branch

    :raises ExtensionError: if no tags exist on the branch
    """
    try:
        cmd = "git describe --tags --abbrev=0"
        return subprocess.check_output(cmd.split(" ")).strip().decode('utf-8')

    except subprocess.CalledProcessError:
        raise ExtensionError("``sphinx-github-style``: no tags found on current branch")


def get_repo_dir() -> Path:
    """Returns the root directory of the repository

    :return: A Path object representing the working directory of the repository.
    """
    try:
        cmd = "git rev-parse --show-toplevel"
        repo_dir = Path(subprocess.check_output(cmd.split(" ")).strip().decode('utf-8'))

    except subprocess.CalledProcessError as e:
        raise RuntimeError("Unable to determine the repository directory") from e

    return repo_dir
