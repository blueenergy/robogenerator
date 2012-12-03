from distutils.core import setup
from os.path import join
import os
import glob
 
datadir = 'graph_algorithm'
datafiles = [(datadir, [f for f in glob.glob(os.path.join(datadir, '*'))])]
SCRIPTS = ['robogenerator','robograph']
SCRIPTS = [join('src', 'bin', s) for s in SCRIPTS]
if os.sep == '\\':
    SCRIPTS += [s+'.bat' for s in SCRIPTS]
setup(name='robogenerator',
      version='0.2',
      description='Case generator for Robot',
      author='shuyolin',
      author_email='shuyong.y.lin@nsn.com',
      url='',      
      package_dir={'': 'src'},
      packages=['robogenerator', 'robogenerator.test','robogenerator.data_algorithm','robogenerator.data_algorithm.metacomm','robogenerator.data_algorithm.metacomm.combinatorics','robogenerator.example',
                'robogenerator.example.Volume_create_delete_function','robogenerator.example.UnitStateChange','robogenerator.example.UnitRestart',
                'robogenerator.example.TrialService','robogenerator.example.SIPCallService',
				'robogenerator.graph','robogenerator.graph_algorithm','robogenerator.strategy'],
	  scripts = SCRIPTS,
      platforms    = 'any',
      package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.class','*.java','*.exe'],
    }
      )

