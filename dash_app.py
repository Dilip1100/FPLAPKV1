import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import logging
import os
import base64
import io

# Set up logging
log_dir = "/tmp/automotive_dashboard"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "dashboard.log")
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Initialize Faker
fake = Faker()

# Initialize Dash app with CYBORG theme
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.CYBORG,
        "https://use.fontawesome.com/releases/v5.15.4/css/all.css"
    ]
)
app.title = "Automotive Analytics Dashboard"
server = app.server  # For Gunicorn

# Data generation functions
def generate_sales_data():
    try:
        car_makes = ['Toyota', 'Honda', 'Ford', 'Chevrolet', 'BMW', 'Mercedes', 'Hyundai', 'Volkswagen']
        car_models = {
            'Toyota': ['Camry', 'Corolla', 'RAV4'],
            'Honda': ['Civic', 'Accord', 'CR-V'],
            'Ford': ['F-150', 'Mustang', 'Explorer'],
            'Chevrolet': ['Silverado', 'Malibu', 'Equinox'],
            'BMW': ['3 Series', '5 Series', 'X5'],
            'Mercedes': ['C-Class', 'E-Class', 'GLC'],
            'Hyundai': ['Elantra', 'Sonata', 'Tucson'],
            'Volkswagen': ['Jetta', 'Passat', 'Tiguan']
        }
        salespeople = [fake.name() for _ in range(10)]
        dates = pd.date_range(start="2023-01-01", end="2025-07-07", freq="D")
        data = {
            'Salesperson': [random.choice(salespeople) for _ in range(1000)],
            'Car Make': [random.choice(car_makes) for _ in range(1000)],
            'Car Year': [random.randint(2018, 2025) for _ in range(1000)],
            'Date': [random.choice(dates) for _ in range(1000)],
            'Sale Price': [round(random.uniform(15000, 100000), 2) for _ in range(1000)],
            'Commission Earned': [round(random.uniform(500, 5000), 2) for _ in range(1000)]
        }
        df = pd.DataFrame(data)
        df['Car Model'] = df['Car Make'].apply(lambda x: random.choice(car_models[x]))
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Year'] = df['Date'].dt.year
        df['Quarter'] = df['Date'].dt.to_period('Q').astype(str)
        df['Month'] = df['Date'].dt.to_period('M').astype(str)
        logging.info("Sales data generated successfully")
        return df
    except Exception as e:
        logging.error(f"Error generating sales data: {str(e)}")
        return pd.DataFrame()

def generate_fake_data(df):
    try:
        hr_data = pd.DataFrame({
            "Employee ID": [f"E{1000+i}" for i in range(10)],
            "Name": [fake.name() for _ in range(10)],
            "Role": ["Sales Exec", "Manager", "Technician", "Clerk", "Sales Exec", "Technician", "HR", "Manager", "Clerk", "Sales Exec"],
            "Department": ["Sales", "Sales", "Service", "Admin", "Sales", "Service", "HR", "Sales", "Admin", "Sales"],
            "Join Date": pd.date_range(start="2018-01-01", periods=10, freq="180D"),
            "Salary (USD)": [50000 + i*1500 for i in range(10)],
            "Performance Score": [round(x, 1) for x in np.random.uniform(2.5, 5.0, 10)]
        })
        time_log_data = pd.DataFrame({
            "Employee ID": np.random.choice(hr_data["Employee ID"], size=30, replace=True),
            "Date": pd.date_range(end=pd.to_datetime("2025-07-07"), periods=30).tolist(),
            "Clock In": [f"{np.random.randint(8, 10)}:{str(np.random.randint(0, 60)).zfill(2)} AM" for _ in range(30)],
            "Clock Out": [f"{np.random.randint(4, 6)+12}:{str(np.random.randint(0, 60)).zfill(2)} PM" for _ in range(30)],
            "Total Hours": [round(np.random.uniform(6.5, 9.5), 1) for _ in range(30)]
        }).sort_values(by="Date", ascending=False)
        inventory_data = pd.DataFrame({
            "Part ID": [f"P{i:04d}" for i in range(1, 21)],
            "Part Name": [fake.word().capitalize() + " " + random.choice(["Filter", "Brake", "Tire", "Battery", "Sensor", "Pump"]) for _ in range(20)],
            "Car Make": [random.choice(df['Car Make'].dropna().unique()) for _ in range(20)],
            "Stock Level": [random.randint(0, 150) for _ in range(20)],
            "Reorder Level": [random.randint(10, 60) for _ in range(20)],
            "Unit Cost": [round(random.uniform(20, 600), 2) for _ in range(20)]
        })
        end_date = datetime.strptime("2025-07-07", "%Y-%-m-%d")
        crm_data = pd.DataFrame({
            "Customer ID": [f"C{100+i}" for i in range(20)],
            "Customer Name": [fake.name() for _ in range(20)],
            "Contact Date": [fake.date_between(start_date="-1y", end_date=end_date) for _ in range(20)],
            "Interaction Type": [random.choice(["Inquiry", "Complaint", "Follow-up", "Feedback", "Service Request"]) for _ in range(20)],
            "Salesperson": [random.choice(df['Salesperson'].dropna().unique()) for _ in range(20)],
            "Satisfaction Score": [round(random.uniform(1.0, 5.0), 1) for _ in range(20)]
        })
        demo_data = pd.DataFrame({
            "Customer ID": [f"C{100+i}" for i in range(20)],
            "Age Group": [random.choice(["18-25", "26-35", "36-45", "46-55", "55+"]) for _ in range(20)],
            "Region": [fake.state() for _ in range(20)],
            "Purchase Amount": [round(random.uniform(15000, 100000), 2) for _ in range(20)],
            "Preferred Make": [random.choice(df['Car Make'].dropna().unique()) for _ in range(20)]
        })
        logging.info("Fake data generated successfully")
        return hr_data, inventory_data, crm_data, demo_data, time_log_data
    except Exception as e:
        logging.error(f"Error generating fake data: {str(e)}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# Generate data
df = generate_sales_data()
hr_data, inventory_data, crm_data, demo_data, time_log_data = generate_fake_data(df)

# Custom CSS
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
# Save CSS to assets folder
os.makedirs("assets", exist_ok=True)
with open("assets/custom.css", "w") as f:
    f.write(custom_css)

# Layout
app.layout = dbc.Container([
    html.Div([
        html.H1(
            [html.I(className="fas fa-car mr-2"), "Automotive Analytics Dashboard"],
            className="text-center text-white mb-3",
            style={"fontWeight": "600"}
        ),
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

    html.Div([
        dbc.Button(
            [html.I(className="fas fa-download mr-1"), "Download Data as CSV"],
            id="download-btn",
            color="secondary",
            className="mr-2 mb-3"
        ),
        dcc.Download(id="download-csv"),
    ], className="text-center"),

    dbc.Toast(
        id="notification-toast",
        header="Notification",
        is_open=False,
        dismissable=True,
        duration=4000,
        style={"position": "fixed", "top": 10, "right": 10, "width": 350}
    ),

    html.Footer(
        "© 2025 One Trust | Crafted for smarter auto-financial decisions",
        className="text-center text-muted mt-4",
        style={"fontSize": "0.9em"}
    ),

    dcc.Store(id='filtered-data'),
    dcc.Store(id='theme-state', data='dark')
], fluid=True)

# Callbacks
@app.callback(
    Output('car-models-dropdown', 'options'),
    Input('car-makes-dropdown', 'value')
)
def update_car_models(car_make):
    try:
        options = [{'label': 'All', 'value': 'All'}]
        if car_make != 'All':
            models = sorted(df[df['Car Make'] == car_make]['Car Model'].dropna().unique())
            options.extend([{'label': x, 'value': x} for x in models])
        logging.info(f"Car models updated for {car_make}")
        return options
    except Exception as e:
        logging.error(f"Error updating car models: {str(e)}")
        return [{'label': 'All', 'value': 'All'}]

@app.callback(
    [
        Output('filtered-data', 'data'),
        Output('total-sales', 'children'),
        Output('total-commission', 'children'),
        Output('avg-price', 'children'),
        Output('trans-count', 'children'),
        Output('notification-toast', 'is_open'),
        Output('notification-toast', 'children')
    ],
    [
        Input('apply-filters', 'n_clicks'),
        State('salespeople-dropdown', 'value'),
        State('car-makes-dropdown', 'value'),
        State('car-models-dropdown', 'value'),
        State('car-years-dropdown', 'value')
    ]
)
def apply_filters(n_clicks, salesperson, car_make, car_model, car_year):
    try:
        if n_clicks is None:
            return df.to_json(date_format='iso', orient='split'), "Total Sales: $0", "Total Commission: $0", "Avg Sale Price: $0", "Transactions: 0", False, ""
        filtered_df = df.copy()
        if salesperson != 'All':
            filtered_df = filtered_df[filtered_df['Salesperson'] == salesperson]
        if car_make != 'All':
            filtered_df = filtered_df[filtered_df['Car Make'] == car_make]
        if car_model != 'All':
            filtered_df = filtered_df[filtered_df['Car Model'] == car_model]
        if car_year != 'All':
            filtered_df = filtered_df[filtered_df['Car Year'].astype(str) == car_year]
        
        total_sales = f"Total Sales: ${filtered_df['Sale Price'].sum():,.0f}"
        total_comm = f"Total Commission: ${filtered_df['Commission Earned'].sum():,.0f}"
        avg_price = f"Avg Sale Price: ${filtered_df['Sale Price'].mean():,.0f}" if not filtered_df.empty else "Avg Sale Price: $0"
        trans_count = f"Transactions: {filtered_df.shape[0]:,}"
        
        logging.info("Filters applied successfully")
        return filtered_df.to_json(date_format='iso', orient='split'), total_sales, total_comm, avg_price, trans_count, True, "Filters applied successfully!"
    except Exception as e:
        logging.error(f"Error applying filters: {str(e)}")
        return df.to_json(date_format='iso', orient='split'), "Total Sales: $0", "Total Commission: $0", "Avg Sale Price: $0", "Transactions: 0", True, f"Error: {str(e)}"

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
        
        elif tab == 'tab-3d':
            if filtered_df.empty:
                return html.P("No data available for 3D Sales", className="text-white")
            scatter_data = filtered_df.sample(n=min(100, len(filtered_df)), random_state=1)
            fig = go.Figure(data=[
                go.Scatter3d(
                    x=scatter_data['Commission Earned'], 
                    y=scatter_data['Sale Price'], 
                    z=scatter_data['Car Year'],
                    mode='markers', 
                    marker=dict(size=5, color=scatter_data['Car Year'], colorscale='Viridis', showscale=True)
                )
            ])
            fig.update_layout(
                scene=dict(xaxis_title='Commission Earned ($)', yaxis_title='Sale Price ($)', zaxis_title='Car Year'),
                template='plotly_dark', 
                height=450
            )
            return dcc.Graph(figure=fig, config=plotly_config)
        
        # [Other tabs remain similar; apply plotly_config and consistent styling]
        logging.info(f"Tab content rendered for {tab}")
        return html.P("Select a tab to view content.", className="text-white")
    except Exception as e:
        logging.error(f"Error rendering tab content for {tab}: {str(e)}")
        return html.P(f"Error loading content: {str(e)}", className="text-danger")

@app.callback(
    Output('collapse-filters', 'is_open'),
    Input('collapse-button', 'n_clicks'),
    State('collapse-filters', 'is_open')
)
def toggle_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

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

@app.callback(
    Output("download-csv", "data"),
    Input("download-btn", "n_clicks"),
    State("filtered-data", "data"),
    prevent_initial_call=True,
)
def download_data(n_clicks, data):
    try:
        filtered_df = pd.read_json(data, orient='split')
        return dcc.send_data_frame(filtered_df.to_csv, "filtered_automotive_data.csv")
    except Exception as e:
        logging.error(f"Error downloading data: {str(e)}")
        return None

# Client-side callback for theme toggle
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

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
