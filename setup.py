#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setup_requirements = ['pytest-runner', ]

test_requirements = [
    'pytest>=6',
    "pytest-cov>=2",
]

setup(
    author="Robert Alexander",
    author_email='raalexander.phi@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description="A ctypes wrapper for Windows Semaphore Objects",
    install_requires=[],
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='semaphore_win_ctypes',
    name='semaphore_win_ctypes',
    packages=find_packages(include=[
        'semaphore_win_ctypes',
        'semaphore_win_ctypes.*'
    ]),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ralexander-phi/semaphore_win_ctypes',
    version='0.1.2',
    zip_safe=False,
)
