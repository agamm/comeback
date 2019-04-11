from setuptools import setup


DOWNLOAD_URL = 'https://github.com/agamm/comeback/archive/v0.0.2-alpha.tar.gz'


setup(
    name='comeback',
    packages=['comeback'],
    version='0.0.1',
    author='agamm',
    description='Comeback right to your project\'s last state',
    url='https://github.com/agamm/comeback',
    keywords=['autorun', 'comeback', 'project restoration', 'auto open'],
    py_modules=['src'],
    license='MIT',
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': ['comeback=comeback.main:cli'],
    },
    download_url=DOWNLOAD_URL,
    classifiers=[
        'Development Status :: 3 - Alpha',
        # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Intended Audience :: Developers',
        # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
