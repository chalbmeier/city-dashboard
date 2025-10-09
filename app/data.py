from dash_leaflet.express import dicts_to_geojson
from functools import lru_cache
import pandas as pd

INDICATOR_INFO1 = 'Percentage of respondents who answered "very satisfied" or "rather satisfied".'
INDICATOR_INFO2 = 'Percentage of respondents who "strongly" or "somewhat agree" with statement.'

INDICATORS = {
    'satis_city': {'label': '"I\'m satisfied to live in my city"', 'icon': 'mdi:city', 'info': INDICATOR_INFO2},
    'satis_transport': {'label': 'Satisfaction with public transport', 'icon': 'mdi:bus', 'info': INDICATOR_INFO1},
    'satis_school': {'label': 'Satisfaction with schools and other educational facilities', 'icon': 'mdi:account-school', 'info': INDICATOR_INFO1},
    'satis_healthcare': {'label': 'Satisfaction with health care services, doctors, and hospitals', 'icon': 'mdi:ambulance', 'info': INDICATOR_INFO1},
    'satis_greenspaces': {'label': 'Satisfaction with green spaces', 'icon': 'mdi:pine-tree', 'info': INDICATOR_INFO1},
    'satis_sports': {'label': 'Satisfaction with sport facilities', 'icon': 'mdi:table-tennis', 'info': INDICATOR_INFO1},
    'satis_culture': {'label': 'Satisfaction with cultural facilities', 'icon': 'mdi:theatre', 'info': INDICATOR_INFO1},
    'satis_publicspaces': {'label': 'Satisfaction with public spaces', 'icon': 'mdi:bench-back', 'info': INDICATOR_INFO1},
    'satis_housing': {'label': '"It\'s easy to find good housing in my city at a reasonable price"', 'icon': 'mdi:house-find', 'info': INDICATOR_INFO2},
}

N_INDICATORS = len(INDICATORS.keys())

@lru_cache(maxsize=1)
def load_data():
    df = pd.read_csv('data/data.csv')
    return df

@lru_cache(maxsize=1)
def load_geojson_data():
    df = pd.read_csv('data/cities.csv')
    geojson = dicts_to_geojson([{**c, **dict(tooltip=c["name"])} for c in df.to_dict(orient='records')])
    return geojson