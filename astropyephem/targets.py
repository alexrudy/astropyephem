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

import sys

import ephem

import astropy.units as u
from astropy.coordinates import ICRS, FK5
from astropy.time import Time
from astropy.utils.misc import find_mod_objs

from .bases import EphemClass, EphemAttribute, EphemPositionClass

__all__ = ['FixedBody', 'EllipticalBody', 'HyperbolicBody', 'ParabolicBody', 'SolarSystemBody', 'PlanetaryMoon',
    'ArtificialSatellite']

class FixedBody(EphemPositionClass):
    """A FixedBody is an object with a fixed RA and DEC"""
    
    __wrapped_class__ = ephem.FixedBody
    
    def __init__(self, position = None, name = None):
        super(FixedBody, self).__init__()
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
        
class EllipticalBody(EphemPositionClass):
    """EllipticalBody"""
    __wrapped_class__ = ephem.EllipticalBody
    
    _a = EphemAttribute('_a', u.AU)
    _size = EphemAttribute('_size', u.arcsec)
    
class HyperbolicBody(EphemPositionClass):
    """HyperbolicBody"""
    __wrapped_class__ = ephem.HyperbolicBody
    
    _q = EphemAttribute('_q', u.AU)
    _size = EphemAttribute('_size', u.arcsec)
    
class ParabolicBody(EphemPositionClass):
    """HyperbolicBody"""
    __wrapped_class__ = ephem.ParabolicBody
    
    _q = EphemAttribute('_q', u.AU)
    _size = EphemAttribute('_size', u.arcsec)

class SolarSystemBody(EphemPositionClass):
    """SolarSystemBody"""
    
    
    # Heliocentric coordinates are not implemented
    # by astropy, and so are not supported here for now.
    @property
    def heliocentric_position(self):
        """Return the heliocentric computed position."""
        raise NotImplementedError
    
    sun_distance = EphemAttribute("sun_distance", u.AU)
    earth_distance = EphemAttribute("earth_distance", u.AU)

class PlanetaryMoon(SolarSystemBody):
    """Class for a Planetary moon."""
    
    # x,y,z positions are in units of planet radii, which we don't
    # know, so we don't convert those to quantities here.
    pass

class ArtificialSatellite(SolarSystemBody):
    """Artificial Earth Satellite."""
    
    elevation = EphemAttribute("elevation", u.m)
    range = EphemAttribute("range", u.m)
    range_velocity = EphemAttribute("range_velocity", u.m/u.s)
    

# Setup the planet classes. 
# We handle the specific planets that are provided by ephem below.
module = sys.modules[__name__]
for class_name, full_class_name, ephem_class in zip(*find_mod_objs('ephem')):
    if isinstance(ephem_class, (ephem.Planet)):
        setattr(module, class_name, type(class_name, (SolarSystemBody,), dict(__wrapped_class__ = ephem_class)))
        __all__ += [ class_name ]
    elif isinstance(ephem_class, (ephem.PlanetMoon)):
        setattr(module, class_name, type(class_name, (PlanetaryMoon,), dict(__wrapped_class__ = ephem_class)))
        __all__ += [ class_name ]

class Sun(SolarSystemBody):
    """Our star."""
    __wrapped_class__ = ephem.Sun
    
class Moon(SolarSystemBody):
    """Earth's Moon"""
    __wrapped_class__ = ephem.Moon
    
    
class Jupiter(SolarSystemBody):
    """Jupiter"""
    __wrapped_class__ = ephem.Jupiter
    
class Saturn(SolarSystemBody):
    """Jupiter"""
    __wrapped_class__ = ephem.Saturn
        
