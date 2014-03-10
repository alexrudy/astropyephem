# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst
# 
#  targets.py
#  astropyephem
#  
#  Created by Alexander Rudy on 2014-03-10.
# 


from __future__ import (absolute_import, unicode_literals, division,
                        print_function)


import ephem

import astropy.units as u
from astropy.coordinates import ICRS, FK5, AltAz
from astropy.time import Time

from .bases import EphemClass, EphemPositionClass

class Target(EphemPositionClass):
    """A Target is an object with a fixed RA and DEC"""
    
    __wrapped_class__ = ephem.FixedBody
    
    def __init__(self, position = None, name = None):
        super(Target, self).__init__()
        if position is not None:
            self.fixed_position = position
        if name is not None:
            self.name = name
    
    def __repr__(self):
        """Represent this object"""
        repr_str = "<{} ".format(self.__class__.__name__)
        if self.name is not None:
            repr_str += "'{}'".format(self.name)
        try:
            repr_str += " at (RA={ra},DEC={dec})".format(
                ra = self.fixed_position.ra.to_string(u.hour, sep=":", pad=True),
                dec = self.fixed_position.dec.to_string(u.degree, sep=":", alwayssign=True),
            )
        except:
            pass
        return repr_str + ">"
    
    @property
    def fixed_position(self):
        """The position using :class:`astropy.coordinates.ICRS` in astrometric coordinates."""
        return FK5(self._ra, self._dec, equinox=self._equinox).transform_to(ICRS)
        
    @fixed_position.setter
    def fixed_position(self, coord):
        """Set the position using :class:`astropy.coordinates.ICRS`."""
        coord_fk5 = coord.transform_to(FK5)
        self._ra = coord_fk5.ra
        self._dec = coord_fk5.dec
        self._epoch = coord_fk5.equinox
        
    

class Sun(EphemPositionClass):
    """Our star."""
    __wrapped_class__ = ephem.Sun
    
class Moon(EphemPositionClass):
    """Earth's Moon"""
    __wrapped_class__ = ephem.Moon
    
