from distutils.core import setup
#from setuptools import setup
from os.path import join
import os
import glob

'''
don't install PIL automatically since it will cause problem during compiling
install_requires=[
'PIL'
],

It seems following statement doesn't take effect
datadir = 'graph_algorithm'
datafiles = [(datadir, [f for f in glob.glob(os.path.join(datadir, '*'))])]

'''


 

SCRIPTS = ['robogenerator','robograph','robomind']
SCRIPTS = [join('src', 'bin', s) for s in SCRIPTS]

SCRIPTS += [s+'.bat' for s in SCRIPTS]
setup(name='robogenerator',
      version='0.3.7',
      description='Case generator for Robot',
      author='shuyolin',
      author_email='shuyong.y.lin@nsn.com',
      url='https://github.com/blueenergy/robogenerator',      
      package_dir={'': 'src'},
      packages=['robogenerator', 'robogenerator.test','robogenerator.data_algorithm',
                'robogenerator.data_algorithm.metacomm','robogenerator.data_algorithm.metacomm.combinatorics',
                'robogenerator.example','robogenerator.example.FileBehavior',
                'robogenerator.example.Volume_create_delete_function',
                'robogenerator.example.SIPCallService',
                'robogenerator.example.xmind',
				'robogenerator.graph','robogenerator.graph_algorithm','robogenerator.graph_algorithm.16','robogenerator.graph_algorithm.17','robogenerator.strategy'],
	  scripts = SCRIPTS,
      package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.class','*.java','*.exe','*.xmind','*.html','*.jpg','*.png'],
      },
      platforms    = 'any',

      )

