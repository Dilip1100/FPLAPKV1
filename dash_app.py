import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import logging
import os
import base64
import io

# Set up logging (unchanged)
log_dir = "/tmp/automotive_dashboard"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "dashboard.log")
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Initialize Dash app with CYBORG theme for a modern, sleek look
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.CYBORG,  # Modern, dark theme
        "https://use.fontawesome.com/releases/v5.15.4/css/all.css"  # Font Awesome for icons
    ]
)
app.title = "Automotive Analytics Dashboard"
server = app.server

# Data generation (unchanged)
# [Include your existing generate_sales_data() and generate_fake_data() functions here]

# Generate data (unchanged)
df = generate_sales_data()
hr_data, inventory_data, crm_data, demo_data, time_log_data = generate_fake_data(df)

# Custom CSS for additional styling
custom_css = """
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
.card {
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    transition: transform 0.2s;
}
.card:hover {
    transform: translateY(-2px);
}
.sticky-header {
    position: sticky;
    top: 0;
    z-index: 1000;
    background-color: #1a252f;
    padding: 10px 0;
}
.metric-card {
    background-color: #2c3e50;
    padding: 15px;
    border-radius: 6px;
    text-align: center;
}
"""

# Inject custom CSS
app.css.append_css({"external_url": "/assets/custom.css"})  # Assumes custom.css is saved in assets/

# Layout with enhanced UI
app.layout = dbc.Container([
    # Sticky Header
    html.Div([
        html.H1(
            [html.I(className="fas fa-car mr-2"), "Automotive Analytics Dashboard"],
            className="text-center text-white mb-3",
            style={"fontWeight": "600"}
        ),
        # Theme Toggle
        html.Div([
            dbc.Button(
                [html.I(className="fas fa-sun mr-1"), "Toggle Theme"],
                id="theme-toggle",
                color="secondary",
                size="sm",
                className="mb-3"
            )
        ], className="text-right"),
    ], className="sticky-header"),

    # Collapsible Filter Section
    dbc.Card([
        dbc.CardHeader(
            html.Div([
                html.I(className="fas fa-filter mr-2"),
                "Filter Options",
                dbc.Button(
                    "Toggle Filters",
                    id="collapse-button",
                    className="float-right",
                    color="link",
                    size="sm"
                )
            ])
        ),
        dbc.Collapse(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Label(
                            "Salesperson",
                            className="text-white",
                            **{"aria-label": "Select Salesperson"}
                        ),
                        dcc.Dropdown(
                            id='salespeople-dropdown',
                            options=[{'label': 'All', 'value': 'All'}] + [{'label': x, 'value': x} for x in sorted(df['Salesperson'].dropna().unique())],
                            value='All',
                            className="mb-2",
                            clearable=False,
                            **{"aria-label": "Salesperson dropdown"}
                        ),
                        dcc.Tooltip(
                            id="salesperson-tooltip",
                            content="Filter by salesperson name",
                            target="salespeople-dropdown"
                        )
                    ], width={"size": 3, "xs": 12}),
                    dbc.Col([
                        html.Label(
                            "Car Make",
                            className="text-white",
                            **{"aria-label": "Select Car Make"}
                        ),
                        dcc.Dropdown(
                            id='car-makes-dropdown',
                            options=[{'label': 'All', 'value': 'All'}] + [{'label': x, 'value': x} for x in sorted(df['Car Make'].dropna().unique())],
                            value='All',
                            className="mb-2",
                            clearable=False,
                            **{"aria-label": "Car Make dropdown"}
                        ),
                        dcc.Tooltip(
                            id="car-make-tooltip",
                            content="Filter by car manufacturer",
                            target="car-makes-dropdown"
                        )
                    ], width={"size": 3, "xs": 12}),
                    dbc.Col([
                        html.Label(
                            "Car Year",
                            className="text-white",
                            **{"aria-label": "Select Car Year"}
                        ),
                        dcc.Dropdown(
                            id='car-years-dropdown',
                            options=[{'label': 'All', 'value': 'All'}] + [{'label': str(x), 'value': str(x)} for x in sorted(df['Car Year'].dropna().astype(str).unique())],
                            value='All',
                            className="mb-2",
                            clearable=False,
                            **{"aria-label": "Car Year dropdown"}
                        ),
                        dcc.Tooltip(
                            id="car-year-tooltip",
                            content="Filter by car manufacturing year",
                            target="car-years-dropdown"
                        )
                    ], width={"size": 3, "xs": 12}),
                    dbc.Col([
                        html.Label(
                            "Car Model",
                            className="text-white",
                            **{"aria-label": "Select Car Model"}
                        ),
                        dcc.Dropdown(
                            id='car-models-dropdown',
                            options=[{'label': 'All', 'value': 'All'}],
                            value='All',
                            className="mb-2",
                            clearable=False,
                            **{"aria-label": "Car Model dropdown"}
                        ),
                        dcc.Tooltip(
                            id="car-model-tooltip",
                            content="Filter by car model (select Car Make first)",
                            target="car-models-dropdown"
                        )
                    ], width={"size": 3, "xs": 12}),
                ], className="mb-3"),
                dbc.Row([
                    dbc.Col([
                        html.Label(
                            "Metric",
                            className="text-white",
                            **{"aria-label": "Select Metric"}
                        ),
                        dcc.Dropdown(
                            id='metric-dropdown',
                            options=[{'label': x, 'value': x} for x in ["Sale Price", "Commission Earned"]],
                            value="Sale Price",
                            className="mb-2",
                            clearable=False,
                            **{"aria-label": "Metric dropdown"}
                        ),
                        dcc.Tooltip(
                            id="metric-tooltip",
                            content="Select metric to display in charts",
                            target="metric-dropdown"
                        )
                    ], width={"size": 3, "xs": 12}),
                    dbc.Col([
                        dbc.Button(
                            [html.I(className="fas fa-check mr-1"), "Apply Filters"],
                            id="apply-filters",
                            color="primary",
                            className="mr-2"
                        ),
                        dbc.Button(
                            [html.I(className="fas fa-undo mr-1"), "Reset Filters"],
                            id="reset-filters",
                            color="secondary"
                        )
                    ], width={"size": 3, "xs": 12}),
                ])
            ]),
            id="collapse-filters",
            is_open=True
        )
    ], className="mb-4 card"),

    # Metrics Section with Enhanced Styling
    dbc.Card([
        dbc.CardHeader(
            html.Div([
                html.I(className="fas fa-chart-line mr-2"),
                "Key Performance Indicators"
            ])
        ),
        dbc.CardBody([
            dcc.Loading(
                id="loading-metrics",
                type="circle",
                children=dbc.Row([
                    dbc.Col(
                        html.Div(
                            id='total-sales',
                            className="text-white metric-card"
                        ),
                        width={"size": 3, "xs": 6},
                        className="mb-2"
                    ),
                    dbc.Col(
                        html.Div(
                            id='total-commission',
                            className="text-white metric-card"
                        ),
                        width={"size": 3, "xs": 6},
                        className="mb-2"
                    ),
                    dbc.Col(
                        html.Div(
                            id='avg-price',
                            className="text-white metric-card"
                        ),
                        width={"size": 3, "xs": 6},
                        className="mb-2"
                    ),
                    dbc.Col(
                        html.Div(
                            id='trans-count',
                            className="text-white metric-card"
                        ),
                        width={"size": 3, "xs": 6},
                        className="mb-2"
                    )
                ])
            )
        ])
    ], className="mb-4 card"),

    # Tabs with Icons
    dcc.Tabs(id="tabs", value='tab-kpi', children=[
        dcc.Tab(label='KPI Trend', value='tab-kpi', children=[html.I(className="fas fa-chart-line mr-1")]),
        dcc.Tab(label='3D Sales', value='tab-3d', children=[html.I(className="fas fa-cube mr-1")]),
        dcc.Tab(label='Heatmap', value='tab-heatmap', children=[html.I(className="fas fa-th mr-1")]),
        dcc.Tab(label='Top Performers', value='tab-top', children=[html.I(className="fas fa-trophy mr-1")]),
        dcc.Tab(label='Vehicle Sales', value='tab-vehicle', children=[html.I(className="fas fa-car mr-1")]),
        dcc.Tab(label='Model Comparison', value='tab-model', children=[html.I(className="fas fa-table mr-1")]),
        dcc.Tab(label='Trends', value='tab-trends', children=[html.I(className="fas fa-chart-area mr-1")]),
        dcc.Tab(label='HR Overview', value='tab-hr', children=[html.I(className="fas fa-users mr-1")]),
        dcc.Tab(label='Inventory', value='tab-inventory', children=[html.I(className="fas fa-warehouse mr-1")]),
        dcc.Tab(label='CRM', value='tab-crm', children=[html.I(className="fas fa-headset mr-1")]),
        dcc.Tab(label='Demographics', value='tab-demo', children=[html.I(className="fas fa-user-friends mr-1")])
    ], className="mb-3"),
    dcc.Loading(
        id="loading-tabs",
        type="circle",
        children=html.Div(id='tabs-content')
    ),

    # Download and Export Section
    html.Div([
        dbc.Button(
            [html.I(className="fas fa-download mr-1"), "Download Data as CSV"],
            id="download-btn",
            color="secondary",
            className="mr-2 mb-3"
        ),
        dbc.Button(
            [html.I(className="fas fa-image mr-1"), "Export Charts as PNG"],
            id="export-charts",
            color="secondary",
            className="mb-3"
        ),
        dcc.Download(id="download-csv"),
    ], className="text-center"),

    # Toast for Notifications
    dbc.Toast(
        id="notification-toast",
        header="Notification",
        is_open=False,
        dismissable=True,
        duration=4000,
        style={"position": "fixed", "top": 10, "right": 10, "width": 350}
    ),

    # Footer
    html.Footer(
        "© 2025 One Trust | Crafted for smarter auto-financial decisions",
        className="text-center text-muted mt-4",
        style={"fontSize": "0.9em"}
    ),

    # Store filtered data and theme
    dcc.Store(id='filtered-data'),
    dcc.Store(id='theme-state', data='dark')
], fluid=True)

# Callback for Collapsible Filters
@app.callback(
    Output('collapse-filters', 'is_open'),
    Input('collapse-button', 'n_clicks'),
    State('collapse-filters', 'is_open')
)
def toggle_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# Callback for Reset Filters
@app.callback(
    [
        Output('salespeople-dropdown', 'value'),
        Output('car-makes-dropdown', 'value'),
        Output('car-models-dropdown', 'value'),
        Output('car-years-dropdown', 'value'),
        Output('metric-dropdown', 'value'),
        Output('notification-toast', 'is_open'),
        Output('notification-toast', 'children')
    ],
    Input('reset-filters', 'n_clicks'),
    prevent_initial_call=True
)
def reset_filters(n_clicks):
    if n_clicks:
        return 'All', 'All', 'All', 'All', 'Sale Price', True, "Filters reset successfully!"
    return dash.no_update

# Callback for Theme Toggle (client-side for performance)
app.clientside_callback(
    """
    function(n_clicks, current_theme) {
        if (n_clicks) {
            const newTheme = current_theme === 'dark' ? 'light' : 'dark';
            document.body.className = newTheme + '-theme';
            return newTheme;
        }
        return current_theme;
    }
    """,
    Output('theme-state', 'data'),
    Input('theme-toggle', 'n_clicks'),
    State('theme-state', 'data')
)

# Modified Tabs Content Callback for Chart Export and Enhanced Plotly Config
@app.callback(
    Output('tabs-content', 'children'),
    [
        Input('tabs', 'value'),
        Input('filtered-data', 'data'),
        Input('metric-dropdown', 'value')
    ]
)
def render_tab_content(tab, filtered_data, metric):
    try:
        filtered_df = pd.read_json(filtered_data, orient='split') if filtered_data else pd.DataFrame()
        
        # Plotly config for all charts
        plotly_config = {
            'displayModeBar': True,
            'modeBarButtonsToAdd': ['downloadImage'],
            'displaylogo': False
        }

        if tab == 'tab-kpi':
            if filtered_df.empty:
                return html.P("No data available for KPI Trend", className="text-white")
            kpi_trend = filtered_df.groupby('Month')[['Sale Price', 'Commission Earned']].sum().reset_index()
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=kpi_trend['Month'], 
                y=kpi_trend['Sale Price'], 
                name='Sale Price', 
                line=dict(color='#00b7eb'),
                hovertemplate='%{x}: $%{y:,.2f}'
            ))
            fig.add_trace(go.Scatter(
                x=kpi_trend['Month'], 
                y=kpi_trend['Commission Earned'], 
                name='Commission', 
                line=dict(color='#ff6f61'),
                hovertemplate='%{x}: $%{y:,.2f}'
            ))
            fig.update_layout(
                title='KPI Trend',
                xaxis_title='Month',
                yaxis_title='Amount ($)',
                template='plotly_dark',
                xaxis=dict(tickangle=45, gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                height=450,
                hovermode='x unified',
                margin=dict(l=50, r=50, t=80, b=50)
            )
            return dcc.Graph(figure=fig, config=plotly_config)
        
        # [Other tab content remains similar but with updated colors and config]
        # For brevity, only KPI tab is shown with updates. Apply similar styling (colors, hover, config) to other tabs.

        logging.info(f"Tab content rendered for {tab}")
        return html.P("Select a tab to view content.", className="text-white")
    except Exception as e:
        logging.error(f"Error rendering tab content for {tab}: {str(e)}")
        return html.P(f"Error loading content: {str(e)}", className="text-danger")

# Existing Callbacks (unchanged unless modified above)
# [Include your existing callbacks for car models, filters, download, etc.]

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)
