import pandas as pd

# Read the cleaned data
df = pd.read_csv('cleaned_data.csv')

# Extract the data into lists
countries = list(df['Country'])
life_expectancy = list(df['Life Expectancy'])
gdp = list(df['GDP'])
doctors_per_capita = list(df['Doctors Per Capita'])
water_quality = list(df['Water Quality'])

# Get mean median and mode of each column
def mean_median_mode(column):
    mean = sum(column) / len(column)
    if len(column) % 2 == 0:
        median = (column[len(column) // 2] + column[len(column) // 2 - 1]) / 2
    else:
        median = column[len(column) / 2]
    mode = max(set([round(x) for x in column]), key=[round(x) for x in column].count)
    range_column = max(column) - min(column)
    return round(mean, 2), round(median, 2), round(mode, 2), round(range_column, 2) 

print("Life Expectancy:")
mean, median, mode, range_column = mean_median_mode(life_expectancy)
print(f"Mean: {mean}, Median: {median}, Mode: {mode}, Range: {range_column}")

print("GDP:")
mean, median, mode, range_column = mean_median_mode(gdp)
print(f"Mean: {mean}, Median: {median}, Mode: {mode}, Range: {range_column}")

print("Doctors per Capita:")
mean, median, mode, range_column = mean_median_mode(doctors_per_capita)
print(f"Mean: {mean}, Median: {median}, Mode: {mode}, Range: {range_column}")

print("Water Quality:")
mean, median, mode, range_column = mean_median_mode(water_quality)
print(f"Mean: {mean}, Median: {median}, Mode: {mode}, Range: {range_column}")
