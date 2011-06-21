from setuptools import setup, find_packages
import os

version = '.1'

setup(name='PluginIndexes.DateDateIndex',
      version=version,
      description="Date Index for ZCatalog that ignores time[zones]",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.rst")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Plone",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
        ],
      keywords='zcatalog, plone, catalog, index, date',
      author='eleddy',
      author_email='elizabeth.leddy@gmail.com',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['PluginIndexes'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
         'Products.ZCatalog', 
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
