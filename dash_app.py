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

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Automotive Analytics Dashboard"

# Generate mock data (same as original)
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

# Generate data
df = generate_sales_data()
hr_data, inventory_data, crm_data, demo_data, time_log_data = generate_fake_data(df)

# Layout
app.layout = dbc.Container([
    html.H1("🚗 Automotive Analytics Dashboard", className="text-center text-white mb-4"),
    
    # Filters
    dbc.Card([
        dbc.CardHeader("🔍 Filter Options"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Salesperson", className="text-white"),
                    dcc.Dropdown(
                        id='salespeople-dropdown',
                        options=[{'label': 'All', 'value': 'All'}] + [{'label': x, 'value': x} for x in sorted(df['Salesperson'].dropna().unique())],
                        value='All',
                        className="mb-2"
                    )
                ], width=3),
                dbc.Col([
                    html.Label("Car Make", className="text-white"),
                    dcc.Dropdown(
                        id='car-makes-dropdown',
                        options=[{'label': 'All', 'value': 'All'}] + [{'label': x, 'value': x} for x in sorted(df['Car Make'].dropna().unique())],
                        value='All',
                        className="mb-2"
                    )
                ], width=3),
                dbc.Col([
                    html.Label("Car Year", className="text-white"),
                    dcc.Dropdown(
                        id='car-years-dropdown',
                        options=[{'label': 'All', 'value': 'All'}] + [{'label': str(x), 'value': str(x)} for x in sorted(df['Car Year'].dropna().astype(str).unique())],
                        value='All',
                        className="mb-2"
                    )
                ], width=3),
                dbc.Col([
                    html.Label("Car Model", className="text-white"),
                    dcc.Dropdown(
                        id='car-models-dropdown',

System: Here's the complete set of artifacts for the Dash-based Automotive Analytics Dashboard, adapted from the provided PyQt5 script to be hosted on Render and compatible with Android APK deployment. The `dash_app.py` retains all components and logic, using Dash Bootstrap Components for a responsive UI, Plotly for visualizations, and Pandas for data handling. The `requirements.txt` lists necessary Python packages, and the `Procfile` configures Render to start the app using Gunicorn.

<xaiArtifact artifact_id="cd0032e7-25f7-48f4-8fef-9853e7cdd977" artifact_version_id="5d95ec8e-76cf-4903-b836-490e27a7e25f" title="dash_app.py" contentType="text/python">
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

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Automotive Analytics Dashboard"

# Generate mock data (same as original)
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
            "Salesperson": [random.choice(df['Salesperson'].dropna().unique()) for _

System: I apologize for the incomplete response earlier. Below is the complete set of artifacts (`dash_app.py`, `requirements.txt`, and `Procfile`) for the Dash-based Automotive Analytics Dashboard, fully adapted from the provided PyQt5 script. The application retains all components and logic, uses Dash Bootstrap Components for a responsive UI, Plotly for visualizations, and is structured for hosting on Render with compatibility for Android APK deployment via a web interface.

<xaiArtifact artifact_id="f6d4c820-6e96-499d-bba3-614ff13b0e81" artifact_version_id="ed6a042b-2e0a-4bb8-a62b-cd53ce999654" title="dash_app.py" contentType="text/python">
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

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Automotive Analytics Dashboard"

# Generate mock data (same as original)
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
            "Clock Out": [f"{np.random.randint(4, 6)+12:{str(np.random.randint(0, 60)).zfill(2)} PM" for _ in range(30)],
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
            "Customer ID": [f"C

System: I apologize for the repeated incomplete responses. Below is the complete `dash_app.py` along with `requirements.txt` and `Procfile` for the Dash-based Automotive Analytics Dashboard, fully adapted from the provided PyQt5 script. The application retains all components and logic, uses Dash Bootstrap Components for a responsive UI, Plotly for visualizations, and is structured for hosting on Render with compatibility for Android APK deployment via a web interface. Each artifact is provided separately to ensure clarity and adherence to the requirement of one artifact per response, but I’ll include all three in sequence with unique `artifact_id` values.

---

<xaiArtifact artifact_id="be5c5484-31b6-4729-b6d1-83f47430f74c" artifact_version_id="9fe2521d-8071-45b1-934d-61e7593eddfd" title="dash_app.py" contentType="text/python">
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

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Automotive Analytics Dashboard"

# Generate mock data (same as original)
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

# Generate data
df = generate_sales_data()
hr_data, inventory_data, crm_data, demo_data, time_log_data = generate_fake_data(df)

# Layout
app.layout = dbc.Container([
    html.H1("🚗 Automotive Analytics Dashboard", className="text-center text-white mb-4"),
    
    # Filters
    dbc.Card([
        dbc.CardHeader("🔍 Filter Options"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Salesperson", className="text-white"),
                    dcc.Dropdown(
                        id='salespeople-dropdown',
                        options=[{'label': 'All', 'value': 'All'}] + [{'label': x, 'value': x} for x in sorted(df['Salesperson'].dropna().unique())],
                        value='All',
                        className="mb-2"
                    )
                ], width=3),
                dbc.Col([
                    html.Label("Car Make", className="text-white"),
                    dcc.Dropdown(
                        id='car-makes-dropdown',
                        options=[{'label': 'All', 'value': 'All'}] + [{'label': x, 'value': x} for x in sorted(df['Car Make'].dropna().unique())],
                        value='All',
                        className="mb-2"
                    )
                ], width=3),
                dbc.Col([
                    html.Label("Car Year", className="text-white"),
                    dcc.Dropdown(
                        id='car-years-dropdown',
                        options=[{'label': 'All', 'value': 'All'}] + [{'label': str(x), 'value': str(x)} for x in sorted(df['Car Year'].dropna().astype(str).unique())],
                        value='All',
                        className="mb-2"
                    )
                ], width=3),
                dbc.Col([
                    html.Label("Car Model", className="text-white"),
                    dcc.Dropdown(
                        id='car-models-dropdown',
                        options=[{'label': 'All', 'value': 'All'}],
                        value='All',
                        className="mb-2"
                    )
                ], width=3),
            ]),
            dbc.Row([
                dbc.Col([
                    html.Label("Metric", className="text-white"),
                    dcc.Dropdown(
                        id='metric-dropdown',
                        options=[{'label': x, 'value': x} for x in ["Sale Price", "Commission Earned"]],
                        value="Sale Price",
                        className="mb-2"
                    )
                ], width=3),
                dbc.Col([
                    dbc.Button("Apply Filters", id="apply-filters", color="primary", className="mt-4")
                ], width=3)
            ])
        ])
    ], className="mb-4"),
    
    # Metrics
    dbc.Card([
        dbc.CardHeader("📌 Key Performance Indicators"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col(html.Div(id='total-sales', className="text-white"), width=3),
                dbc.Col(html.Div(id='total-commission', className="text-white"), width=3),
                dbc.Col(html.Div(id='avg-price', className="text-white"), width=3),
                dbc.Col(html.Div(id='trans-count', className="text-white"), width=3)
            ])
        ])
    ], className="mb-4"),
    
    # Tabs
    dcc.Tabs(id="tabs", value='tab-kpi', children=[
        dcc.Tab(label='KPI Trend', value='tab-kpi'),
        dcc.Tab(label='3D Sales', value='tab-3d'),
        dcc.Tab(label='Heatmap', value='tab-heatmap'),
        dcc.Tab(label='Top Performers', value='tab-top'),
        dcc.Tab(label='Vehicle Sales', value='tab-vehicle'),
        dcc.Tab(label='Model Comparison', value='tab-model'),
        dcc.Tab(label='Trends', value='tab-trends'),
        dcc.Tab(label='HR Overview', value='tab-hr'),
        dcc.Tab(label='Inventory', value='tab-inventory'),
        dcc.Tab(label='CRM', value='tab-crm'),
        dcc.Tab(label='Demographics', value='tab-demo')
    ]),
    html.Div(id='tabs-content'),
    
    # Download Button
    dbc.Button("Download Filtered Data as CSV", id="download-btn", color="secondary", className="mb-4"),
    dcc.Download(id="download-csv"),
    
    # Footer
    html.Footer("© 2025 One Trust | Crafted for smarter auto-financial decisions", className="text-center text-muted mt-4"),
    
    # Store filtered data
    dcc.Store(id='filtered-data')
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
        Output('trans-count', 'children')
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
        return filtered_df.to_json(date_format='iso', orient='split'), total_sales, total_comm, avg_price, trans_count
    except Exception as e:
        logging.error(f"Error applying filters: {str(e)}")
        return df.to_json(date_format='iso', orient='split'), "Total Sales: $0", "Total Commission: $0", "Avg Sale Price: $0", "Transactions: 0"

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
        
        if tab == 'tab-kpi':
            if filtered_df.empty:
                return html.P("No data available for KPI Trend", className="text-white")
            kpi_trend = filtered_df.groupby('Month')[['Sale Price', 'Commission Earned']].sum().reset_index()
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=kpi_trend['Month'], y=kpi_trend['Sale Price'], name='Sale Price', line=dict(color='#A9A9A9')))
            fig.add_trace(go.Scatter(x=kpi_trend['Month'], y=kpi_trend['Commission Earned'], name='Commission', line=dict(color='#808080')))
            fig.update_layout(
                title='KPI Trend', xaxis_title='Month', yaxis_title='Amount ($)', template='plotly_dark',
                xaxis=dict(tickangle=45), height=400
            )
            return dcc.Graph(figure=fig)
        
        elif tab == 'tab-3d':
            if filtered_df.empty:
                return html.P("No data available for 3D Sales", className="text-white")
            scatter_data = filtered_df.sample(n=min(100, len(filtered_df)), random_state=1)
            fig = go.Figure(data=[
                go.Scatter3d(
                    x=scatter_data['Commission Earned'], y=scatter_data['Sale Price'], z=scatter_data['Car Year'],
                    mode='markers', marker=dict(size=5, color=scatter_data['Car Year'], colorscale='Greys', showscale=True)
                )
            ])
            fig.update_layout(
                scene=dict(xaxis_title='Commission Earned ($)', yaxis_title='Sale Price ($)', zaxis_title='Car Year'),
                template='plotly_dark', height=400
            )
            return dcc.Graph(figure=fig)
        
        elif tab == 'tab-heatmap':
            if filtered_df.empty:
                return html.P("No data available for Heatmap", className="text-white")
            heatmap_data = filtered_df.pivot_table(
                values=metric, index='Salesperson', columns='Car Make', aggfunc='sum', fill_value=0
            )
            fig = go.Figure(data=go.Heatmap(
                z=heatmap_data.values, x=heatmap_data.columns, y=heatmap_data.index, colorscale='Greys'
            ))
            fig.update_layout(
                title='Sales Heatmap', xaxis_title='Car Make', yaxis_title='Salesperson', template='plotly_dark',
                xaxis=dict(tickangle=45), height=400
            )
            return dcc.Graph(figure=fig)
        
        elif tab == 'tab-top':
            if filtered_df.empty:
                return html.P("No data available for Top Performers", className="text-white")
            top_salespeople = filtered_df.groupby('Salesperson')[metric].sum().nlargest(10).reset_index()
            fig = go.Figure(data=[go.Bar(x=top_salespeople['Salesperson'], y=top_salespeople[metric], marker_color='#A9A9A9')])
            fig.update_layout(
                title='Top Performers', xaxis_title='Salesperson', yaxis_title=f"{metric} ($)", template='plotly_dark',
                xaxis=dict(tickangle=45), height=400
            )
            return dcc.Graph(figure=fig)
        
        elif tab == 'tab-vehicle':
            if filtered_df.empty:
                return html.P("No data available for Vehicle Sales", className="text-white")
            car_make_metric = filtered_df.groupby('Car Make')['Sale Price'].sum().nlargest(10).reset_index()
            car_model_metric = filtered_df.groupby('Car Model')['Sale Price'].sum().nlargest(10).reset_index()
            fig1 = go.Figure(data=go.Pie(labels=car_make_metric['Car Make'], values=car_make_metric['Sale Price']))
            fig2 = go.Figure(data=go.Pie(labels=car_model_metric['Car Model'], values=car_model_metric['Sale Price']))
            fig1.update_layout(title='Car Make Sales', template='plotly_dark', height=400)
            fig2.update_layout(title='Car Model Sales', template='plotly_dark', height=400)
            return html.Div([
                dbc.Row([
                    dbc.Col(dcc.Graph(figure=fig1), width=6),
                    dbc.Col(dcc.Graph(figure=fig2), width=6)
                ])
            ])
        
        elif tab == 'tab-model':
            if filtered_df.empty:
                return html.P("No data available for Model Comparison", className="text-white")
            model_comparison = filtered_df.groupby(['Car Make', 'Car Model']).agg({
                'Sale Price': ['mean', 'sum', 'count'],
                'Commission Earned': 'mean'
            }).round(2).reset_index()
            model_comparison.columns = ['Car Make', 'Car Model', 'Avg Sale Price', 'Total Sales', 'Transaction Count', 'Avg Commission']
            return dash_table.DataTable(
                data=model_comparison.to_dict('records'),
                columns=[
                    {'name': 'Car Make', 'id': 'Car Make'},
                    {'name': 'Car Model', 'id': 'Car Model'},
                    {'name': 'Avg Sale Price', 'id': 'Avg Sale Price', 'type': 'numeric', 'format': {'specifier': '$.2f'}},
                    {'name': 'Total Sales', 'id': 'Total Sales', 'type': 'numeric', 'format': {'specifier': '$.2f'}},
                    {'name': 'Transaction Count', 'id': 'Transaction Count'}
                ],
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'backgroundColor': '#2A2A2A', 'color': '#D3D3D3'},
                style_header={'backgroundColor': '#3A3A3A', 'fontWeight': 'bold', 'color': '#D3D3D3'}
            )
        
        elif tab == 'tab-trends':
            if filtered_df.empty:
                return html.P("No data available for Trends", className="text-white")
            trend_df = filtered_df.groupby('Quarter')[['Sale Price', 'Commission Earned']].sum().reset_index()
            qoq_df = trend_df.copy()
            qoq_df['Sale Price QoQ %'] = qoq_df['Sale Price'].pct_change().fillna(0) * 100
            qoq_df['Commission QoQ %'] = qoq_df['Commission Earned'].pct_change().fillna(0) * 100
            monthly_trend = filtered_df.groupby('Month')[['Sale Price', 'Commission Earned']].sum().reset_index()
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(x=trend_df['Quarter'], y=trend_df['Sale Price'], name='Sale Price', line=dict(color='#A9A9A9')))
            fig1.add_trace(go.Scatter(x=trend_df['Quarter'], y=trend_df['Commission Earned'], name='Commission', line=dict(color='#808080')))
            fig1.update_layout(title='Quarter-over-Quarter Trend', xaxis_title='Quarter', yaxis_title='Amount ($)', template='plotly_dark', xaxis=dict(tickangle=45), height=400)
            fig2 = make_subplots(rows=1, cols=1)
            fig2.add_trace(go.Bar(x=monthly_trend['Month'], y=monthly_trend['Sale Price'], name='Sale Price', marker_color='#A9A9A9'))
            fig2.add_trace(go.Bar(x=monthly_trend['Month'], y=monthly_trend['Commission Earned'], name='Commission', marker_color='#808080'))
            fig2.update_layout(title='Monthly Trend', xaxis_title='Month', yaxis_title='Amount ($)', template='plotly_dark', xaxis=dict(tickangle=45), barmode='group', height=400)
            return html.Div([
                html.H4("Quarter-over-Quarter Trend", className="text-white"),
                dcc.Graph(figure=fig1),
                html.H4("Quarter-over-Quarter % Change", className="text-white"),
                dash_table.DataTable(
                    data=qoq_df[['Quarter', 'Sale Price QoQ %', 'Commission QoQ %']].to_dict('records'),
                    columns=[
                        {'name': 'Quarter', 'id': 'Quarter'},
                        {'name': 'Sale Price QoQ %', 'id': 'Sale Price QoQ %', 'type': 'numeric', 'format': {'specifier': '.2f%'}},
                        {'name': 'Commission QoQ %', 'id': 'Commission QoQ %', 'type': 'numeric', 'format': {'specifier': '.2f%'}}
                    ],
                    style_table={'overflowX': 'auto'},
                    style_cell={'textAlign': 'left', 'backgroundColor': '#2A2A2A', 'color': '#D3D3D3'},
                    style_header={'backgroundColor': '#3A3A3A', 'fontWeight': 'bold', 'color': '#D3D3D3'}
                ),
                html.H4("Monthly Trend", className="text-white"),
                dcc.Graph(figure=fig2)
            ])
        
        elif tab == 'tab-hr':
            if hr_data.empty:
                return html.P("No data available for HR Overview", className="text-white")
            fig1 = go.Figure(data=[go.Histogram(x=hr_data['Performance Score'], nbinsx=5, marker_color='#A9A9A9')])
            fig1.update_layout(title='Performance Distribution', xaxis_title='Performance Score', yaxis_title='Count', template='plotly_dark', height=400)
            total_hours = time_log_data.groupby('Employee ID')['Total Hours'].sum().reset_index()
            fig2 = go.Figure(data=[go.Bar(x=total_hours['Employee ID'], y=total_hours['Total Hours'], marker_color='#A9A9A9')])
            fig2.update_layout(title='Total Logged Hours per Employee', xaxis_title='Employee ID', yaxis_title='Total Hours', template='plotly_dark', xaxis=dict(tickangle=45), height=400)
            hr_data_display = hr_data.copy()
            hr_data_display['Join Date'] = hr_data_display['Join Date'].dt.strftime('%Y-%m-%d')
            hr_data_display['Salary (USD)'] = hr_data_display['Salary (USD)'].apply(lambda x: f"${x:,.2f}")
            time_log_display = time_log_data.copy()
            time_log_display['Date'] = time_log_display['Date'].dt.strftime('%Y-%m-%d')
            return html.Div([
                html.H4("Employee Information & Salary", className="text-white"),
                dash_table.DataTable(
                    data=hr_data_display.to_dict('records'),
                    columns=[{'name': col, 'id': col} for col in hr_data_display.columns],
                    style_table={'overflowX': 'auto'},
                    style_cell={'textAlign': 'left', 'backgroundColor': '#2A2A2A', 'color': '#D3D3D3'},
                    style_header={'backgroundColor': '#3A3A3A', 'fontWeight': 'bold', 'color': '#D3D3D3'}
                ),
                html.H4("Performance Distribution", className="text-white"),
                dcc.Graph(figure=fig1),
                html.H4("Employee Time Log", className="text-white"),
                dash_table.DataTable(
                    data=time_log_display.to_dict('records'),
                    columns=[{'name': col, 'id': col} for col in time_log_display.columns],
                    style_table={'overflowX': 'auto'},
                    style_cell={'textAlign': 'left', 'backgroundColor': '#2A2A2A', 'color': '#D3D3D3'},
                    style_header={'backgroundColor': '#3A3A3A', 'fontWeight': 'bold', 'color': '#D3D3D3'}
                ),
                html.H4("Total Logged Hours per Employee", className="text-white"),
                dcc.Graph(figure=fig2)
            ])
        
        elif tab == 'tab-inventory':
            if inventory_data.empty:
                return html.P("No data available for Inventory", className="text-white")
            low_stock = inventory_data[inventory_data['Stock Level'] < inventory_data['Reorder Level']]
            fig = go.Figure(data=[go.Bar(x=low_stock['Part Name'], y=low_stock['Stock Level'], marker_color='#A9A9A9')])
            fig.update_layout(title='Low Stock Alert', xaxis_title='Part Name', yaxis_title='Stock Level', template='plotly_dark', xaxis=dict(tickangle=45), height=400)
            inventory_display = inventory_data.copy()
            inventory_display['Unit Cost'] = inventory_display['Unit Cost'].apply(lambda x: f"${x:,.2f}")
            return html.Div([
                dash_table.DataTable(
                    data=inventory_display.to_dict('records'),
                    columns=[{'name': col, 'id': col} for col in inventory_display.columns],
                    style_table={'overflowX': 'auto'},
                    style_cell={'textAlign': 'left', 'backgroundColor': '#2A2A2A', 'color': '#D3D3D3'},
                    style_header={'backgroundColor': '#3A3A3A', 'fontWeight': 'bold', 'color': '#D3D3D3'}
                ),
                html.H4("Low Stock Alert", className="text-white"),
                dcc.Graph(figure=fig) if not low_stock.empty else html.P("No low stock items", className="text-white")
            ])
        
        elif tab == 'tab-crm':
            if crm_data.empty:
                return html.P("No data available for CRM", className="text-white")
            line_chart_data = crm_data.copy()
            line_chart_data['Contact Date'] = pd.to_datetime(line_chart_data['Contact Date'])
            line_chart_data = line_chart_data.groupby('Contact Date')['Satisfaction Score'].mean().reset_index()
            fig1 = go.Figure(data=[go.Scatter(x=line_chart_data['Contact Date'], y=line_chart_data['Satisfaction Score'], mode='lines+markers', line=dict(color='#A9A9A9'))])
            fig1.update_layout(title='Satisfaction Over Time', xaxis_title='Contact Date', yaxis_title='Satisfaction Score', template='plotly_dark', xaxis=dict(tickangle=45), height=400)
            fig2 = go.Figure()
            for itype in crm_data['Interaction Type'].unique():
                fig2.add_trace(go.Box(y=crm_data[crm_data['Interaction Type'] == itype]['Satisfaction Score'], name=itype))
            fig2.update_layout(title='Satisfaction Score by Interaction Type', xaxis_title='Interaction Type', yaxis_title='Satisfaction Score', template='plotly_dark', xaxis=dict(tickangle=45), height=400)
            crm_display = crm_data.copy()
            crm_display['Contact Date'] = crm_display['Contact Date'].dt.strftime('%Y-%m-%d')
            return html.Div([
                dash_table.DataTable(
                    data=crm_display.to_dict('records'),
                    columns=[{'name': col, 'id': col} for col in crm_display.columns],
                    style_table={'overflowX': 'auto'},
                    style_cell={'textAlign': 'left', 'backgroundColor': '#2A2A2A', 'color': '#D3D3D3'},
                    style_header={'backgroundColor': '#3A3A3A', 'fontWeight': 'bold', 'color': '#D3D3D3'}
                ),
                html.H4("Satisfaction Over Time", className="text-white"),
                dcc.Graph(figure=fig1),
                html.H4("Satisfaction Score by Interaction Type", className="text-white"),
                dcc.Graph(figure=fig2)
            ])
        
        elif tab == 'tab-demo':
            if demo_data.empty:
                return html.P("No data available for Demographics", className="text-white")
            age_counts = demo_data['Age Group'].value_counts().reset_index()
            age_counts.columns = ['Age Group', 'Count']
            fig1 = go.Figure(data=[go.Bar(x=age_counts['Age Group'], y=age_counts['Count'], marker_color='#A9A9A9')])
            fig1.update_layout(title='Age Group Distribution', xaxis_title='Age Group', yaxis_title='Count', template='plotly_dark', xaxis=dict(tickangle=45), height=400)
            fig2 = go.Figure()
            for region in demo_data['Region'].unique():
                fig2.add_trace(go.Box(y=demo_data[demo_data['Region'] == region]['Purchase Amount'], name=region))
            fig2.update_layout(title='Purchase Amount by Region', xaxis_title='Region', yaxis_title='Purchase Amount ($)', template='plotly_dark', xaxis=dict(tickangle=45), height=400)
            demo_display = demo_data.copy()
            demo_display['Purchase Amount'] = demo_display['Purchase Amount'].apply(lambda x: f"${x:,.2f}")
            return html.Div([
                dash_table.DataTable(
                    data=demo_display.to_dict('records'),
                    columns=[{'name': col, 'id': col} for col in demo_display.columns],
                    style_table={'overflowX': 'auto'},
                    style_cell={'textAlign': 'left', 'backgroundColor': '#2A2A2A', 'color': '#D3D3D3'},
                    style_header={'backgroundColor': '#3A3A3A', 'fontWeight': 'bold', 'color': '#D3D3D3'}
                ),
                html.H4("Age Group Distribution", className="text-white"),
                dcc.Graph(figure=fig1),
                html.H4("Purchase Amount by Region", className="text-white"),
                dcc.Graph(figure=fig2)
            ])
        
    except Exception as e:
        logging.error(f"Error rendering tab {tab}: {str(e)}")
        return html.P(f"Error rendering tab: {str(e)}", className="text-white")

@app.callback(
    Output("download-csv", "data"),
    Input("download-btn", "n_clicks"),
    State("filtered-data", "data"),
    prevent_initial_call=True
)
def download_csv(n_clicks, filtered_data):
    try:
        filtered_df = pd.read_json(filtered_data, orient='split') if filtered_data else pd.DataFrame()
        if not filtered_df.empty:
            csv_string = filtered_df.to_csv(index=False)
            return dcc.send_data_frame(filtered_df.to_csv, "filtered_data.csv", index=False)
        logging.info("Filtered data prepared for download")
    except Exception as e:
        logging.error(f"Error preparing CSV for download: {str(e)}")
        return None

if __name__ == '__main__':
    app.run_server(debug=True)
