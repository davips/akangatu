"""Setup for akangatu package."""
#  Copyright (c) 2020. Davi Pereira dos Santos
#  This file is part of the akangatu project.
#  Please respect the license - more about this in the section (*) below.
#
#  akangatu is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  akangatu is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with akangatu.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is a crime and is unethical regarding the effort and
#  time spent here.
#  Relevant employers or funding agencies will be notified accordingly.

import setuptools


NAME = "akangatu"


VERSION = "0.2107.2"


AUTHOR = 'Davi Pereira-Santos'


AUTHOR_EMAIL = 'dpsabc@gmail.com'


DESCRIPTION = 'Data Handling and Science'


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
#               'Operating System' :: 'POSIX' :: 'Linux',
               'Programming Language :: Python :: 3.8']


INSTALL_REQUIRES = [
    'numpy', "more_itertools", "garoupa==0.2101.12"
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

