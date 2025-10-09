from dash import Dash
from dash_extensions.enrich import DashProxy
from .callbacks import set_callbacks
from .data import load_geojson_data, load_data

def create_app():
    app = DashProxy(suppress_callback_exceptions=True)
    from .layout import layout
    app.layout = layout

    set_callbacks(app)

    try:
        _ = load_data() # cached, read-only
        _ = load_geojson_data() # cached, read-only
    except Exception as e:
        app.logger.warning(f"Data loading failed: {e}")
    return app

app = create_app()
server = app.server

