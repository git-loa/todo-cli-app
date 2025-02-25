#!/usr/bin/python3
""" "
setup.py - This module sets up the package using setuptools.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="todo-cli-app",
    version="0.1.0",
    author="Leonard Okyere Afeke",
    author_email="leo.afeke@outlook.com",
    description="A command-line to-d list application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/git-loa/todo-cli-app",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "psycopg2",
        # Add other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "todo=main:cli_main",  # This is the entry point.
        ]
    },
    classifiers=[
        "Progamming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
