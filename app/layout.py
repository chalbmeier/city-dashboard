from dash import dcc, html
from .components.footer import create_footer
from .components.indicator_info_panel import create_indicator_info_panel
from .components.plot import create_icon_column
from .constants import INITIAL_CITY


layout = html.Div(
    children=[
        # State variables
        dcc.Location(id="url"), # helper to trigger clientside callbacks at start
        dcc.Store(id="menu-state", data=True), # initial menu state, data={True, False}
        dcc.Store(id="map-params", data=None), # update at start up
        # Map
        html.Div(
            children=[
                html.Div(
                    id="map-wrap",
                    className="map-wrap", 
                    children=[]
                ),
                dcc.Store(id="selected-city-store", data=INITIAL_CITY),
                dcc.Store(id="last_map_clicks", data=0) # click counter to handle city selection
            ],
        ),
        # Side bar
        html.Div(
            className="sidebar-wrap state0",
            id="sidebar-wrap",
            children=[
                html.Div(
                    className="sidebar",
                    id="sidebar",
                    children=[
                        html.Div(
                            className="title",
                            children=[
                                html.Span("Quality of Life in European Cities"),
                                html.Br(),
                                html.Span("Results from an EU Survey", className="title-subtitle")
                            ],
                        ),
                        html.Div(
                            className="plot-wrap",
                            children=[
                                #html.Div(className="cell-colored"),
                                html.Div(),
                                html.Div(
                                    className="city-title",
                                    children=[
                                        html.Span("City: ", className="city-title-start"),
                                        html.Span(id="city-name"),
                                    ],
                                ),
                            ]
                        ),
                        html.Div(
                            className="widget-container",
                            children=[
                                html.Div(
                                    className="plot-wrap plot-wrap-recenter",
                                    children=[
                                        create_icon_column(),
                                        dcc.Graph(
                                            id="bar-plot", 
                                            config={"responsive": True, "displayModeBar": False}
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        html.Div(
                            className="widget-container",
                            children=[
                                html.Div(create_indicator_info_panel(0), id="indicator-info-panel-1"),
                            ],
                        ),
                        html.Div(
                            className="data-info",
                            children=[
                                create_footer(),
                            ]
                        )
                    ],
                ),
                html.Button("", id="toggle-btn", className="toggle-btn state0"),
            ],
        ),
    ],
)