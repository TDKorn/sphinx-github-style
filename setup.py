import os
from pathlib import Path
from setuptools import setup, find_packages

LONG_DESCRIPTION_SRC = 'README_PyPi.rst'


def read(file):
    with open(os.path.abspath(file), 'r', encoding='utf-8') as f:
        return f.read()

# Parse version
init = Path(__file__).parent.joinpath("sphinx_github_style", "__init__.py")
for line in init.read_text().split("\n"):
    if line.startswith("__version__ ="):
        break
version = line.split(" = ")[-1].strip('"')

setup(
    name="sphinx-github-style",
    version=version,
    description="Sphinx Github Integration and Github Dark Theme Pygments Style",
    # long_description=read(LONG_DESCRIPTION_SRC),
    # long_description_content_type="text/x-rst; charset=UTF-8",
    author="Adam Korn",
    author_email='hello@dailykitten.net',
    license="MIT License",
    packages=find_packages(),
    url="https://github.com/tdkorn/sphinx-github-style",
    download_url="https://github.com/TDKorn/sphinx-github-style/tarball/master",
    keywords=["sphinx", "sphinx-extension", "sphinx-theme", "pygments", "pygments-style", "github", "linkcode"],
    # install_requires=["requests"],
    package_data={
        "sphinx_github_style": [
            "_static/github-linkcode.css",
            "add_linkcode_class.py",
             "github_style.py",
            "linkcode_resolve.py",
        # "sphinx_copybutton": [
        #     "_static/copybutton.css",
        #     "_static/copybutton_funcs.js",
        #     "_static/copybutton.js_t",
        #     "_static/copy-button.svg",
        #     "_static/check-solid.svg",
        #     "_static/clipboard.min.js",
        ]
    },
    classifiers=[
        "Framework :: Sphinx :: Extension",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3.7",
    install_requires=["sphinx>=1.8"],
    # extras_require={
    #     "code_style": ["pre-commit==2.12.1"],
    #     "rtd": [
    #         "sphinx",
    #         "ipython",
    #         "myst-nb",
    #         "sphinx-book-theme",
    #         "sphinx-examples",
    #     ],
    # },
)
