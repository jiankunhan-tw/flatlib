""" 
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)

    This module implements a class to represent an 
    astrology Chart. It provides methods to handle
    the chart, as well as three relevant properties:
    
    - objects: a list with the chart's objects
    - houses: a list with the chart's houses
    - angles: a list with the chart's angles

    Since houses 1 and 10 may not match the Asc and
    MC in some house systems, the Chart class 
    includes the list of angles. The angles should be
    used when you want to deal with angle's longitudes.
    
    There are also methods to access fixed stars.
"""

from . import angle
from . import const
from . import utils
from .ephem import ephem
from .datetime import Datetime

# ✅ 新增：定義 nextSign 函數（每30度切換星座）
def nextSign(start):
    return ((int(start) // 30 + 1) * 30) % 360

# ✅ 直接內嵌 House 類別，使用自定 nextSign()
class House:
    @staticmethod
    def contains(house, lon):
        start = house.lon
        end = nextSign(start)
        if start < end:
            return start <= lon < end
        else:
            return lon >= start or lon < end


# ------------------ #
#    Chart Class     #
# ------------------ #

class Chart:
    """ This class represents an astrology chart. """

    def __init__(self, date, pos, **kwargs):
        hsys = kwargs.get('hsys', const.HOUSES_DEFAULT)
        IDs = kwargs.get('IDs', const.LIST_OBJECTS_TRADITIONAL)

        self.date = date
        self.pos = pos
        self.hsys = hsys
        self.objects = ephem.getObjectList(IDs, date, pos)
        self.houses, self.angles = ephem.getHouses(date, pos, hsys)

    def copy(self):
        chart = Chart.__new__(Chart)
        chart.date = self.date
        chart.pos = self.pos
        chart.hsys = self.hsys
        chart.objects = self.objects.copy()
        chart.houses = self.houses.copy()
        chart.angles = self.angles.copy()
        return chart

    # === Properties === #

    def getObject(self, ID):
        return self.objects.get(ID)

    def getHouse(self, ID):
        return self.houses.get(ID)

    def getAngle(self, ID):
        return self.angles.get(ID)

    def get(self, ID):
        if ID.startswith('House'):
            return self.getHouse(ID)
        elif ID in const.LIST_ANGLES:
            return self.getAngle(ID)
        else:
            return self.getObject(ID)

    # === Fixed stars === #

    def getFixedStar(self, ID):
        return ephem.getFixedStar(ID, self.date)

    def getFixedStars(self):
        IDs = const.LIST_FIXED_STARS
        return ephem.getFixedStarList(IDs, self.date)

    # === Houses and angles === #

    def isHouse1Asc(self):
        house1 = self.getHouse(const.HOUSE1)
        asc = self.getAngle(const.ASC)
        dist = angle.closestdistance(house1.lon, asc.lon)
        return abs(dist) < 0.0003

    def isHouse10MC(self):
        house10 = self.getHouse(const.HOUSE10)
        mc = self.getAngle(const.MC)
        dist = angle.closestdistance(house10.lon, mc.lon)
        return abs(dist) < 0.0003

    # === Other properties === #

    def isDiurnal(self):
        sun = self.getObject(const.SUN)
        mc = self.getAngle(const.MC)
        lat = self.pos.lat
        sunRA, sunDecl = utils.eqCoords(sun.lon, sun.lat)
        mcRA, mcDecl = utils.eqCoords(mc.lon, 0)
        return utils.isAboveHorizon(sunRA, sunDecl, mcRA, lat)

    def getMoonPhase(self):
        sun = self.getObject(const.SUN)
        moon = self.getObject(const.MOON)
        dist = angle.distance(sun.lon, moon.lon)
        if dist < 90:
            return const.MOON_FIRST_QUARTER
        elif dist < 180:
            return const.MOON_SECOND_QUARTER
        elif dist < 270:
            return const.MOON_THIRD_QUARTER
        else:
            return const.MOON_LAST_QUARTER

    # === Solar returns === #

    def solarReturn(self, year):
        sun = self.getObject(const.SUN)
        date = Datetime('{0}/01/01'.format(year), '00:00', self.date.utcoffset)
        srDate = ephem.nextSolarReturn(date, sun.lon)
        return Chart(srDate, self.pos, hsys=self.hsys)

    # === New: House locator === #

    def houseOf(self, obj):
        if isinstance(obj, str):
            obj = self.get(obj)
        elif hasattr(obj, 'id'):
            obj = self.get(obj.id)
        else:
            raise ValueError("Unsupported object type for houseOf()")

        for house in self.houses:
            if House.contains(house, obj.lon):
                return int(house.id)

        return None
