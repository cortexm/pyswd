"""A setup tools based setup module.
"""

import setuptools

exec(open('swd/__about__.py').read())

def get_long_description():
    """Return long description from README.md file"""
    import os
    import codecs
    current_dir = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(current_dir, 'README.md'), encoding='utf-8') as readme_file:
        long_description = readme_file.read()
    return long_description

setuptools.setup(
    name=PROGNAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=get_long_description(),
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license='MIT',
    keywords='SWD debugger STM32 STLINK CORTEX-M ARM',

    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Embedded Systems',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],

    packages=[
        'swd'
    ],

    install_requires=[
        'pyusb (>=1.0.2)'
    ],

    entry_points={
        'console_scripts': [
            'pyswd=swd._app:main',
        ],
    },
)
