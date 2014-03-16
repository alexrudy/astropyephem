# 
#  descriptors.py
#  astropyephem
#  
#  Created by Alexander Rudy on 2014-03-15.
# 

from __future__ import (absolute_import, unicode_literals, division, print_function)

import functools

def descriptor__get__(f):
    """A simple wrapper for descriptors which handles the convention that 
    type(self).item should return the full descriptor class used by item."""
    
    @functools.wraps(f)
    def get(self, obj, objtype):
        if obj is None:
            return self
        else:
            return f(self, obj, objtype)
    
    return get