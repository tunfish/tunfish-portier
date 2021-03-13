# -*- coding: utf-8 -*-
from setuptools import setup, find_namespace_packages

setup(name='tunfish-portier',
      version='0.1.0',
      description='Convenient VPN infrastructure on top of secure WireGuard tunnels',
      #long_description=README,
      license="AGPL 3, EUPL 1.2",
      classifiers=[
        "Programming Language :: Python 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Telecommunications Industry",
        "Topic :: Communications",
        "Topic :: Database",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Object Brokering",
        "Topic :: System :: Networking",
        "Topic :: Utilities",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS"
        ],
      author='The Tunfish Developers',
      author_email='hello@tunfish.org',
      url='https://github.com/tunfish/tunfish-system',
      keywords='',
      packages=find_namespace_packages(include=["tunfish.*"]),
      include_package_data=True,
      package_data={
      },
      zip_safe=False,
      test_suite='tunfish.test',
      install_requires=[
          'tunfish-common',
          'pyroute2',
          'sqlalchemy',
          'sqlalchemy_utils',
      ],

      dependency_links=[
      ],
      entry_points={
          'console_scripts': [
              'tf-portier           = tunfish.portier:start',
              'tfctl           = tunfish.tfctl:start',
          ],
      },
)
