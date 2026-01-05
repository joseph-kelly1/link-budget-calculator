import json

from skyfield.api import Loader

load_data = Loader('data')

def get_ts():
    """Load and return the Skyfield timescale object."""
    return load_data.timescale()

def fetch_active_satellites():
    """
    Fetches a list of active satellites from CelesTrak.
    Returns a dictionary of EarthSatellite objects.
    """
    url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle'
    sats = load_data.tle_file(url)

    return {sat.name: sat for sat in sats}

def get_tle_for_sat(sat_name, satellite_dict):
    """Retrieves a specific satellite object by name."""
    return satellite_dict.get(sat_name)

def fetch_sat_epoch(sat_name, satellite_dict):
    """Fetches the epoch time of a specific satellite."""
    sat = get_tle_for_sat(sat_name, satellite_dict)
    if sat:
        return sat.epoch
    else:
        raise ValueError(f"Satellite '{sat_name}' not found in the provided dictionary.")