from setuptools import setup, find_packages

setup(
    author='Ryan Horiguchi',
    author_email='ryan.horiguchi@gmail.com',
    dependency_links=[],
    entry_points={
        'console_scripts': ['tv_time_export = tv_time_export.__main__:main'],
    },
    install_requires=[
        'PyYAML==6.0',
        'beautifulsoup4==4.11.1',
        'charset-normalizer==1.3.3',
        'requests==2.27.1',
        'retrying==1.3.3'
    ],
    license='AGPL-3.0',
    name='tv_time_export',
    packages=find_packages(),
    python_requires='>=3.7',
    url='git@github.com:rhoriguchi/tv_time_export.git',
    version='1.0.18',
    zip_safe=False,
)
