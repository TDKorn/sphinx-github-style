# ============================ Linkcode Extension Settings ============================
#
#                     Adapted from https://github.com/nlgranger/SeqTools
#
#
import inspect
import os
import subprocess
import sys

import pkg_resources

# Get the blob to link to on GitHub
linkcode_revision = "master"

# Get the most recent tag to link to on GitHub
# try:
#     cmd = "git describe --tags --abbrev=0"
#     tag = subprocess.check_output(cmd.split(" ")).strip().decode('utf-8')
#     linkcode_revision = tag
#
# except subprocess.CalledProcessError:
#     linkcode_revision = "main"

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
    pass


# Set GitHub version to be same as linkcode
html_context['github_version'] = linkcode_revision

# Source URL template; formatted + returned by linkcode_resolve
linkcode_url = "https://github.com/tdkorn/my-magento/blob/" \
               + linkcode_revision + "/{filepath}#L{linestart}-L{linestop}"
"https://github.com/{user}/{repo}/tree/{linkcode_revision}/{pkg}/{file}.py#L{start}-L{finish}}"

# Hardcoded Top Level Module Path since MyMagento isn't PyPi release name
modpath = pkg_resources.require('my-magento')[0].location

# Top Level Package Name
top_level = 'magento'  # pkg_resources.require('my-magento')[0].get_metadata('top_level.txt').strip()



def linkcode_resolve(domain, info):
    """Returns a link to the source code on GitHub, with appropriate lines highlighted

    Adapted from https://github.com/nlgranger (ily)
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
    filepath = '/'.join(filepath[filepath.find(top_level):].split('\\'))

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
