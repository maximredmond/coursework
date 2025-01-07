import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, ColumnDataSource
from bokeh.models import HoverTool

def get_life_expectancy(file_path, year=2019, gender='FEMALE'):
    # Create a dictionary for life expectancy data by country
    life_exp_data = {}

    data = pd.read_csv(file_path)
    for _, row in data.iterrows():
        if row['DIM_TIME'] == year and row['DIM_GEO_CODE_TYPE'] == 'COUNTRY' and row['DIM_SEX'] == gender:
            country = row['GEO_NAME_SHORT']
            life_exp = float(row['AMOUNT_N'])
            life_exp_data[country] = life_exp

    return life_exp_data

def get_doctors_per_capita(file_path, year=2022):
    # Create a dictionary for doctors per capita data
    doctors_data = {}

    data = pd.read_csv(file_path)
    for _, row in data.iterrows():
        if row['Period'] == year:
            country = row['Location']
            doctors = float(row['FactValueNumeric'])
            doctors_data[country] = doctors

    return doctors_data

# File paths to the CSV files
life_expectancy_file_path = '90E2E48_ALL_LATEST.csv'  # Replace with your life expectancy data file path
doctors_file_path = '5dcef02b-455e-42f2-8223-1fd11ccdfe43.csv'  # Replace with your doctors per capita data file path

# Get life expectancy data
life_exp_data = get_life_expectancy(life_expectancy_file_path, year=2019, gender='FEMALE')

# Get number of doctors per capita
doctors_data = get_doctors_per_capita(doctors_file_path, year=2022)

# Prepare data for scatter plot
scatter_x = []
scatter_y = []
labels = []

for country, life_exp in life_exp_data.items():
    if country in doctors_data:
        scatter_x.append(doctors_data[country])
        scatter_y.append(life_exp)
        labels.append(country)

# Perform linear regression for the line of best fit
coefficients = np.polyfit(scatter_x, scatter_y, 1)
line_func = np.poly1d(coefficients)

# Generate data for the line of best fit
x_fit = np.linspace(min(scatter_x), max(scatter_x), 100)
y_fit = line_func(x_fit)

# Create scatter plot using Bokeh
source = ColumnDataSource(data={
    'x': scatter_x,
    'y': scatter_y,
    'label': labels
})

p = figure(title='Life Expectancy (2019) vs. Number of Doctors per Capita (2022)',
           x_axis_label='Doctors per 10,000 Population',
           y_axis_label='Life Expectancy (years)',
           tools="pan,box_zoom,reset,hover"
           , x_axis_type="log")

p.scatter('x', 'y', size=8, source=source, alpha=0.7, legend_label='Data Points')


# Add hover tool
hover = p.select_one(HoverTool)
hover.tooltips = [
    ("Country", "@label"),
    ("Doctors per 10,000", "@x{0.0}"),
    ("Life Expectancy", "@y{0.0}")
]

p.legend.location = "top_left"

show(p)
