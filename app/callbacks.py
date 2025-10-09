import dash
from dash import ALL, ctx, Input, no_update, Output, State
from .components.indicator_info_panel import create_indicator_info_panel
from .components.map import create_map
from .components.plot import create_plot
from .constants import INITIAL_CITY
from .data import N_INDICATORS

def set_callbacks(app):
    # Toggle sidebar
    @app.callback(
        Output("menu-state", "data"),
        Output("toggle-btn", "className"),
        Input("toggle-btn", "n_clicks"),
        State("menu-state", "data"),
        prevent_initial_call=True,
    )
    def toggle_sidebar(n_clicks, state_now):
        state_next = not state_now
        btn_class = f"toggle-btn {"state0" if state_next else "state1"}"
        return state_next, btn_class

    @app.callback(
        Output("sidebar-wrap", "className"),
        Output("sidebar", "className"),
        Input("menu-state", "data"),
        prevent_initial_call=True,
    )
    def apply_sidebar_style(is_state0):
        if is_state0:
            return ("sidebar-wrap state0", "sidebar state0")
        else:
            return ("sidebar-wrap state1", "sidebar state1")

    ### Map
    # Get screen size at start and set initial center of map
    app.clientside_callback(
        """
        function(href) {
            const width = window.innerWidth;
            const height = window.innerHeight;
            const center_lat = 52.5 - 900/height;
            const center_lng = width < 890 ? 6.5 : -20.8 + width/90;
            const center = [center_lat, center_lng];
            const zoom = 3.5 + width/1500;
            return {center: center, zoom: zoom};
        }
        """,
        Output("map-params", "data"),
        Input("url", "href"),
    )

    # Create map
    @app.callback(
        Output("map-wrap", "children"),
        Input("map-params", "data"),
    )
    def load_map(params):
        if not params:
            return no_update
        return create_map(center=params["center"], zoom=params["zoom"])

    # Update graph if new city was selected
    @app.callback(
        Output("bar-plot", "figure"),
        Output("city-name", "children"),
        Input("selected-city-store", "data"),
        prevent_initial_call=False,
    )
    def update_graph(data):
        return (create_plot(data), data) # Ex.: data = "Praha"

    # User selects city in map
    @app.callback(
        Output("geojson", "hideout"),
        Output("last_map_clicks", "data"),
        Input("geojson", "n_clicks"),
        Input({"type": "city-btn", "index": ALL}, "n_clicks_timestamp"),
        State("geojson", "clickData"),
        State("geojson", "hideout"),
        State("last_map_clicks", "data"),
        State({"type": "city-btn", "index": ALL}, "id"),
        prevent_initial_call=True,
    )
    def update_select_city(map_clicks, btn_timestamps, feature, hideout, last_map_clicks, btn_ids):
        if feature is None and btn_timestamps is None and map_clicks is None:
            return hideout

        # Check city in map was clicked
        if map_clicks is not None:
            map_clicked = map_clicks > last_map_clicks
            last_map_clicks = map_clicks
        else:
            map_clicked = False

        if map_clicked:
            name = feature["properties"]["name"]
            hideout["selected_city"] = name
            return (hideout, last_map_clicks)

        # Check if city in rank table was clicked using timestamps
        if not btn_timestamps:
            raise dash.exceptions.PreventUpdate
        times = [t or 0 for t in btn_timestamps] # convert None to 0
        max_ts = max(times)
        if max_ts == 0:
            # Only 0 timestamps -> no real clicks
            raise dash.exceptions.PreventUpdate

        idx = times.index(max_ts)
        city = btn_ids[idx]["index"]
        hideout["selected_city"] = city
        return (hideout, last_map_clicks)

    # Change internal selected-city-store if user selected new city
    @app.callback(
            Output("selected-city-store", "data"),
            Input("geojson", "hideout"),
            prevent_initial_call=True # hideout does not exist at start
    )
    def hideout_to_city_store(hideout):
        if hideout is None:
            no_update
        city = hideout.get("selected_city")
        return city

    # Selection of indicator
    @app.callback(
            Output("indicator-info-panel-1", "children"),
            Output({"type": "rank-button", "index": ALL}, "className"),
            Input({"type": "rank-button", "index": ALL}, "n_clicks"),
            prevent_initial_call=False,
    )
    def update_indicator(n_clicks):
        if ctx.triggered_id is None:   
            clicked_idx = 0
        else:
            clicked_idx = ctx.triggered_id["index"]
        # Classes of indicator buttons
        classes = ["iip-btn-row"] * N_INDICATORS
        classes[clicked_idx] = "iip-btn-row clicked"
        return (create_indicator_info_panel(clicked_idx), classes)

    ### Info box button in footer
    @app.callback(
        Output("info-box-overlay-1", "className"),
        Input("data-info-btn-1", "n_clicks"),
        Input("info-box-close-btn-1", "n_clicks"),
        State("info-box-overlay-1", "className"),
        prevent_initial_call=True,
    )
    def toggle_data_info_modal(open_click, close_click, cls):
        cls = cls or "info-box-overlay"
        trigger = ctx.triggered_id
        if trigger == "data-info-btn-1":
            return "info-box-overlay open"
        if trigger == "info-box-close-btn-1":
            return "info-box-overlay" 
        return cls
        


