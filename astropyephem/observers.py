# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst
# 
#  observers.py
#  astropyephem
#  
#  Created by Alexander Rudy on 2014-03-03.
# 

from __future__ import (absolute_import, unicode_literals, division,
                        print_function)

import ephem

import six

import astropy.units as u
from astropy.coordinates import ICRS, FK5, AltAz, Angle
from astropy.time import Time

from .bases import EphemClass, EphemAttribute, EphemCelciusAttribute

class Observer(EphemClass):
    """Make an observer."""
    
    __wrapped_class__ = ephem.Observer
    
    def __init__(self, **kwargs):
        super(Observer, self).__init__()
        for keyword, value in kwargs.items():
            setattr(self, keyword, value)
            
    def __repr__(self):
        """Represent an observer."""
        repr_str = "<{0}".format(self.__class__.__name__)
        if hasattr(self, 'name'):
            repr_str += " '{0}'".format(self.name)
        if hasattr(self, 'lat') and hasattr(self, 'lon'):
            repr_str += " at ({0},{1})".format(self.lat, self.lon)
        return repr_str + ">"
    
    
    elevation = EphemAttribute("elevation", u.m)
    
    temp = EphemCelciusAttribute("temp")
    
    pressure = EphemAttribute("pressure", 1e-3 * u.bar)
    
