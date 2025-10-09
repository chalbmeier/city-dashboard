from dash import dcc, html
from dash_iconify import DashIconify

def create_footer():
    div = html.Div(
        className="data-info-grid",
        children=[
            html.Button(
                className="data-info-btn", id="data-info-btn-1", n_clicks=0,
                children=[
                    DashIconify(
                        icon='mdi:information-variant-circle-outline',
                        width=32,
                        className="data-info-icon"
                    ),
                ],
            ),
            html.Div(
                #className="data-info-text",
                children=[
                    html.Span("Data source: ", className="data-info-title"),
                    html.Span("European Commission / DG Regional and Urban Policy, Survey on the Quality of Life in European Cities, 2023."),
                    html.Br(),
                    html.Span("Leafleft | © OpenStreetMap contributors.")
                ],
            ),
            info_box(),
        ],
    )
    return div

def info_box(body=None):

    if body is None:
        body = dcc.Markdown(
"""
The source of data is the **Survey on the Quality of Life in European Cities** conducted by the European Commission / DG Regional and Urban Policy in 2023.

The survey’s target population was all residents of the cities of interest aged 15 or over. The survey used a stratified random sampling design. The statistics shown here are based on approximately 850 completed interviews per city, reweighted to match population totals.

In line with the official reports, for each indicator I excluded the “don’t know/not answered” response category and reweighted the remaining categories, so the reported percentage shares are relative to those respondents who provided a valid answer.

The data and official reports are available at https://ec.europa.eu/regional_policy/information-sources/maps/quality-of-life_en.

This website’s code is available at https://github.com/chalbmeier/city-dashboard. It is not an official EU website, and I’m not associated with an EU institution.
""", link_target="_blank",
        )

    div = html.Div(
        className="info-box-overlay",
        id="info-box-overlay-1",
        children=html.Div(
            className="info-box-modal",
            children=[
                html.Div(
                    className="info-box-header",
                    children=[
                        html.Div("Information"),
                        html.Button(
                            "x", 
                            className="info-box-close-btn", 
                            id="info-box-close-btn-1",
                            title="Close",
                            n_clicks=0,
                        ),
                    ],
                ),
                html.Div(className="info-box-body", children=body),
            ],
        )
    )
    return div