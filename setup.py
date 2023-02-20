import os
from pathlib import Path
from setuptools import setup, find_packages

LONG_DESCRIPTION_SRC = 'README.rst'


def read(file):
    with open(os.path.abspath(file), 'r', encoding='utf-8') as f:
        return f.read()


def get_version():
    file = os.path.abspath(os.path.join('sphinx_github_style', '__init__.py'))
    for line in read(file).split('\n'):
        if line.startswith("__version__ ="):
            return line.split(" = ")[-1].strip('"')


setup(
    name="sphinx-github-style",
    version=get_version(),
    description="Sphinx Github Integration and Github Dark Theme Pygments Style",
    long_description=read(LONG_DESCRIPTION_SRC),
    long_description_content_type="text/x-rst; charset=UTF-8",
    author="Adam Korn",
    author_email='hello@dailykitten.net',
    license="MIT License",
    packages=find_packages(),
    keywords=["sphinx", "sphinx-extension", "sphinx-theme", "pygments", "pygments-style", "github", "linkcode"],
    url="https://github.com/tdkorn/sphinx-github-style",
    download_url="https://github.com/TDKorn/sphinx-github-style/tarball/master",
    package_data={
        "sphinx_github_style": [
            "_static/github_style.css",
        ],
    },
    classifiers=[
        "Framework :: Sphinx :: Extension",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=["sphinx>=1.8"],
)
