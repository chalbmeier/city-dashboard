from dash import dcc, html
from .components.footer import create_footer
from .components.indicator_info_panel import create_indicator_info_panel
from .components.map import create_map
from .components.plot import create_icon_column


layout = html.Div(
    children=[
        # Map
        html.Div(
            children=[
                create_map(),
                dcc.Store(
                    id="last_map_clicks", data=0
                ),  # click counter to handle city selection
            ],
            className="map-fill",
        ),
        # Side bar
        html.Div(
            className="sidebar-wrap",
            id="sidebar-wrap",
            children=[
                html.Div(
                    className="sidebar open",
                    id="sidebar",
                    children=[
                        html.Div(
                            className="sidebar-scroll",
                            children=[
                                html.Div(
                                    className="title",
                                    children=[
                                        html.Span(
                                            "Quality of Life in European Cities"
                                        ),
                                        html.Br(),
                                        html.Span(
                                            "Results from an EU Survey",
                                            className="title-subtitle",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    create_indicator_info_panel(0), id="indicator-info-panel-1"
                                ),
                                html.Div(
                                    className="plot-wrap",
                                    children=[
                                        html.Div(className="cell-colored"),
                                        html.Div(
                                            className="city-title",
                                            children=[
                                                html.Span(
                                                    "City: ", className="city-title-start"
                                                ),
                                                html.Span(id="selected-city"),
                                            ],
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="plot-wrap plot-wrap-recenter",
                                    children=[
                                        create_icon_column(),
                                        dcc.Graph(
                                            id="bar-plot", config={"displayModeBar": False}
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="data-info",
                                    children=[
                                        create_footer(),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                html.Button("«", id="toggle-btn", className="toggle-btn"),
            ],
        ),
        dcc.Store(id="menu-open", data=True),  # initial menu state
    ],
)
