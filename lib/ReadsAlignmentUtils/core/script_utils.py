import logging
import os
import subprocess
import traceback


'''
A utility python module containing a set of methods necessary for this kbase 
module.
'''

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}

def log(message, level=logging.INFO, logger = None):
    if logger is None:
        if level == logging.DEBUG:
            print('\nDEBUG: '+message+'\n')
        elif level == logging.INFO:
            print('\nINFO: '+message+'\n')
        elif level == logging.WARNING:
            print('\nWARNING: '+message+'\n')
        elif level == logging.ERROR:
            print('\nERROR: ' + message+'\n')
        elif level == logging.CRITICAL:
            print('\nCRITICAL: ' + message+'\n')
    else:
        logger.log(level, '\n'+message+'\n')

def whereis(program):
    """
    returns path of program if it exists in your ``$PATH`` variable or `
    `None`` otherwise
    """
    for path in os.environ.get('PATH', '').split(':'):
    	if os.path.exists(os.path.join(path, program)) and not os.path.isdir(os.path.join(path, program)):
            return os.path.join(path, program)
    return None