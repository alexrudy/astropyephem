=============
Astropy Ephem
=============

This is a wrapper for the Ephem_ module, which uses Astropy_ objects. Although the Ephem_ module is quite powerful, its measurement objects are less well defined, and less well documented than Astropy_.

This is an early development version. It requires an existing installation of Ephem_.

.. _Ephem: http://rhodesmill.org/pyephem/
.. _Astropy: http://www.astropy.org/
.. _git: http://git-scm.com/
.. _github: http://github.com
.. _Cython: http://cython.org/

Simple Examples
---------------

This module should work almost identically to Ephem_/PyEphem, with some minor adjustments to your import statements. So if you import this module as ``import astropyephem as ephem``, you should be able to run the Ephem_ examples and tutorial!

::
    >>> import astropyephem as ephem
    >>> u = ephem.Uranus()
    >>> u.compute('1781/3/13')
    >>> print('%s %s %s' % (u.ra, u.dec, u.mag))
    1.46501rad 0.410996rad 5.6 mag
    >>> u.ra
    <Angle 1.4650062559255066 rad>
    >>> type(u.ra)
    astropy.coordinates.angles.Angle

Positions will be in ICRS coordinates (although you can transform to any coordinate frame you like using the full power of the ``astropy.coordinates`` package)::
    
    >>> from astropy.coordinates import *
    >>> u.position
    <ICRS Coordinate: ra=87.2737189688 deg, dec=23.6395924879 deg>
    >>> u.transform_to(Galactic)
    <Galactic Coordinate: l=184.935951366 deg, b=-2.0754155542 deg>
    
