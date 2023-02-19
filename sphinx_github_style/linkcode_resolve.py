#! sphinx_github_style/linkcode_resolve.py

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
    pass


# Add the "Edit on GitHub" link at the top
html_context = {
    'display_github': True,
    'github_user': 'TDKorn',
    'github_repo': 'insta-tweet',
    'github_version': f'{linkcode_revision}/docs/source/'
}

# Source URL template; formatted + returned by linkcode_resolve
linkcode_url = "https://github.com/tdkorn/insta-tweet/blob/" \
               + linkcode_revision + "/{filepath}#L{linestart}-L{linestop}"

# Hardcoded Top Level Module Path // since InstaTweet isn't PyPi release name :(  it could be tho...
modpath = pkg_resources.require('insta-tweet')[0].location


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
    if on_rtd:
        # Ex. InstaTweet\instatweet.py --> InstaTweet/instatweet.py
        filepath = '/'.join(filepath.split('\\'))

    else:
        # For local builds, I must be doing something wrong because the
        # paths are always like "..\..\..\InstaTweet\module.py"
        filepath = '/'.join(filepath.lstrip('..\\').split('\\'))

    # Example of final link: https://github.com/tdkorn/insta-tweet/blob/docs/InstaTweet/instatweet.py#L73-L117
    final_link = linkcode_url.format(
        filepath=filepath,
        linestart=linestart,
        linestop=linestop
    )
    print(f"Final Link for {fullname}: {final_link}")
    replace_autodoc_refs_with_linkcode(
        info=info,
        link=final_link,
        rst_src=rst_src,
    )
    return final_link

