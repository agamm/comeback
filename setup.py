from setuptools import setup


setup(
    name='comeback',
    version='0.0.1',
    py_modules=['src'],
    license="MIT",
    install_requires=[
        'click',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': ['comeback=src.main:cli'],
    },
)