import csv
from collections import defaultdict
import pandas as pd

def clean_life_expectancy(file_path):
    # Read the csv and store it in df
    df = pd.read_csv(file_path)
    
    # Remove any duplicate rows
    df = df.drop_duplicates()
    
    # Filter the dataframe to data from 2019
    df = df[df['DIM_TIME'] == 2019]
    # Filter out any non-country regions
    df = df[df['DIM_GEO_CODE_TYPE'] == 'COUNTRY']
    # Filter out male and female to only get the average
    df = df[df['DIM_SEX'] == 'TOTAL']
    
    # Remove any unnecessary columns
    for column in df.columns.values:
        if column not in ['GEO_NAME_SHORT','AMOUNT_N']:
            df.drop(column, axis=1, inplace=True)
            
    # Round values from the life expectancy comma to 2 decimal places
    df['AMOUNT_N'] = df['AMOUNT_N'].apply(lambda value: round(value, 2))
    
    return df


def clean_gdp(file_path):
    # Read the csv and store it in df and skip first 4 rows as they do not contain data
    df = pd.read_csv(file_path, skiprows=4)
    
    # Remove any duplicate rows
    df = df.drop_duplicates()

    # Filter the dataframe to data from 2019 and drop unnecessary columns
    for column in df.columns.values:
        if column not in ['Country Name', '2019']:
            df.drop(column, axis=1, inplace=True)
            
    # Round values from the GDP comma to 2 decimal places
    df['2019'] = df['2019'].apply(lambda value: round(value, 2))
    # Drop any rows with missing values
    df.dropna(subset=['2019'], inplace=True)
    
    return df        
            
def clean_doctors_per_capita(file_path):
    # Read the csv and store it in df
    df = pd.read_csv(file_path)
    
    # Remove any duplicate rows
    df = df.drop_duplicates()
    
    # Filter the dataframe to data from 2019
    df = df[df['Period'] == 2019]
    
    # Remove any unnecessary columns
    for column in df.columns.values:
        if column not in ['Location', 'Value']:
            df.drop(column, axis=1, inplace=True)
           
    # Round values from the doctors per capita comma to 2 decimal places 
    df['Value'] = df['Value'].apply(lambda value: round(value, 2))
    
    return df

def clean_water_quality(file_path):
    # Read the csv and store it in df
    df = pd.read_csv(file_path)
    
    # Remove any duplicate rows
    df = df.drop_duplicates()
    
    return df

    
    
# File paths to the CSV files
life_expectancy_file_path = '90E2E48_ALL_LATEST.csv'
gdp_file_path = 'API_NY.GDP.PCAP.CD_DS2_en_csv_v2_77536.csv'
doctors_per_capita_file_path = '5dcef02b-455e-42f2-8223-1fd11ccdfe43.csv'
water_quality_file_path = 'water-quality-by-country-2024.csv'

# Clean the data
cleaned_le = clean_life_expectancy(life_expectancy_file_path)
cleaned_gdp = clean_gdp(gdp_file_path)
cleaned_dpc = clean_doctors_per_capita(doctors_per_capita_file_path)
cleaned_water_quality = clean_water_quality(water_quality_file_path)

# Rename columns for better usability
cleaned_le = cleaned_le.rename(columns={"GEO_NAME_SHORT": "Country", "AMOUNT_N": "Life Expectancy"})
cleaned_gdp = cleaned_gdp.rename(columns={"Country Name": "Country", "2019": "GDP"})
cleaned_dpc = cleaned_dpc.rename(columns={"Location": "Country", "Value": "Doctors Per Capita"})
cleaned_water_quality = cleaned_water_quality.rename(columns={"country": "Country", "WaterQuality_EPIDrinkingWaterScore_2024": "Water Quality"})

# Merge the dataframes into one
combined_df = cleaned_le.merge(cleaned_gdp, on="Country", how="inner")
combined_df = combined_df.merge(cleaned_dpc, on="Country", how="inner")
combined_df = combined_df.merge(cleaned_water_quality, on="Country", how="inner")

# Save the cleaned data to a new CSV file without the index
combined_df.to_csv('cleaned_data.csv', index=False)