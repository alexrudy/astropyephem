# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst
# 
#  exceptions.py
#  astropyephem
#  
#  Created by Alexander Rudy on 2014-03-23.
# 

from __future__ import (absolute_import, unicode_literals, division, print_function)

from astropy.utils.misc import find_mod_objs

import sys
import inspect
import ephem

__all__ = ['AstropyEphemException']

class AstropyEphemException(object):
    """An exception raised by astropyephem"""
    pass
        

# Setup the pyephem exceptions.
# This only serves to provide a common base-class for pyephem errors.
module = sys.modules[__name__]
for class_name, full_class_name, ephem_class in zip(*find_mod_objs('ephem')):
    if inspect.isclass(ephem_class) and class_name not in globals():
        if issubclass(ephem_class, Exception):
            globals()[class_name] = type(class_name, (ephem_class,AstropyEphemException,), dict())
            __all__ += [ class_name ]