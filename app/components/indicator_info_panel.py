from dash import html
from dash_iconify import DashIconify
from app.data import INDICATORS, load_data


def create_indicator_info_panel(index):
    """
    Create info panel for a specific indicator.
    index: index of currently selected indicator in INDICATORS.keys()
    """
    indicator = list(INDICATORS.keys())[index]

    div = html.Div(
        children=[
            indicator_buttons(0),
            create_ranked_city_list(indicator),
        ],
        className="indicator-info-panel",
    )
    return div


def indicator_buttons(indicator):
    buttons = []
    for i, (_, ind) in enumerate(INDICATORS.items()):
        buttons.append(
            html.Button(
                DashIconify(icon=ind["icon"], width=22, className="rank-button"),
                id={"type": "rank-button", "index": i},
                n_clicks=0,
                className="iip-btn-row",
            )
        )
    div = html.Div(
        className="iip-btn-col",
        children=buttons,
    )
    return div


def create_ranked_city_list(indicator, n_ranks=10):
    """
    Create list of cities ranked according to a specific indicator.
    indicator: currently selected indicator
    """
    # Get data
    ranked_cities = (
        load_data()
        .loc[lambda d: d["indicator"] == indicator, ["name", "value"]]
        .sort_values("value", ascending=False)
    )
    top_cities = ranked_cities.head(n_ranks).values

    # Table title
    label = INDICATORS[indicator]["label"]
    title = html.Div(
        className="iip-title",
        children=[
            html.Span("Indicator: ", className="iip-title-start"),
            html.Span(f"{label}"),
        ],
    )
    # Table head
    rows = [
        html.Div(
            children=[
                html.Div(className="rank-table-header rank-table-col-right"),
                html.Div("City", className="rank-table-header rank-table-col-left"),
                html.Div("Percent", className="rank-table-header rank-table-col-right"),
            ],
            className="rank-table-row-base",
        )
    ]
    # Table body
    for i, (city, value) in enumerate(top_cities):
        # Check if last row
        if i == n_ranks - 1:
            class_name = "rank-table-row-base rank-table-row rank-table-row-last"  # last table row
        else:
            class_name = "rank-table-row-base rank-table-row"

        # Check even or uneven row
        if i % 2 == 0:
            class_name += " rank-table-row-even"

        rows.append(
            html.Button(
                children=[
                    html.Div(f"{i+1}.", className="rank-table-col-right"),
                    html.Div(f"{city}", className="rank-table-col-left"),
                    html.Div(
                        f"{round(100*value, 1)}", className="rank-table-col-right"
                    ),
                ],
                id={"type": "city-btn", "index": city},
                className=class_name,
                n_clicks=0,
            )
        )
    # Info box
    info_text = INDICATORS[indicator]["info"]
    info_box = html.Div(
        className="iip-info-text",
        children=[
            html.Span("Info:", style={"font-weight": "600"}),
            html.Br(),
            html.Span(f"{info_text}"),
        ],
    )
    # Put everything together
    div = html.Div(
        className="rank-table-outer",
        children=[
            title,
            html.Div(
                className="rank-table",
                children=[
                    html.Div(children=rows),
                ],
            ),
            info_box,
        ],
    )
    return div
