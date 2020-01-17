'''
Created on 17-Jan-2020

@author: Srinivas Gunti
'''
from distutils.core import setup

#List of files to install. path relative to root
files = []

setup(name = 'Minesweeper',
      version = '1.0.0',
      description = '',
      author = 'Srinivas, Gunti',
      author_email = 'srnvsiit@gmail.com',
#       url = '',
      packages = ['main'],
      package_data = {'package': files},
      scripts = ['runner'],
      long_description = """   """
      )
