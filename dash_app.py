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
            "Join Date": pd.date_range(start="2018-01
