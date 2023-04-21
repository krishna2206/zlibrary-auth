from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = 'A library that automate authentication process on Z-Library'
setup(
    name="zlibrary-auth",
    version=VERSION,
    author="Anhy Krishna Fitiavana",
    author_email="fitiavana.krishna@gmail.com",
    description=DESCRIPTION,
    long_description=open('README.md').read(),
    packages=find_packages(),
    install_requires=['click', 'playwright', 'Pillow'],
    entry_points={
        'console_scripts': [
            'zlib-auth=zlib_auth.zlib_auth:cli',
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)