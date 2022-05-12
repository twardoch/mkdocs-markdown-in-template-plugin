#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

from setuptools import find_packages, setup

NAME = "mkdocs-markdown-in-template-plugin"
PY_NAME = NAME.replace("-", "_")


def get_absolute_path(*args):
    """Transform relative pathnames into absolute pathnames."""
    directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(directory, *args)


with open(get_absolute_path("README.md")) as f:
    long_description = f.read()


def get_version(*args):
    verstrline = open(get_absolute_path(PY_NAME, "__init__.py"), "rt").read()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        return mo.group(1)
    return "undefined"


def get_requirements(*args):
    """Get requirements from pip requirement files."""
    requirements = set()
    with open(get_absolute_path(*args)) as handle:
        for line in handle:
            # Strip comments.
            line = re.sub(r"^#.*|\s#.*", "", line)
            # Ignore empty lines
            if line and not line.isspace():
                requirements.add(re.sub(r"\s+", "", line))
    return sorted(requirements)


setup(
    name=f"{NAME}",
    version=get_version(),
    description="A MkDocs plugin that lets you use Markdown inside the theme's Jinja2 template files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[
        "mkdocs",
        "jinja",
        "markdown",
        "theme",
        "template",
    ],
    url=f"https://github.com/twardoch/{NAME}",
    author="Adam Twardoch",
    author_email="adam+github@twardoch.com",
    license="MIT",
    python_requires=">=3.9",
    install_requires=get_requirements("requirements.txt"),
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
    ],
    entry_points={
        "mkdocs.plugins": [
            f"markdown-in-template = {PY_NAME}.plugin:MarkdownInTemplatePlugin"
        ]
    },
)
