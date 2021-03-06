# -*- coding: utf-8 -*-

""" systemcheck - A Python-based extensive configuration validation solution

systemcheck is a simple application that has two primary functions: 

* Compare the configuration of a specific system parameters against a list of desired values
* Document the configuration of a specific system. 



"""

# define authorship information
__authors__ = ['Lars Fasel']
__author__ = ','.join(__authors__)
__credits__ = []
__copyright__ = 'Copyright (c) 2017'
__license__ = 'GNU AGPLv3'

# maintanence information
__maintainer__ = 'Lars Fasel'
__email__ = 'systemcheck@team-fasel.com'

# define version information
__requires__ = ['PyQt5']
__version_info__ = (0, 1, 0)
__version__ = 'v{}.{}.{}'.format(*__version_info__)
__revision__ = __version__

#from systemcheck import plugins
#from systemcheck import config
#from systemcheck import models
#from systemcheck import session
#from systemcheck import systems
#from systemcheck import checks
#from systemcheck import gui

import systemcheck.checks
import systemcheck.plugins
import systemcheck.config
import systemcheck.models
import systemcheck.session
import systemcheck.systems
import systemcheck.gui
