import dash
from dash import dcc, html
import pandas as pd
import numpy as np
import plotly.express as px
from faker import Faker
import random

fake = Faker()
app = dash.Dash(__name__)

# Generate mock data
def generate_data(n=100):
    car_makes = ['Toyota', 'Honda', 'Ford', 'BMW']
    salespeople = [fake.name() for _ in range(10)]
    data = {
        'Salesperson': [random.choice(salespeople) for _ in range(n)],
        'Car Make': [random.choice(car_makes) for _ in range(n)],
        'Sale Price': [round(random.uniform(15000, 60000), 2) for _ in range(n)]
    }
    return pd.DataFrame(data)

df = generate_data()

fig = px.bar(df.groupby("Car Make")["Sale Price"].sum().reset_index(), 
             x="Car Make", y="Sale Price", title="Total Sales by Car Make")

app.layout = html.Div([
    html.H1("Automotive Dashboard"),
    dcc.Graph(figure=fig)
])

server = app.server

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8080)