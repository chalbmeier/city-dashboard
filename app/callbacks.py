import dash
from dash import ALL, ctx, Input, Output, State
from .components.indicator_info_panel import create_indicator_info_panel
from .components.plot import create_plot
from .data import N_INDICATORS


def set_callbacks(app):
    # Toggle sidebar
    @app.callback(
        Output("menu-open", "data"),
        Output("toggle-btn", "children"),
        Input("toggle-btn", "n_clicks"),
        State("menu-open", "data"),
        prevent_initial_call=True,
    )
    def toggle_sidebar(n_clicks, open_now):
        open_next = not open_now
        label = "«" if open_next else "»"

        return open_next, label

    @app.callback(
        Output("sidebar-wrap", "className"),
        Output("sidebar", "className"),
        Input("menu-open", "data"),
    )
    def apply_sidebar_style(is_open):
        if is_open:
            return ("sidebar-wrap", "sidebar open")
        else:
            return ("sidebar-wrap closed", "sidebar closed")

    # Select city
    @app.callback(
        Output("selected-city", "children"),
        Input("geojson", "hideout"),
    )
    def display_selected_city(hideout):
        city = hideout.get("selected_city")
        return f"{city}" if city else "No city selected."

    @app.callback(Output("bar-plot", "figure"), Input("geojson", "hideout"))
    def update_graph(hideout):
        city = hideout.get("selected_city")
        return create_plot(city)

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
    def update_select_city(
        map_clicks, btn_timestamps, feature, hideout, last_map_clicks, btn_ids
    ):
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
        times = [t or 0 for t in btn_timestamps]  # convert None to 0
        max_ts = max(times)
        if max_ts == 0:
            # Only 0 timestamps -> no real clicks
            raise dash.exceptions.PreventUpdate

        idx = times.index(max_ts)
        city = btn_ids[idx]["index"]
        hideout["selected_city"] = city
        return (hideout, last_map_clicks)

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
