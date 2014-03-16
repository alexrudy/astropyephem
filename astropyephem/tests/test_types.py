# -*- coding: utf-8 -*-

def test_ephem_date():
    from ..types import ea_date
    import astropy.time
    import ephem
    astropy_Time = ea_date(ephem.date("2000/01/01"))
    assert astropy_Time == astropy.time.Time("2000-01-01", scale='utc')
    assert isinstance(astropy_Time, astropy.time.Time)

def test_ephem_date_failing():
    from ..types import ea_date
    import astropy.time
    import ephem
    astropy_Time = ea_date(ephem.date("2000/01/01"))
    assert astropy_Time != astropy.time.Time("2000-01-01", scale='tai')
    assert isinstance(astropy_Time, astropy.time.Time)

def test_ephem_date_roundtrip():
    """docstring for test_ephem_date_roundtrip"""
    from ..types import ea_date, ae_date
    import astropy.time
    import ephem
    
    astropy_original = astropy.time.Time("2000-01-01", scale='utc')
    astropy_roundtrip = ea_date(ae_date(astropy_original))
    assert astropy_original == astropy_roundtrip
    
    ephem_original = ephem.date("2000/01/01")
    ephem_roundtrip = ae_date(ea_date(ephem_original))
    assert ephem_original == ephem_roundtrip
    