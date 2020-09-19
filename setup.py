"""Setup for akangatu package."""
import setuptools

import akangatu

NAME = "akangatu"


VERSION = 0.1


AUTHOR = 'Davi Pereira-Santos'


AUTHOR_EMAIL = ''


DESCRIPTION = 'Science as data akangatuormation'


with open('README.md', 'r') as fh:
    LONG_DESCRIPTION = fh.read()


LICENSE = 'GPL3'


URL = 'https://github.com/davips/akangatu'


DOWNLOAD_URL = 'https://github.com/davips/akangatu/releases'


CLASSIFIERS = ['Intended Audience :: Science/Research',
               'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
               'Natural Language :: English',
               'Programming Language :: Python',
               'Topic :: Scientific/Engineering',
               'Operating System :: Linux',
               'Programming Language :: Python :: 3.8']


INSTALL_REQUIRES = [
    'numpy',
]


EXTRAS_REQUIRE = {
}

SETUP_REQUIRES = ['wheel']

setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    classifiers=CLASSIFIERS,
    description=DESCRIPTION,
    download_url=DOWNLOAD_URL,
    extras_require=EXTRAS_REQUIRE,
    install_requires=INSTALL_REQUIRES,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license=LICENSE,
    packages=setuptools.find_packages(),
    setup_requires=SETUP_REQUIRES,
    url=URL,
)

package_dir = {'': 'akangatu'}  # For IDEs like Intellij to recognize the package.

