#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['pandas',
               'openpyxl',
               'numpy',
               'matplotlib>=3.5.0',
               'wntr',
               'imageio',
               'imageio-ffmpeg',
               'networkx>=2.7,<=3.3']

test_requirements = [ ]

setup(
    author="Tyler Trimble",
    author_email='TylerL.Trimble@gmail.com',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
            ],
    description="A python package for easy generation and customization of water network graphs.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='viswaternet',
    name='viswaternet',
    packages=find_packages(include=['viswaternet', 'viswaternet.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/tylertrimble/viswaternet',
    version='2.2.2',
    zip_safe=False,
)
