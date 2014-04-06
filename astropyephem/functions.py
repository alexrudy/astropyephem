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
from .bases import _decorate_attribute_convert
from .targets import FixedBody
from .observers import Observer

__all__ = ['star','city']

def star(name, *args, **kwargs):
    """Return a star, wrapping ephem star objects."""
    estar = ephem.star(name, *args, **kwargs)
    star = FixedBody()
    star.__wrapped_instance__ = estar
    return star
    
def city(name):
    """Return a city object."""
    ecity = ephem.city(name)
    city = Observer()
    city.__wrapped_instance__ = ecity
    return city


# Wrap the pyephem functions to use astropy attributes.
module = sys.modules[__name__]
for func_name, full_func_name, ephem_func in zip(*find_mod_objs('ephem')):
    if inspect.isfunction(ephem_func) and func_name not in globals():
        globals()[func_name] = _decorate_attribute_convert(ephem_func)
        __all__ += [ func_name ]