# Dash version of the PyQt5 Automotive Dashboard
# Core features: Layout, Filters, KPI, Tabs, Graphs, Tables, CSV Export

import dash
from dash import Dash, dcc, html, Input, Output, State, dash_table
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from faker import Faker
import random
import io
from datetime import datetime

app = Dash(__name__, suppress_callback_exceptions=True)
fake = Faker()

# ------------------ Data Generation ------------------
def generate_sales_data():
    car_makes = ['Toyota', 'Honda', 'Ford', 'Chevrolet', 'BMW', 'Mercedes', 'Hyundai', 'Volkswagen']
    car_models = {
        'Toyota': ['Camry', 'Corolla', 'RAV4'], 'Honda': ['Civic', 'Accord', 'CR-V'],
        'Ford': ['F-150', 'Mustang', 'Explorer'], 'Chevrolet': ['Silverado', 'Malibu', 'Equinox'],
        'BMW': ['3 Series', '5 Series', 'X5'], 'Mercedes': ['C-Class', 'E-Class', 'GLC'],
        'Hyundai': ['Elantra', 'Sonata', 'Tucson'], 'Volkswagen': ['Jetta', 'Passat', 'Tiguan']
    }
    salespeople = [fake.name() for _ in range(10)]
    dates = pd.date_range(start="2023-01-01", end="2025-07-07", freq="D")
    df = pd.DataFrame({
        'Salesperson': [random.choice(salespeople) for _ in range(1000)],
        'Car Make': [random.choice(car_makes) for _ in range(1000)],
        'Car Year': [random.randint(2018, 2025) for _ in range(1000)],
        'Date': [random.choice(dates) for _ in range(1000)],
        'Sale Price': [round(random.uniform(15000, 100000), 2) for _ in range(1000)],
        'Commission Earned': [round(random.uniform(500, 5000), 2) for _ in range(1000)]
    })
    df['Car Model'] = df['Car Make'].apply(lambda x: random.choice(car_models[x]))
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Year'] = df['Date'].dt.year
    df['Quarter'] = df['Date'].dt.to_period('Q').astype(str)
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    return df

# ------------------ Layout ------------------
df = generate_sales_data()

app.layout = html.Div([
    html.H2("\U0001F697 Automotive Analytics Dashboard", style={'color': 'white', 'textAlign': 'center', 'fontSize': '28px'}),

    html.Div([
        html.Div([
            html.Label("Salesperson", style={'color': 'white'}),
            dcc.Dropdown(['All'] + sorted(df['Salesperson'].unique()), 'All', id='salesperson')
        ], style={'flex': '1', 'padding': '5px'}),

        html.Div([
            html.Label("Car Make", style={'color': 'white'}),
            dcc.Dropdown(['All'] + sorted(df['Car Make'].unique()), 'All', id='car-make')
        ], style={'flex': '1', 'padding': '5px'}),

        html.Div([
            html.Label("Car Year", style={'color': 'white'}),
            dcc.Dropdown(['All'] + sorted(df['Car Year'].astype(str).unique()), 'All', id='car-year')
        ], style={'flex': '1', 'padding': '5px'}),

        html.Div([
            html.Label("Car Model", style={'color': 'white'}),
            dcc.Dropdown(['All'], 'All', id='car-model')
        ], style={'flex': '1', 'padding': '5px'}),

        html.Div([
            html.Label("Metric", style={'color': 'white'}),
            dcc.Dropdown(['Sale Price', 'Commission Earned'], 'Sale Price', id='metric')
        ], style={'flex': '1', 'padding': '5px'})
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'padding': '10px'}),

    html.Div(id='kpi-cards', style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-evenly', 'color': 'white', 'padding': '10px'}),

    dcc.Tabs(id='tabs', value='kpi-tab', children=[
        dcc.Tab(label='KPI Trend', value='kpi-tab'),
        dcc.Tab(label='Heatmap', value='heatmap-tab'),
        dcc.Tab(label='Top Performers', value='top-tab'),
        dcc.Tab(label='Model Comparison', value='model-tab')
    ], style={'padding': '0px 10px'}),

    html.Div(id='tab-content', style={'padding': '20px'}),

    html.Div([
        html.Button("Download CSV", id='download-button', style={'margin': '10px'}),
        dcc.Download(id="download-csv")
    ], style={'textAlign': 'center'}),

    html.Footer("\u00a9 2025 One Trust | Crafted for smarter auto-financial decisions", style={'textAlign': 'center', 'color': 'gray', 'marginTop': '30px'})
], style={'backgroundColor': '#1C1C1C', 'fontFamily': 'Segoe UI', 'maxWidth': '1280px', 'margin': 'auto'})

# ------------------ Callbacks ------------------
@app.callback(
    Output('car-model', 'options'),
    Input('car-make', 'value')
)
def update_car_models(make):
    if make == 'All':
        return [{'label': 'All', 'value': 'All'}]
    models = df[df['Car Make'] == make]['Car Model'].unique()
    return [{'label': m, 'value': m} for m in ['All'] + sorted(models)]

@app.callback(
    Output('kpi-cards', 'children'),
    Output('tab-content', 'children'),
    Input('salesperson', 'value'),
    Input('car-make', 'value'),
    Input('car-year', 'value'),
    Input('car-model', 'value'),
    Input('metric', 'value'),
    Input('tabs', 'value')
)
def update_dashboard(sp, make, year, model, metric, tab):
    dff = df.copy()
    if sp != 'All': dff = dff[dff['Salesperson'] == sp]
    if make != 'All': dff = dff[dff['Car Make'] == make]
    if year != 'All': dff = dff[dff['Car Year'].astype(str) == year]
    if model != 'All': dff = dff[dff['Car Model'] == model]

    total_sales = f"${dff['Sale Price'].sum():,.0f}"
    total_comm = f"${dff['Commission Earned'].sum():,.0f}"
    avg_price = f"${dff['Sale Price'].mean():,.0f}" if not dff.empty else "$0"
    count = f"{dff.shape[0]:,}"

    kpis = [
        html.Div([html.H4("Total Sales"), html.P(total_sales)]),
        html.Div([html.H4("Total Commission"), html.P(total_comm)]),
        html.Div([html.H4("Avg Sale Price"), html.P(avg_price)]),
        html.Div([html.H4("Transactions"), html.P(count)])
    ]

    if tab == 'kpi-tab':
        if dff.empty:
            content = html.P("No data available", style={'color': 'white'})
        else:
            trend_df = dff.groupby('Month')[['Sale Price', 'Commission Earned']].sum().reset_index()
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=trend_df['Month'], y=trend_df['Sale Price'], name='Sale Price'))
            fig.add_trace(go.Scatter(x=trend_df['Month'], y=trend_df['Commission Earned'], name='Commission'))
            fig.update_layout(template='plotly_dark', height=500)
            content = dcc.Graph(figure=fig)

    elif tab == 'heatmap-tab':
        if dff.empty:
            content = html.P("No data available", style={'color': 'white'})
        else:
            heatmap_data = dff.pivot_table(values=metric, index='Salesperson', columns='Car Make', aggfunc='sum', fill_value=0)
            fig = go.Figure(data=go.Heatmap(z=heatmap_data.values, x=heatmap_data.columns, y=heatmap_data.index, colorscale='Greys'))
            fig.update_layout(template='plotly_dark', height=500)
            content = dcc.Graph(figure=fig)

    elif tab == 'top-tab':
        if dff.empty:
            content = html.P("No data available", style={'color': 'white'})
        else:
            top_df = dff.groupby('Salesperson')[metric].sum().nlargest(10).reset_index()
            fig = go.Figure(data=go.Bar(x=top_df['Salesperson'], y=top_df[metric]))
            fig.update_layout(template='plotly_dark', height=500)
            content = dcc.Graph(figure=fig)

    elif tab == 'model-tab':
        if dff.empty:
            content = html.P("No data available", style={'color': 'white'})
        else:
            model_data = dff.groupby(['Car Make', 'Car Model']).agg({
                'Sale Price': ['mean', 'sum', 'count'],
                'Commission Earned': 'mean'
            }).round(2)
            model_data.columns = ['Avg Sale Price', 'Total Sales', 'Transaction Count', 'Avg Commission']
            model_data = model_data.reset_index()
            content = dash_table.DataTable(
                data=model_data.to_dict('records'),
                columns=[{"name": i, "id": i} for i in model_data.columns],
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'backgroundColor': '#1C1C1C', 'color': 'white'},
                style_header={'backgroundColor': '#2A2A2A', 'color': 'white'}
            )

    return kpis, content

@app.callback(
    Output("download-csv", "data"),
    Input("download-button", "n_clicks"),
    State('salesperson', 'value'),
    State('car-make', 'value'),
    State('car-year', 'value'),
    State('car-model', 'value'),
    prevent_initial_call=True
)
def download_filtered(n, sp, make, year, model):
    dff = df.copy()
    if sp != 'All': dff = dff[dff['Salesperson'] == sp]
    if make != 'All': dff = dff[dff['Car Make'] == make]
    if year != 'All': dff = dff[dff['Car Year'].astype(str) == year]
    if model != 'All': dff = dff[dff['Car Model'] == model]
    return dcc.send_data_frame(dff.to_csv, filename="filtered_data.csv", index=False)

def run_dash():
    app.run_server(host='0.0.0.0', port=8050, debug=False)

