"""
Setup configuration for MorphUI
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("morphui/__init__.py", "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break

setup(
    name="morphui",
    version=version,
    author="j4ggr",
    author_email="",
    description="A creative and flexible UI extension for Kivy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/j4ggr/MorphUI",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
    ],
    python_requires=">=3.7",
    install_requires=[
        "kivy>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
        ],
    },
    keywords="kivy ui widgets gui mobile desktop",
    project_urls={
        "Bug Reports": "https://github.com/j4ggr/MorphUI/issues",
        "Source": "https://github.com/j4ggr/MorphUI",
    },
)