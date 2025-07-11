"""
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)

    This module defines the class House to represent
    the astrological houses. It includes a static 
    method to determine if a longitude is inside 
    a house.
"""

from . import angle


class House:
    """This class provides static methods to
    deal with houses."""

    @staticmethod
    def contains(house, lon):
        """Returns true if the longitude is inside
        the house limits.
        """

        start = house.lon
        end = angle.nextSign(start)

        if start < end:
            return start <= lon < end
        else:
            return lon >= start or lon < end
