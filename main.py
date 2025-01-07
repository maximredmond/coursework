import csv
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd

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

# File path to the CSV file
file_path = '90E2E48_ALL_LATEST.csv'

# Sort the data
sorted_data = sort_data_by_country_gender_age(file_path)

# Print the result
for country, genders in sorted_data.items():
    print(country)
    for gender, age in genders.items():
        print(f"  {gender}: {age}")

# Prepare data for scatter plot
countries = []
ages = []
genders = []

for country, gender_data in sorted_data.items():
    for gender, age in gender_data.items():
        countries.append(country)
        ages.append(age)
        genders.append(gender)

# Create scatter plot
plt.figure(figsize=(10, 6))
colors = {'MALE': 'blue', 'FEMALE': 'red', 'TOTAL': 'green'}

for gender in set(genders):
    if gender not in colors:
        print(f"Warning: Gender '{gender}' is not in the color mapping. Skipping.")
        continue
    gender_ages = [ages[i] for i in range(len(ages)) if genders[i] == gender]
    gender_countries = [countries[i] for i in range(len(countries)) if genders[i] == gender]
    plt.scatter(gender_countries, gender_ages, label=gender, c=colors[gender])

plt.xlabel('Country')
plt.ylabel('Life Expectancy (2019)')
plt.title('Life Expectancy by Country and Gender (2019)')
plt.legend()
plt.xticks(rotation=90, fontsize=8)
plt.tight_layout()
plt.ylim(bottom=0)
plt.show()
