from dash_extensions.javascript import Namespace
import dash_leaflet as dl
from app.constants import COLOR_1, COLOR_2, COLOR_3
from app.data import load_geojson_data

# Functions defined in assets/mapElements.js. Values can be passed from Python with hideout argument
namespace = Namespace("mapElements")
point_to_layer = namespace("pointToLayer")
style_handle = namespace("styleHandle")


def create_map():
    cities = dl.GeoJSON(
        data=load_geojson_data(),
        id="geojson",
        format="geojson",
        hideout=dict(
            selected_city="Praha",  # default city
            colors=dict(default=COLOR_1, selected=COLOR_2, border=COLOR_3),
            marker=dict(radius=9.9),
        ),
        options=dict(
            pointToLayer=point_to_layer
        ),  # convert png markers to vector markers
        style=style_handle,
    )
    map = dl.Map(
        id="map",
        center=[53, -9.5],
        zoom=4,
        zoomControl=False,
        style={"height": "100%", "width": "100%"},
        children=[
            dl.TileLayer(
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> contributors',
            ),
            cities,
            dl.ZoomControl(position="topright"),
        ],
    )
    return map