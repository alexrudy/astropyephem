# Licensed under a 3-clause BSD style license - see LICENSE.rst

# This sub-module is destined for common non-package specific utility
# functions that will ultimately be merged into `astropy.utils`

from astropy.utils.compat import override__dir__

try:
    from astropy.utils.introspection import find_mod_objs
except ImportError:
    from astropy.utils.misc import find_mod_objs
    