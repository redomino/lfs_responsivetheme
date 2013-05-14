# python imports
import os
from setuptools import find_packages
from setuptools import setup

# lfs imports
from lfs_responsivetheme import __version__

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()

setup(name='lfs_responsivetheme',
      version=__version__,
      description='A responsive theme for LFS',
      long_description=README,
      classifiers=[
          'Environment :: Web Environment',
          'Framework :: Django',
          'License :: OSI Approved :: GPL License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
      ],
      keywords='django e-commerce online-shop responsive-theme',
      author="Andrea D'Este",
      author_email='andrea.deste@redomino.com',
      url='http://www.redomino.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
      ],
)
