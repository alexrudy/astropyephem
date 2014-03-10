# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst
# 
#  bases.py
#  astropyephem
#  
#  Created by Alexander Rudy on 2014-03-04.
# 

from __future__ import (absolute_import, unicode_literals, division,
                        print_function)


import abc
import functools
import six
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import ICRS, FK5, AltAz
from pyshell.util import descriptor__get__

from .types import convert_astropy_to_ephem_weak, convert_ephem_to_astropy_weak

EQUINOX_J2000 = Time('J2000', scale='utc')
CELCIUS_OFFSET = 273.15 * u.K


@six.add_metaclass(abc.ABCMeta)
class EphemClass(object):
    """Converts attributes"""
    
    __wrapped_class__ = None
    
    def __init__(self, *args, **kwargs):
        """Initialize this instance."""
        super(EphemClass, self).__init__(*args, **kwargs)
        self.__dict__['__wrapped_instance__'] = self.__wrapped_class__(*args, **kwargs)
    
    def __repr__(self):
        """Represent this object"""
        try:
            repr_str = "<{}".format(self.__class__.__name__)
            if hasattr(self,'name') and self.name is not None:
                repr_str += " '{}' ".format(self.name)
            return repr_str + ">"
        except:
            wrapped_repr = repr(getattr(self,'__wrapped_instance__',getattr(self,'__wrapped_class__','UNKNOWN')))[1:-1]
            return "<{} wraps {}>".format(self.__class__.__name__, wrapped_repr)
    
    @staticmethod
    def _decorate_attribute_convert(f):
        """Convert function results from """
        @functools.wraps(f)
        def wrap_convert(*args, **kwargs):
            e_args = [convert_astropy_to_ephem_weak(arg) for arg in args]
            e_kwargs = { key:convert_astropy_to_ephem_weak(kwargs[key]) for key in kwargs }
            return convert_ephem_to_astropy_weak(f(*e_args, **e_kwargs))
        return wrap_convert
        
    def __getattr__(self, attribute_name):
        """Manipulate attribute access to use :mod:`astropy` objects."""
        attribute = getattr(self.__wrapped_instance__, attribute_name)
        if six.callable(attribute) and isinstance(getattr(attribute,'__self__',None), self.__wrapped_class__):
            return self._decorate_attribute_convert(attribute)
        return convert_ephem_to_astropy_weak(attribute)
        
    def __setattr__(self, attribute_name, value):
        """Set attributes, with type conversion."""
        if attribute_name in dir(self):
            return super(EphemClass, self).__setattr__(attribute_name, value)
        elif (not attribute_name.startswith("__")) and hasattr(self.__wrapped_instance__, attribute_name):
            value = convert_astropy_to_ephem_weak(value)
            return setattr(self.__wrapped_instance__, attribute_name, value)
        else:
            return super(EphemClass, self).__setattr__(attribute_name, value)
        
    def __set_wrapped_attr__(self, attribute_name, value):
        """Set a wrapped attribute name and value."""
        if (not attribute_name.startswith("__")) and hasattr(self.__wrapped_instance__, attribute_name):
            value = convert_astropy_to_ephem_weak(value)
            return setattr(self.__wrapped_instance__, attribute_name, value)
        raise AttributeError("{}:{} doesn't have attribute '{}'".format(self.__class__.__name__, self.__wrapped_class__.__name__, attribute_name))
    
    @classmethod
    def __subclasshook__(cls, C):
        if cls.__wrapped_class__ is not None:
            if issubclass(C, cls.__wrapped_class__):
                return True
        return NotImplemented

class EphemAttribute(object):
    """A descriptor which wraps an ephem attribute, giving it astropy units.."""
    def __init__(self, name, unit):
        super(EphemAttribute, self).__init__()
        self.name = name
        self.unit = unit
        
    def __set__(self, obj, value):
        """Set named the attribute"""
        return obj.__set_wrapped_attr__(self.name, u.Quantity(value, self.unit).value)
        
    @descriptor__get__
    def __get__(self, obj, objtype):
        """Get the named attribute."""
        return u.Quantity(getattr(obj.__wrapped_instance__, self.name), self.unit)
        
        
class EphemCelciusAttribute(EphemAttribute):
    """A unit attribute in Celcius"""
    def __init__(self, name):
        super(EphemCelciusAttribute, self).__init__(name, unit=u.K)
        
    def __set__(self, obj, value):
        """Set with offset."""
        return super(EphemCelciusAttribute, self).__set__(obj, value - CELCIUS_OFFSET)
        
    @descriptor__get__
    def __get__(self, obj, objtype):
        """Get with offsets."""
        return super(EphemCelciusAttribute, self).__get__(obj, objtype) + CELCIUS_OFFSET
        

class EphemPositionClass(EphemClass):
    """A target object, subclassed from ephem, which uses astropy coordinates."""

    def __repr__(self):
        """Represent this object"""
        repr_str = "<{} ".format(self.__class__.__name__)
        if self.name is not None:
            repr_str += "'{}'".format(self.name)
        try:
            repr_str += " at (RA={ra},DEC={dec})".format(
                ra = self.position.ra.to_string(u.hour, sep=":", pad=True),
                dec = self.position.dec.to_string(u.degree, sep=":", alwayssign=True),
            )
        except:
            pass
        return repr_str + ">"

    @property
    def _equinox(self):
        """The equinox of this Body"""
        if hasattr(self.__wrapped_instance__, '_epoch'):
            return self._epoch
        else:
            return EQUINOX_J2000

    @property
    def altaz(self):
        """Return the Alt/Az coordinate for this position."""
        return AltAz(self.az, self.alt)

    @property
    def position(self):
        """Return the astrometric computed position."""
        return self.astrometric_position

    @property
    def astrometric_position(self):
        """Return the astrometric computed position."""
        return FK5(self.a_ra, self.a_dec, equinox=self._equinox).transform_to(ICRS)

    @property
    def geocentric_position(self):
        """Return the geocentric computed position."""
        return FK5(self.g_ra, self.g_dec, equinox=self._equinox).transform_to(ICRS)

    @property
    def apparent_position(self):
        """Return the apparent computed position."""
        return FK5(self.ra, self.dec, equinox=self._equinox).transform_to(ICRS)
    
    def to_starlist(self):
        """To a starlist format"""
        string = "{name:<20s} {ra:s} {dec:s} {epoch:.0f}".format(
                                name = self.name.strip(),
                                ra = self.position.ra.to_string(u.hour, sep=" ", pad=True),
                                dec = self.position.dec.to_string(u.degree, sep=" ", alwayssign=True),
                                epoch = self.position.equinox.jyear,
                            )
        return string