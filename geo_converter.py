#!/usr/bin/python
# geo_converter.py
# Saito 2016
"""This is a module for converting from the the geocoordinate, radius
convention to the bounding box convention. It allows use of the same
parameter file for the Twitter REST API and Streaming API.

Usage:
bounding_box = convert_geocoordinates(
               latitude_degrees, longitude_degrees, radius_miles)
where
bounding_box == [southwest corner, northeast corner] ==
                [lon1, lat1, lon2, lat2]

and can be used when calling the streaming API. Notice it's longitude
then latitude!

"""
from __future__ import division

import math
import sys
from geopy.geocoders import Nominatim


def deg_to_rads(degs):
    rads = (degs / 360) * 2 * math.pi
    return rads


def convert_geocoordinates(latitude_degrees, longitude_degrees, radius_miles):
    """latitude and longitude in degrees, radius in miles, are converted
    to a bounding box representation, where box = [lat1, lon1, lat2,
    lon2]
    This doesn't work near the poles!
    """
    if latitude_degrees > 85 or latitude_degrees < -85:
        print "latitude is >85 or < -85. This won't work near poles!"
        sys.exit(0)
    if longitude_degrees > 180 or longitude_degrees < -180:
        print "longitude is >180 or < -180"
        sys.exit(0)

    radius_km = radius_miles / 0.62137
    if radius_km > 100:
        print "bounding box may be inaccurate for large radii"
    # print radius_km
    circ_of_earth_km = 40075.1612
    lat_rads = deg_to_rads(latitude_degrees)
    circ_of_earth_km_at_lat = math.cos(abs(lat_rads)) * circ_of_earth_km
    # print circ_of_earth_km_at_lat
    lon_km_per_degree = circ_of_earth_km_at_lat / 360
    print "lon_km_per_degree = {} at {}".format(lon_km_per_degree,
                                                latitude_degrees)
    lon_delta = radius_km / lon_km_per_degree
    # print "longitudinal delta = {}".format(lon_delta)
    lon1 = longitude_degrees - lon_delta
    lon2 = longitude_degrees + lon_delta
    # print lon1
    # print lon2
    # check if within range:

    # equator to pole distance in km
    eq2pole = 10001.965729
    lat_km_per_degree = eq2pole / 90
    lat_delta = radius_km / lat_km_per_degree
    # print lat_delta
    lat1 = latitude_degrees - lat_delta
    lat2 = latitude_degrees + lat_delta

    # check all points and correct if possible
    lat1 = correct_latitude(lat1)
    lat2 = correct_latitude(lat2)
    lon1 = correct_longitude(lon1)
    lon2 = correct_longitude(lon2)
    bounding_box = [lon1, lat1, lon2, lat2]
    return bounding_box


def correct_longitude(lon):
    if lon > 180:
        return -180 + (lon - 180)
    elif lon < -180:
        return 180 - (abs(lon) - 180)
    else:
        return lon


def correct_latitude(lat):
    if lat > 90 or lat < -90:
        print "This doesn't work near the poles!!!!"
        sys.exit(0)
    return lat


def get_bounding_box_from(GeoSearchClass):
    latitude = GeoSearchClass._latitude
    longitude = GeoSearchClass._longitude
    radius = GeoSearchClass._radius
    bounding_box = convert_geocoordinates(latitude, longitude, radius)
    return bounding_box


def get_search_terms_from(GeoSearchClass):
    """parses search_term string of form "", "sf", "#sf+#tech" from the
    params file and returns as list for use with streaming class

    """
    search_string = GeoSearchClass._search_term
    if search_string == "" or search_string is None:
        search_terms = None
    else:
        search_terms = search_string.split("+")
    return search_terms


# want to get geocoordinates for a location and visa versa
# to do:
# test!


def get_geocoords_from_address(address):
    """address is a string, like '555 5th Ave. NYC, NY, 12021'. This is
    searched and an approximate geocoordinate is returned, if possible
    in form (latitude, longitude)

    """
    geolocator = Nominatim()  # from geopy.geocoders.Nominatim
    location = geolocator.geocode(address)
    lat = location.latitude
    lon = location.longitude
    coords = (lat, lon)

    # do some check to see if coords were returned
    if not coords:
        return None

    # maybe do some coordinate conversion
    print "found these coords = {}".format(coords)
    back_projected_address = geolocator.reverse("{}, {}".format(lat, lon))
    print "back_projected_address = {}".format(back_projected_address)
    return coords


if __name__ == '__main__':
    # run some tests
    bounding_box = convert_geocoordinates(0, -122.4093, 0)
    print "longitudinal precision should be 111.32"
    print "should be same first and second"
    print "bounding_box = {}".format(bounding_box)

    bounding_box = convert_geocoordinates(37.7821, -122.4093, 1)
    print "should be ~    [-122.426, 37.771, -122.398, 37.790 ]"
    print "bounding_box = {}".format(bounding_box)

    bounding_box = convert_geocoordinates(45, -179.99, 10)
    print "longitudinal precision should be 78.84"
    print "should be sensible around Meridian"
    print "bounding_box = {}".format(bounding_box)

    bounding_box = convert_geocoordinates(84.7821, -122, 10)
    print "longitudinal precision should be ~9"
    print "should be sensible around pole"
    print "bounding_box = {}".format(bounding_box)

    get_geocoords_from_address('28 Lexington St., San Francisco, CA, 94110')
