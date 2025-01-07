import csv
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
from bokeh.plotting import figure, show, ColumnDataSource
from bokeh.models import HoverTool

def sort_data_by_country_gender_age(file_path):
    # Create a nested dictionary structure for the data
    sorted_data = defaultdict(lambda: defaultdict(dict))

    data = pd.read_csv(file_path)
    for _, row in data.iterrows():
        if row['DIM_TIME'] == 2019 and row['DIM_GEO_CODE_TYPE'] == 'COUNTRY':
            country = row['GEO_NAME_SHORT']
            gender = row['DIM_SEX']
            age = float(row['AMOUNT_N'])

            sorted_data[country][gender] = age

    return sorted_data

def get_gdp_per_capita(file_path):
    # Create a dictionary for GDP per capita data
    gdp_data = {}

    data = pd.read_csv(file_path, skiprows=4)
    for _, row in data.iterrows():
        country = row['Country Name']
        gdp_2019 = row['2019']

        if pd.notna(gdp_2019):
            gdp_data[country] = float(gdp_2019)

    return gdp_data

# File paths to the CSV files
life_expectancy_file_path = '90E2E48_ALL_LATEST.csv'
gdp_file_path = 'API_NY.GDP.PCAP.CD_DS2_en_csv_v2_77536.csv'

# Sort the data
sorted_data = sort_data_by_country_gender_age(life_expectancy_file_path)

# Get GDP per capita data
gdp_data = get_gdp_per_capita(gdp_file_path)

# Prepare data for scatter plot
scatter_x = []
scatter_y = []
labels = []

for country, gender_data in sorted_data.items():
    if country in gdp_data:
        gdp = gdp_data[country]
        if 'TOTAL' in gender_data:
            age = gender_data['TOTAL']
            scatter_x.append(gdp)
            scatter_y.append(age)
            labels.append(country)

# Create scatter plot using Bokeh
source = ColumnDataSource(data={
    'x': scatter_x,
    'y': scatter_y,
    'label': labels
})

p = figure(title='Life Expectancy vs. GDP per Capita (2019)', x_axis_label='GDP per Capita (2019)', y_axis_label='Life Expectancy (2019)', tools="pan,box_zoom,reset,hover", x_axis_type="log")
p.scatter('x', 'y', size=8, source=source, alpha=0.7)

# Add hover tool
hover = p.select_one(HoverTool)
hover.tooltips = [
    ("Country", "@label"),
    ("GDP per Capita", "@x"),
    ("Life Expectancy", "@y")
]

show(p)
