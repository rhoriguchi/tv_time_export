import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'requirements.txt')) as f:
    requires = f.read().splitlines()

setup(
    author='Ryan Horiguchi',
    author_email='ryan.horiguchi@gmail.com',
    dependency_links=[],
    install_requires=requires,
    license='unlicense',
    name='tv_time_export',
    packages=find_packages(),
    python_requires='>=3.7',
    url='git@github.com:rhoriguchi/tv_time_export.git',
    version='1.0.0',
    zip_safe=False,
)
