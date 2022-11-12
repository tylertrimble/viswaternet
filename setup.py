#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['pandas',
               'numpy',
               'matplotlib>=3.5.0',
               'wntr',
               'imageio',
               'networkx']

test_requirements = [ ]

setup(
    author="Tyler Trimble",
    author_email='TylerL.Trimble@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A python package for easy generation and customization of water network graphs.",
    entry_points={
        'console_scripts': [
            'visnet=visnet.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='visnet',
    name='visnet',
    packages=find_packages(include=['visnet', 'visnet.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/tylertrimble/visnet',
    version='0.1.0',
    zip_safe=False,
)
