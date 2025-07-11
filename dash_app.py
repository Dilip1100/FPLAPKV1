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
server = app.server

# Cache generated data
cached_data = None
def get_data():
    global cached_data
    if cached_data is None:
        df = generate_sales_data()
        hr_data, inventory_data, crm_data, demo_data, time_log_data = generate_fake_data(df)
        cached_data = (df, hr_data, inventory_data, crm_data, demo_data, time_log_data)
    return cached_data

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
        end_date = datetime.strptime("2025-07-07", "%Y-%m-%d")
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

# Load cached data
df, hr_data, inventory_data, crm_data, demo_data, time_log_data = get_data()

# Custom CSS
custom_css = """
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: linear-gradient(180deg, #1a252f 0%, #2c3e50 100%);
}
.card {
    border-radius: 10px;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
}
.sticky-header {
    position: fixed;
    top: 0;
    width: 100%;
    z-index: 1000;
    background: linear-gradient(90deg, #2c3e50, #3498db);
    padding: 15px 0;
    border-bottom: 3px solid #3498db;
}
.metric-card {
    background-color: #34495e;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    transition: background-color 0.3s;
}
.metric-card:hover {
    background-color: #3e5f8a;
}
.nav-tabs .nav-link {
    color: #bdc3c7;
    font-weight: 600;
    border-radius: 6px;
}
.nav-tabs .nav-link.active {
    color: #ffffff;
    background-color: #3498db;
    border-color: #3498db;
}
.sidebar {
    position: fixed;
    top: 80px;
    left: 0;
    height: calc(100vh - 80px);
    width: 250px;
    background-color: #2c3e50;
    padding: 20px;
    transition: transform 0.3s ease;
}
.sidebar-hidden {
    transform: translateX(-250px);
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.card-body, .tab-content {
    animation: fadeIn 0.5s ease-in;
}
.btn-primary, .btn-secondary {
    transition: background-color 0.3s, transform 0.2s;
}
.btn-primary:hover, .btn-secondary:hover {
    transform: scale(1.05);
}
.back-to-top {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 1000;
}
"""
# Save CSS to assets folder
os.makedirs("assets", exist_ok=True)
with open("assets/custom.css", "w") as f:
    f.write(custom_css)

# Layout
app.layout = dbc.Container([
    # Welcome Modal
    dbc.Modal([
        dbc.ModalHeader("Welcome to Automotive Analytics Dashboard"),
        dbc.ModalBody([
            html.P("Explore sales, HR, inventory, CRM, and demographic data with interactive filters and visualizations."),
            html.P("Use the filters to narrow down data, switch tabs to view different insights, and download results as CSV."),
            dcc.Checkbox(id="dont-show-again", label="Don't show again", className="mt-2")
        ]),
        dbc.ModalFooter(
            dbc.Button("Get Started", id="close-modal", className="ml-auto", color="primary")
        ),
    ], id="welcome-modal", is_open=True, centered=True),

    # Header
    html.Div([
        html.H1(
            [html.I(className="fas fa-car mr-2"), "Automotive Analytics Dashboard"],
            className="text-center text-white mb-3",
            style={"fontWeight": "700", "fontSize": "2.5em"}
        ),
        html.Div([
            dbc.Button(
                [html.I(className="fas fa-sun mr-1"), "Toggle Theme"],
                id="theme-toggle",
                color="light",
                size="sm",
                className="mr-2",
                n_clicks=0
            ),
            dbc.Button(
                [html.I(className="fas fa-bars mr-1"), "Toggle Sidebar"],
                id="sidebar-toggle",
                color="light",
                size="sm",
                className="mb-3",
                n_clicks=0
            )
        ], className="text-right"),
    ], className="sticky-header"),

    # Sidebar
    dbc.Col([
        dbc.Collapse(
            dbc.Card([
                dbc.CardBody([
                    html.H4("Navigation", className="card-title text-white"),
                    dbc.Nav([
                        dbc.NavLink("KPI Trend", href="#tab-kpi", id="nav-kpi", active="exact"),
                        dbc.NavLink("3D Sales", href="#tab-3d", id="nav-3d", active="exact"),
                        dbc.NavLink("Heatmap", href="#tab-heatmap", id="nav-heatmap", active="exact"),
                        dbc.NavLink("Top Performers", href="#tab-top", id="nav-top", active="exact"),
                        dbc.NavLink("Vehicle Sales", href="#tab-vehicle", id="nav-vehicle", active="exact"),
                        dbc.NavLink("Model Comparison", href="#tab-model", id="nav-model", active="exact"),
                        dbc.NavLink("Trends", href="#tab-trends", id="nav-trends", active="exact"),
                        dbc.NavLink("HR Overview", href="#tab-hr", id="nav-hr", active="exact"),
                        dbc.NavLink("Inventory", href="#tab-inventory", id="nav-inventory", active="exact"),
                        dbc.NavLink("CRM", href="#tab-crm", id="nav-crm", active="exact"),
                        dbc.NavLink("Demographics", href="#tab-demo", id="nav-demo", active="exact")
                    ], vertical=True, pills=True, className="mt-3")
                ])
            ], className="sidebar"),
            id="sidebar-collapse",
            is_open=False
        )
    ], width={"size": 2, "xs": 12}, className="d-none d-md-block"),

    # Main Content
    dbc.Col([
        # Filters
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
                ], style={"fontWeight": "600"})
            ),
            dbc.Collapse(
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label(
                                "Salesperson",
                                htmlFor="salespeople-dropdown",
                                className="text-white",
                                style={"fontWeight": "500"}
                            ),
                            dcc.Dropdown(
                                id='salespeople-dropdown',
                                options=[{'label': 'All', 'value': 'All'}] + [{'label': x, 'value': x} for x in sorted(df['Salesperson'].dropna().unique())],
                                value='All',
                                className="mb-2",
                                clearable=False,
                                aria_describedby="salesperson-tooltip"
                            ),
                            dbc.Tooltip(
                                "Filter by salesperson name",
                                target="salespeople-dropdown",
                                placement="top"
                            )
                        ], width={"size": 3, "xs": 12}),
                        dbc.Col([
                            html.Label(
                                "Car Make",
                                htmlFor="car-makes-dropdown",
                                className="text-white",
                                style={"fontWeight": "500"}
                            ),
                            dcc.Dropdown(
                                id='car-makes-dropdown',
                                options=[{'label': 'All', 'value': 'All'}] + [{'label': x, 'value': x} for x in sorted(df['Car Make'].dropna().unique())],
                                value='All',
                                className="mb-2",
                                clearable=False,
                                aria_describedby="car-make-tooltip"
                            ),
                            dbc.Tooltip(
                                "Filter by car manufacturer",
                                target="car-makes-dropdown",
                                placement="top"
                            )
                        ], width={"size": 3, "xs": 12}),
                        dbc.Col([
                            html.Label(
                                "Car Year",
                                htmlFor="car-years-dropdown",
                                className="text-white",
                                style={"fontWeight": "500"}
                            ),
                            dcc.Dropdown(
                                id='car-years-dropdown',
                                options=[{'label': 'All', 'value': 'All'}] + [{'label': str(x), 'value': str(x)} for x in sorted(df['Car Year'].dropna().astype(str).unique())],
                                value='All',
                                className="mb-2",
                                clearable=False,
                                aria_describedby="car-year-tooltip"
                            ),
                            dbc.Tooltip(
                                "Filter by car manufacturing year",
                                target="car-years-dropdown",
                                placement="top"
                            )
                        ], width={"size": 3, "xs": 12}),
                        dbc.Col([
                            html.Label(
                                "Car Model",
                                htmlFor="car-models-dropdown",
                                className="text-white",
                                style={"fontWeight": "500"}
                            ),
                            dcc.Dropdown(
                                id='car-models-dropdown',
                                options=[{'label': 'All', 'value': 'All'}],
                                value='All',
                                className="mb-2",
                                clearable=False,
                                aria_describedby="car-model-tooltip"
                            ),
                            dbc.Tooltip(
                                "Filter by car model (select Car Make first)",
                                target="car-models-dropdown",
                                placement="top"
                            )
                        ], width={"size": 3, "xs": 12}),
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            html.Label(
                                "Metric",
                                htmlFor="metric-dropdown",
                                className="text-white",
                                style={"fontWeight": "500"}
                            ),
                            dcc.Dropdown(
                                id='metric-dropdown',
                                options=[{'label': x, 'value': x} for x in ["Sale Price", "Commission Earned"]],
                                value="Sale Price",
                                className="mb-2",
                                clearable=False,
                                aria_describedby="metric-tooltip"
                            ),
                            dbc.Tooltip(
                                "Select metric to display in charts",
                                target="metric-dropdown",
                                placement="top"
                            )
                        ], width={"size": 3, "xs": 12}),
                        dbc.Col([
                            html.Label(
                                "Date Range",
                                htmlFor="date-range",
                                className="text-white",
                                style={"fontWeight": "500"}
                            ),
                            dcc.DatePickerRange(
                                id='date-range',
                                min_date_allowed=df['Date'].min(),
                                max_date_allowed=df['Date'].max(),
                                start_date=df['Date'].min(),
                                end_date=df['Date'].max(),
                                display_format='YYYY-MM-DD',
                                className="mb-2",
                                aria_describedby="date-range-tooltip"
                            ),
                            dbc.Tooltip(
                                "Filter sales by date range",
                                target="date-range",
                                placement="top"
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
                                color="secondary",
                                className="mr-2"
                            ),
                            dbc.Button(
                                [html.I(className="fas fa-times mr-1"), "Clear Filters"],
                                id="clear-filters",
                                color="danger",
                                className="mb-2"
                            )
                        ], width={"size": 3, "xs": 12}),
                    ])
                ]),
                id="collapse-filters",
                is_open=True
            )
        ], className="mb-4 card"),

        # Metrics
        dbc.Card([
            dbc.CardHeader(
                html.Div([
                    html.I(className="fas fa-chart-line mr-2"),
                    "Key Performance Indicators"
                ], style={"fontWeight": "600"})
            ),
            dbc.CardBody([
                dcc.Loading(
                    id="loading-metrics",
                    type="circle",
                    children=dbc.Row([
                        dbc.Col(
                            html.Div(
                                id='total-sales',
                                className="text-white metric-card",
                                role="status"
                            ),
                            width={"size": 3, "xs": 6},
                            className="mb-2"
                        ),
                        dbc.Col(
                            html.Div(
                                id='total-commission',
                                className="text-white metric-card",
                                role="status"
                            ),
                            width={"size": 3, "xs": 6},
                            className="mb-2"
                        ),
                        dbc.Col(
                            html.Div(
                                id='avg-price',
                                className="text-white metric-card",
                                role="status"
                            ),
                            width={"size": 3, "xs": 6},
                            className="mb-2"
                        ),
                        dbc.Col(
                            html.Div(
                                id='trans-count',
                                className="text-white metric-card",
                                role="status"
                            ),
                            width={"size": 3, "xs": 6},
                            className="mb-2"
                        )
                    ])
                )
            ])
        ], className="mb-4 card"),

        # Tabs
        dcc.Tabs(id="tabs", value='tab-kpi', children=[
            dcc.Tab(label='KPI Trend', value='tab-kpi', className="custom-tab", selected_className="custom-tab-active", children=[html.I(className="fas fa-chart-line mr-1")]),
            dcc.Tab(label='3D Sales', value='tab-3d', className="custom-tab", selected_className="custom-tab-active", children=[html.I(className="fas fa-cube mr-1")]),
            dcc.Tab(label='Heatmap', value='tab-heatmap', className="custom-tab", selected_className="custom-tab-active", children=[html.I(className="fas fa-th mr-1")]),
            dcc.Tab(label='Top Performers', value='tab-top', className="custom-tab", selected_className="custom-tab-active", children=[html.I(className="fas fa-trophy mr-1")]),
            dcc.Tab(label='Vehicle Sales', value='tab-vehicle', className="custom-tab", selected_className="custom-tab-active", children=[html.I(className="fas fa-car mr-1")]),
            dcc.Tab(label='Model Comparison', value='tab-model', className="custom-tab", selected_className="custom-tab-active", children=[html.I(className="fas fa-table mr-1")]),
            dcc.Tab(label='Trends', value='tab-trends', className="custom-tab", selected_className="custom-tab-active", children=[html.I(className="fas fa-chart-area mr-1")]),
            dcc.Tab(label='HR Overview', value='tab-hr', className="custom-tab", selected_className="custom-tab-active", children=[html.I(className="fas fa-users mr-1")]),
            dcc.Tab(label='Inventory', value='tab-inventory', className="custom-tab", selected_className="custom-tab-active", children=[html.I(className="fas fa-warehouse mr-1")]),
            dcc.Tab(label='CRM', value='tab-crm', className="custom-tab", selected_className="custom-tab-active", children=[html.I(className="fas fa-headset mr-1")]),
            dcc.Tab(label='Demographics', value='tab-demo', className="custom-tab", selected_className="custom-tab-active", children=[html.I(className="fas fa-user-friends mr-1")])
        ], className="mb-3"),
        dcc.Loading(
            id="loading-tabs",
            type="circle",
            children=html.Div(id='tabs-content', role="tabpanel")
        ),

        # Download and Controls
        html.Div([
            dbc.Button(
                [html.I(className="fas fa-download mr-1"), "Download Data as CSV"],
                id="download-btn",
                color="secondary",
                className="mr-2 mb-3",
                n_clicks=0
            ),
            dcc.Download(id="download-csv"),
            dbc.Button(
                [html.I(className="fas fa-undo mr-1"), "Reset Chart"],
                id="reset-chart",
                color="secondary",
                className="mb-3 mr-2",
                n_clicks=0
            ),
            dbc.Button(
                [html.I(className="fas fa-arrow-up mr-1"), "Back to Top"],
                id="back-to-top",
                color="secondary",
                className="mb-3 back-to-top",
                n_clicks=0
            )
        ], className="text-center"),

        # Toast
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

        # Stores
        dcc.Store(id='filtered-data'),
        dcc.Store(id='theme-state', data='dark'),
        dcc.Store(id='chart-state', data={}),
        dcc.Store(id='modal-state', data={'show': True})
    ], width={"size": 10, "xs": 12}),
], fluid=True, className="d-flex")

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
        Input('clear-filters', 'n_clicks'),
        State('salespeople-dropdown', 'value'),
        State('car-makes-dropdown', 'value'),
        State('car-models-dropdown', 'value'),
        State('car-years-dropdown', 'value'),
        State('date-range', 'start_date'),
        State('date-range', 'end_date')
    ]
)
def apply_filters(apply_clicks, clear_clicks, salesperson, car_make, car_model, car_year, start_date, end_date):
    try:
        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
        
        if triggered_id == 'clear-filters':
            return (
                df.to_json(date_format='iso', orient='split'),
                "Total Sales: $0",
                "Total Commission: $0",
                "Avg Sale Price: $0",
                "Transactions: 0",
                True,
                "Filters cleared successfully!"
            )
        
        if apply_clicks is None and clear_clicks is None:
            return (
                df.to_json(date_format='iso', orient='split'),
                "Total Sales: $0",
                "Total Commission: $0",
                "Avg Sale Price: $0",
                "Transactions: 0",
                False,
                ""
            )
        
        filtered_df = df.copy()
        if salesperson != 'All':
            filtered_df = filtered_df[filtered_df['Salesperson'] == salesperson]
        if car_make != 'All':
            filtered_df = filtered_df[filtered_df['Car Make'] == car_make]
        if car_model != 'All':
            filtered_df = filtered_df[filtered_df['Car Model'] == car_model]
        if car_year != 'All':
            filtered_df = filtered_df[filtered_df['Car Year'].astype(str) == car_year]
        if start_date and end_date:
            filtered_df = filtered_df[
                (filtered_df['Date'] >= pd.to_datetime(start_date)) & 
                (filtered_df['Date'] <= pd.to_datetime(end_date))
            ]
        
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
        Input('metric-dropdown', 'value'),
        Input('reset-chart', 'n_clicks')
    ]
)
def render_tab_content(tab, filtered_data, metric, reset_n_clicks):
    try:
        filtered_df = pd.read_json(filtered_data, orient='split') if filtered_data else pd.DataFrame()
        plotly_config = {
            'displayModeBar': True,
            'modeBarButtonsToAdd': ['downloadImage', 'resetScale2d'],
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
                title=dict(
                    text='KPI Trend: Sales and Commission Over Time',
                    x=0.5,
                    xanchor='center',
                    font=dict(size=20)
                ),
                xaxis_title='Month',
                yaxis_title='Amount ($)',
                template='plotly_dark',
                xaxis=dict(tickangle=45, gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                height=450,
                hovermode='x unified',
                margin=dict(l=50, r=50, t=80, b=50)
            )
            return dcc.Graph(figure=fig, config=plotly_config, id='kpi-graph')

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
                title=dict(
                    text='3D Sales: Commission vs Sale Price vs Car Year',
                    x=0.5,
                    xanchor='center',
                    font=dict(size=20)
                ),
                scene=dict(
                    xaxis_title='Commission Earned ($)',
                    yaxis_title='Sale Price ($)',
                    zaxis_title='Car Year'
                ),
                template='plotly_dark',
                height=450
            )
            return dcc.Graph(figure=fig, config=plotly_config, id='3d-graph')

        elif tab == 'tab-inventory':
            if inventory_data.empty:
                return html.P("No data available for Inventory", className="text-white")
            return [
                html.Label(
                    "Search Inventory",
                    htmlFor="inventory-search",
                    className="text-white mb-2",
                    style={"fontWeight": "500"}
                ),
                dcc.Input(
                    id='inventory-search',
                    type='text',
                    placeholder='Search by Part Name or Car Make...',
                    className="mb-3",
                    style={'width': '100%'},
                    aria_describedby="inventory-search-tooltip"
                ),
                dbc.Tooltip(
                    "Search inventory by part name or car make",
                    target="inventory-search",
                    placement="top"
                ),
                dcc.Loading(
                    id="loading-inventory",
                    type="circle",
                    children=dash_table.DataTable(
                        id='inventory-table',
                        columns=[
                            {"name": "Part ID", "id": "Part ID"},
                            {"name": "Part Name", "id": "Part Name"},
                            {"name": "Car Make", "id": "Car Make"},
                            {"name": "Stock Level", "id": "Stock Level"},
                            {"name": "Reorder Level", "id": "Reorder Level"},
                            {"name": "Unit Cost", "id": "Unit Cost"}
                        ],
                        data=inventory_data.to_dict('records'),
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'left', 'padding': '5px'},
                        style_header={'backgroundColor': '#2c3e50', 'fontWeight': 'bold', 'color': 'white'},
                        style_data={'backgroundColor': '#34495e', 'color': 'white'},
                        page_size=10
                    )
                )
            ]

        elif tab == 'tab-crm':
            if crm_data.empty:
                return html.P("No data available for CRM", className="text-white")
            return [
                html.Label(
                    "Search CRM",
                    htmlFor="crm-search",
                    className="text-white mb-2",
                    style={"fontWeight": "500"}
                ),
                dcc.Input(
                    id='crm-search',
                    type='text',
                    placeholder='Search by Customer Name or Salesperson...',
                    className="mb-3",
                    style={'width': '100%'},
                    aria_describedby="crm-search-tooltip"
                ),
                dbc.Tooltip(
                    "Search CRM by customer name or salesperson",
                    target="crm-search",
                    placement="top"
                ),
                dcc.Loading(
                    id="loading-crm",
                    type="circle",
                    children=dash_table.DataTable(
                        id='crm-table',
                        columns=[
                            {"name": "Customer ID", "id": "Customer ID"},
                            {"name": "Customer Name", "id": "Customer Name"},
                            {"name": "Contact Date", "id": "Contact Date"},
                            {"name": "Interaction Type", "id": "Interaction Type"},
                            {"name": "Salesperson", "id": "Salesperson"},
                            {"name": "Satisfaction Score", "id": "Satisfaction Score"}
                        ],
                        data=crm_data.to_dict('records'),
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'left', 'padding': '5px'},
                        style_header={'backgroundColor': '#2c3e50', 'fontWeight': 'bold', 'color': 'white'},
                        style_data={'backgroundColor': '#34495e', 'color': 'white'},
                        page_size=10
                    )
                )
            ]

        # [Add other tabs as needed with similar styling and accessibility]
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
        Output('date-range', 'start_date'),
        Output('date-range', 'end_date'),
        Output('notification-toast', 'is_open'),
        Output('notification-toast', 'children')
    ],
    [
        Input('reset-filters', 'n_clicks'),
        Input('clear-filters', 'n_clicks')
    ],
    prevent_initial_call=True
)
def reset_filters(reset_clicks, clear_clicks):
    if reset_clicks or clear_clicks:
        return (
            'All', 'All', 'All', 'All', 'Sale Price',
            df['Date'].min(), df['Date'].max(),
            True, "Filters reset successfully!"
        )
    return dash.no_update

@app.callback(
    Output("download-csv", "data"),
    Input("download-btn", "n_clicks"),
    State("filtered-data", "data"),
    prevent_initial_call=True
)
def download_data(n_clicks, data):
    try:
        filtered_df = pd.read_json(data, orient='split')
        return dcc.send_data_frame(filtered_df.to_csv, "filtered_automotive_data.csv")
    except Exception as e:
        logging.error(f"Error downloading data: {str(e)}")
        return None

@app.callback(
    Output("welcome-modal", "is_open"),
    [
        Input("close-modal", "n_clicks"),
        Input("dont-show-again", "value")
    ],
    State("modal-state", "data")
)
def toggle_modal(n_clicks, dont_show, modal_state):
    if n_clicks:
        if dont_show:
            modal_state['show'] = False
            return False
        return False
    return modal_state.get('show', True)

@app.callback(
    Output("sidebar-collapse", "is_open"),
    Input("sidebar-toggle", "n_clicks"),
    State("sidebar-collapse", "is_open")
)
def toggle_sidebar(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

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

# Client-side callback for sidebar navigation
app.clientside_callback(
    """
    function(n_clicks, tab_value) {
        if (n_clicks && n_clicks.some(n => n)) {
            const clickedIndex = n_clicks.findIndex(n => n);
            const tabIds = ['kpi', '3d', 'heatmap', 'top', 'vehicle', 'model', 'trends', 'hr', 'inventory', 'crm', 'demo'];
            return 'tab-' + tabIds[clickedIndex];
        }
        return tab_value;
    }
    """,
    Output('tabs', 'value'),
    Input({'type': 'nav', 'index': dash.dependencies.ALL}, 'n_clicks'),
    State('tabs', 'value')
)

# Client-side callback for back to top
app.clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks) {
            window.scrollTo({top: 0, behavior: 'smooth'});
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output('back-to-top', 'n_clicks'),
    Input('back-to-top', 'n_clicks')
)

# Callback for inventory search
@app.callback(
    Output('inventory-table', 'data'),
    Input('inventory-search', 'value')
)
def update_inventory_table(search_term):
    try:
        if not search_term:
            return inventory_data.to_dict('records')
        search_term = search_term.lower()
        filtered = inventory_data[
            inventory_data['Part Name'].str.lower().str.contains(search_term) |
            inventory_data['Car Make'].str.lower().str.contains(search_term)
        ]
        return filtered.to_dict('records')
    except Exception as e:
        logging.error(f"Error filtering inventory table: {str(e)}")
        return inventory_data.to_dict('records')

# Callback for CRM search
@app.callback(
    Output('crm-table', 'data'),
    Input('crm-search', 'value')
)
def update_crm_table(search_term):
    try:
        if not search_term:
            return crm_data.to_dict('records')
        search_term = search_term.lower()
        filtered = crm_data[
            crm_data['Customer Name'].str.lower().str.contains(search_term) |
            crm_data['Salesperson'].str.lower().str.contains(search_term)
        ]
        return filtered.to_dict('records')
    except Exception as e:
        logging.error(f"Error filtering CRM table: {str(e)}")
        return crm_data.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8050)
