from dash import html
from dash_iconify import DashIconify
import plotly.graph_objects as go
from app.constants import COLORS, FONTS, SIDEBAR_WIDTH
from app.data import INDICATORS, load_data

GRAPH_HEIGHT = 240 # px
GRAPH_MARGIN_TOP = 5 # px
GRAPH_MARGIN_BOTTOM = 30 # px

def create_plot(city):
    df = load_data() 
    data = df[df['name']==city]

    bars = go.Bar(
        x=data['value'],
        y=data['indicator'],
        orientation='h',
        width=0.6,
        name=f'{city}',
        marker=dict(color=COLORS['bar']),
        opacity=1.0,    
        hovertemplate='%{x:.1%}<extra></extra>',
    )
    means = go.Scatter(
        x=data['mean'],
        y=data['indicator'],
        mode='markers',
        marker=dict(
            symbol='line-ns',
            line_color='black',
            line_width=1.7,
            size=7,
        ),
        name='Mean',
        hovertemplate='Mean: %{x:.1%}<extra></extra>',
    )

    fig = go.Figure(
        data=[bars, means],
        layout=dict(
            height=GRAPH_HEIGHT,
            autosize=True,
            barcornerradius=5,
            showlegend=False,
        ),
    )
    # 0% tick label
    fig.add_annotation(
        x=0.03,
        y=-0.075,
        xref='x',
        yref='paper',
        text='0%',
        font_family=FONTS,
        showarrow=False,
    )

    fig.update_layout(
        font_family=FONTS,
        margin=dict(l=0, r=0, t=GRAPH_MARGIN_TOP, b=GRAPH_MARGIN_BOTTOM),
        dragmode=False,
        bargap=0.1, 
        plot_bgcolor=COLORS['bg'],
        paper_bgcolor=COLORS['bg'],
        hoverlabel=dict(
            bgcolor=COLORS['bg'],
            bordercolor="black",
            font_size=12,
            font_color="#333",
            font_family=FONTS,
        ),
    ) 
    fig.update_xaxes(
        fixedrange=True,
        range=[0, 1],
        tickvals=[0.2, 0.4, 0.6, 0.8], # plotly hides 0 automatically due to space constraints
        tickformat='.0%',
        gridcolor='lightgrey',
        gridwidth=0.5,
        zeroline=True,
        zerolinecolor='lightgrey',
        zerolinewidth=1.5,
    )
    fig.update_yaxes(
        fixedrange=True,
        showticklabels=False,
    )
    return fig

def create_icon_column():
    div = html.Div(
        children=[
            html.Div([
                    DashIconify(icon=INDICATORS[ind]['icon'],
                        width=18, color="#3b3b3b", className='indicator-icon'
                    ),
                    html.Span(INDICATORS[ind]['label'], className="tooltip-text"),
                ],
                id={"type": "icon-button", "index": i},
                n_clicks=0,
                className='icon-row'
            ) for i, ind in enumerate(list(INDICATORS.keys()))
        ],
        className='icon-column',
        style={
            "paddingTop": f"{GRAPH_MARGIN_TOP}px",
            "paddingBottom": f"{GRAPH_MARGIN_TOP + 31}px", # +x for legend
        }
    )
    return div