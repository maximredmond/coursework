import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, ColumnDataSource
from bokeh.models import HoverTool

def sort_data_by_country_gender(file_path, year=2019, gender='FEMALE'):
    # Create a dictionary for life expectancy data by country
    life_exp_data = {}

    data = pd.read_csv(file_path)
    for _, row in data.iterrows():
        # Filter by the specified year, country type, and gender
        if row['DIM_TIME'] == year and row['DIM_GEO_CODE_TYPE'] == 'COUNTRY' and row['DIM_SEX'] == gender:
            country = row['GEO_NAME_SHORT']
            life_exp = float(row['AMOUNT_N'])
            life_exp_data[country] = life_exp

    return life_exp_data

def get_alcohol_consumption(file_path, year=2019):
    # Create a dictionary for alcohol consumption data
    alc_data = {}

    data = pd.read_csv(file_path)
    for _, row in data.iterrows():
        if row['Year'] == year:
            country = row['Entity']
            alc_value = float(row['Total alcohol consumption per capita (liters of pure alcohol, projected estimates, 15+ years of age)'])
            alc_data[country] = alc_value

    return alc_data

# File paths to the CSV files
life_expectancy_file_path = '90E2E48_ALL_LATEST.csv'  # Replace with your actual file path
alcohol_consumption_file_path = 'total-alcohol-consumption-per-capita-litres-of-pure-alcohol.csv'  # Replace with your actual file path containing the alcohol data

# Get life expectancy data for 2019 (female life expectancy)
life_exp_data = sort_data_by_country_gender(life_expectancy_file_path, year=2019, gender='FEMALE')

# Get alcohol consumption data for 2019
alcohol_data = get_alcohol_consumption(alcohol_consumption_file_path, year=2019)

# Prepare data for scatter plot
scatter_x = []
scatter_y = []
labels = []

for country, life_exp in life_exp_data.items():
    if country in alcohol_data:
        scatter_x.append(alcohol_data[country])
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

p = figure(title='Life Expectancy (2019) vs. Alcohol Consumption (2019)',
           x_axis_label='Alcohol Consumption (liters per capita)',
           y_axis_label='Life Expectancy (years)',
           tools="pan,box_zoom,reset,hover",
           x_axis_type="log")

p.scatter('x', 'y', size=8, source=source, alpha=0.7, legend_label='Data Points')

# Add hover tool
hover = p.select_one(HoverTool)
hover.tooltips = [
    ("Country", "@label"),
    ("Alcohol Consumption", "@x{0.00}"),
    ("Life Expectancy", "@y{0.0}")
]

p.legend.location = "top_left"

show(p)
