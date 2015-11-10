from __future__ import division
from geopy.distance import vincenty
import math

def distance_vincentry_calculate(l1,l2):
    return vincenty(l1,l2).m

def distance_baidu_caculate(l1,l2):
    p1=Point()
    p2=Point()

    p1.lat=l1[0]
    p1.lng=l1[1]
    p2.lat=l2[0]
    p2.lng=l2[1]

    dis=getDistance(p1, p2)
    return dis

class Point:
    def __self__(self,latitude,longitude):
        self.lat=latitude
        self.lng=longitude

def max(a,b):
    if a>b:
        return a
    return b
def min(a,c):
    if a>c:
        return c
    return a

def lw(a,b, c):
#     b != n && (a = Math.max(a, b));
#     c != n && (a = Math.min(a, c));
    a = max(a,b)
    a = min(a,c)
    return a

def ew(a, b, c):

    while a > c:
        a -= c - b
    while a < b:
        a += c - b
    return a


def oi(a):
    return math.pi * a / 180

def Td(a, b, c, d):
    return 6370996.81 * math.acos(math.sin(c) * math.sin(d) + math.cos(c) * math.cos(d) * math.cos(b - a))

def Wv(a, b):
    if not a or not b:
        return 0;
    a.lng = ew(a.lng, -180, 180)
    a.lat = lw(a.lat, -74, 74)
    b.lng = ew(b.lng, -180, 180)
    b.lat = lw(b.lat, -74, 74)
    return Td(oi(a.lng), oi(b.lng), oi(a.lat), oi(b.lat))

def getDistance(a, b):
    c = Wv(a, b)
    return c
#
# if __name__ == '__main__':
#     print distance_baidu_caculate([37.480563,121.467113],[37.480591,121.467926])