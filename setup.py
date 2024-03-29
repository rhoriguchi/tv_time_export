from setuptools import setup, find_packages

setup(
    author='Ryan Horiguchi',
    author_email='ryan.horiguchi@gmail.com',
    dependency_links=[],
    entry_points={
        'console_scripts': ['tv_time_export = tv_time_export.__main__:main'],
    },
    install_requires=[
        'PyJWT==2.8.0',
        'PyYAML==6.0.1',
        'requests==2.31.0',
        'retrying==1.3.4'
    ],
    license='AGPL-3.0',
    name='tv_time_export',
    packages=find_packages(),
    python_requires='>=3.7',
    url='git@github.com:rhoriguchi/tv_time_export.git',
    version='1.0.24',
    zip_safe=False,
)
