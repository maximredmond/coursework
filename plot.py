import pandas as pd
from bokeh.plotting import figure, show, ColumnDataSource
from bokeh.models import HoverTool
from bokeh.layouts import gridplot

# Read the cleaned data
df = pd.read_csv('cleaned_data.csv')

# Extract the data into lists
countries = list(df['Country'])
life_expectancy = list(df['Life Expectancy'])
gdp = list(df['GDP'])
doctors_per_capita = list(df['Doctors Per Capita'])
water_quality = list(df['Water Quality'])

regions = {
    "Europe": [
        "France", "Sweden", "Latvia", "Denmark", "Spain",
        "Ireland", "Portugal", "Montenegro", "Estonia", "Austria", "Germany",
        "Lithuania", "Romania", "Belarus", "Poland", "Malta", "Finland", "Belgium",
        "Norway", "Albania", "Hungary", "Bulgaria", "Bosnia and Herzegovina",
        "Croatia", "Greece", "Italy", "Slovenia", "North Macedonia", "Iceland", "Switzerland"
    ],
    "Africa": [
        "Sao Tome and Principe", "Mauritius", "Liberia", "Mozambique", "Togo",
        "Zambia", "Niger", "Ethiopia", "Gabon", "Sierra Leone", "Tunisia", "Rwanda",
        "Senegal", "Botswana", "Namibia", "Burkina Faso", "Benin", "Algeria", "Ghana",
        "Mauritania", "South Africa", "Nigeria"
    ],
    "Asia": [
        "Sri Lanka", "Turkmenistan", "China", "Malaysia", "Singapore", "Philippines",
        "Bangladesh", "Jordan", "Uzbekistan", "Afghanistan", "Nepal", "Tajikistan",
        "Armenia", "Azerbaijan", "Indonesia", "Saudi Arabia", "Lebanon", "Thailand",
        "Pakistan", "Mongolia", "United Arab Emirates", "Kazakhstan", "Iraq",
        "Cambodia", "Israel", "Oman", "Bhutan", "Maldives", "Myanmar"
    ],
    "North America": [
        "Panama", "Mexico", "Canada", "Dominican Republic", "Trinidad and Tobago",
        "Cuba", "Costa Rica"
    ],
    "South America": [
        "Colombia", "Ecuador", "Chile", "Brazil"
    ],
    "Oceania": [
        "Tonga", "Vanuatu", "Australia", "New Zealand", "Papua New Guinea"
    ]
}

asia_average_life_expectancy = sum([life_expectancy[countries.index(country)] for country in regions['Asia']]) / len(regions['Asia'])
europe_average_life_expectancy = sum([life_expectancy[countries.index(country)] for country in regions['Europe']]) / len(regions['Europe'])
north_america_average_life_expectancy = sum([life_expectancy[countries.index(country)] for country in regions['North America']]) / len(regions['North America'])
south_america_average_life_expectancy = sum([life_expectancy[countries.index(country)] for country in regions['South America']]) / len(regions['South America'])
africa_average_life_expectancy = sum([life_expectancy[countries.index(country)] for country in regions['Africa']]) / len(regions['Africa'])

# Create the source data for the GDP vs Life Expectancy plot
gdp_vs_le_source = ColumnDataSource(data={
    'x': gdp,
    'y': life_expectancy,
    'label': countries
})

# Create the GDP vs Life Expectancy plot
gdp_vs_le_plot = figure(title='Life Expectancy vs. GDP per Capita', x_axis_label='GDP per Capita (log scale)', y_axis_label='Life Expectancy', tools="pan,box_zoom,reset,hover", x_axis_type="log")
gdp_vs_le_plot.scatter('x', 'y', size=8, source=gdp_vs_le_source, alpha=0.7)

# Add hover tool
hover = gdp_vs_le_plot.select_one(HoverTool)
hover.tooltips = [
    ("Country", "@label"),
    ("GDP per Capita", "@x{$0,0}"),
    ("Life Expectancy", "@y{0.00}")
]

# Create the source data for the Doctors per Capita vs Life Expectancy plot
dpc_vs_le_source = ColumnDataSource(data={
    'x': doctors_per_capita,
    'y': life_expectancy,
    'label': countries
})

# Create the Doctors per Capita vs Life Expectancy plot
dpc_vs_le_plot = figure(title='Life Expectancy vs. Doctors per Capita', x_axis_label='Doctors per Capita (log scale)', y_axis_label='Life Expectancy', tools="pan,box_zoom,reset,hover", x_axis_type="log")
dpc_vs_le_plot.scatter('x', 'y', size=8, source=dpc_vs_le_source, alpha=0.7)

# Add hover tool
hover = dpc_vs_le_plot.select_one(HoverTool)
hover.tooltips = [
    ("Country", "@label"),
    ("Doctors per Capita", "@x{0.00}"),
    ("Life Expectancy", "@y{0.00}")
]

# Create the source data for the bar chart
regions_list = ["Asia", "Europe", "North America", "South America", "Africa"]
average_life_expectancies = [asia_average_life_expectancy, europe_average_life_expectancy, north_america_average_life_expectancy, south_america_average_life_expectancy, africa_average_life_expectancy]

bar_source = ColumnDataSource(data={
    'regions': regions_list,
    'average_life_expectancy': average_life_expectancies
})

# Create the bar chart
bar_plot = figure(x_range=regions_list, title="Average Life Expectancy by Region", x_axis_label='Region', y_axis_label='Average Life Expectancy', tools="pan,box_zoom,reset,hover")
bar_plot.vbar(x='regions', top='average_life_expectancy', width=0.9, source=bar_source)

# Add hover tool to bar chart
hover = bar_plot.select_one(HoverTool)
hover.tooltips = [
    ("Region", "@regions"),
    ("Average Life Expectancy", "@average_life_expectancy{0.00}")
]

wq_vs_le_source = ColumnDataSource(data={
    'x': water_quality,
    'y': life_expectancy,
    'label': countries
})

wq_vs_le_plot = figure(title='Life Expectancy vs. Water Quality', x_axis_label='Water Quality', y_axis_label='Life Expectancy', tools="pan,box_zoom,reset,hover")
wq_vs_le_plot.scatter('x', 'y', size=8, source=wq_vs_le_source, alpha=0.7)

hover = wq_vs_le_plot.select_one(HoverTool)
hover.tooltips = [
    ("Country", "@label"),
    ("Water Quality", "@x{0.00}"),
    ("Life Expectancy", "@y{0.00}")
]

# Create a grid layout for the plots
grid = gridplot([[gdp_vs_le_plot, dpc_vs_le_plot], [bar_plot, wq_vs_le_plot]], width=600, height=600)

# Show the plots
show(grid)
