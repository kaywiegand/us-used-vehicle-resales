

import pandas as pd
from collections import namedtuple


CityBounds = namedtuple('CityBounds', ['name', 'lat_min', 'lat_max', 'lon_min', 'lon_max'])
QUITO = CityBounds("Quito", -0.4, 0.05, -78.6, -78.3)


def is_coord_in_bounds(lat, lon, bounds):
    """
    Prüft, ob eine Koordinate innerhalb definierter Grenzen liegt.
    
    Args:
        lat (float): Der Breitengrad des Punktes.
        lon (float): Der Längengrad des Punktes.
        bounds (dict): Ein Dictionary mit 'lat_min', 'lat_max', 'lon_min', 'lon_max'.
        
    Returns:
        bool: True, wenn der Punkt innerhalb der Box liegt, sonst False.
    """
    lat_ok = bounds.lat_min <= lat <= bounds.lat_max
    lon_ok = bounds.lon_min <= lon <= bounds.lon_max
    
    return lat_ok and lon_ok






