# - *- coding: utf- 8 - *-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tcxreader",
    version="0.3.15",
    author="Alen Rajšp",
    author_email="alen.rajsp@gmail.com",
    description="tcxreader is a reader for Garmin’s TCX file format. It also works well with missing data!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alenrajsp/tcxreader",
    packages=setuptools.find_packages(exclude=['*tests*']),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    python_requires='>=3.6',
    test_suite="tests",
)
