import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

this_directory = pathlib.Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="ssynth_logger",
    packages=find_packages(),
    version="0.0.1",
    description="A logger wrapper for Smartnoise Synth Table Transformer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dscc-admin/lomas/",
    author="Data Science Competence Center, Swiss Federal Statistical Office",
    author_email="dscc@bfs.admin.ch",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
    ],
    keywords=["smartnoise-synth", "logger", "serialiser", "deserialiser"],
    python_requires=">=3.10, <4",
    install_requires=[
        "smartnoise-synth==1.0.4",
    ],
)
