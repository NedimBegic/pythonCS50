import pandas as pd
import pymysql
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Function to connect to the database
def connecting_to_db():
    connection = pymysql.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE")
    )
    return connection

# Cleaning data and making sure there is no mistakes. 
def clean_mpa_column(df, column_name):
    """
    Cleans a column containing m_MPa values by removing non-numeric characters,
    converting values to numeric, replacing invalid data with 0, and handling
    data truncation by setting the value to 0 if truncation is detected.
    
    Parameters:
    - df: The DataFrame containing the data.
    - column_name: The name of the column to clean.
    
    Returns:
    - The DataFrame with the cleaned column.
    """
    # Replace commas with periods to handle locales that use commas as decimal separators
    df[column_name] = df[column_name].str.replace(',', '.', regex=False)
    
    # Remove any non-numeric characters (keep only numbers and decimal points)
    df[column_name] = df[column_name].str.replace(r'[^\d.]+', '', regex=True)

    # Convert to numeric, invalid entries will become NaN
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce')

    # Replace NaN with 0
    df[column_name] = df[column_name].fillna(0)


    return df


# Cleaning data that are not inputed well
def clean_all_mpa_columns(df):
    """
    Cleans all columns with the suffix 'M_MPa' in the DataFrame.
    
    Parameters:
    - df: The DataFrame containing the data.
    
    Returns:
    - The DataFrame with all cleaned m_MPa columns.
    """
    # Find all columns with 'M_MPa' in the name
    mpa_columns = [col for col in df.columns if 'M_MPa' in col]
    
    # Clean each m_MPa column
    for column in mpa_columns:
        df = clean_mpa_column(df, column)
    
    return df

# Clean data that are not imported well 
def clean_shotcrete_layer(df):
    """
    Cleans the Shotcrete_Layer column by replacing non-numeric values with 0.
    """
    # Replace non-numeric values with 0
    df['Shotcrete_Layer'] = pd.to_numeric(df['Shotcrete_Layer'], errors='coerce')
    df['Shotcrete_Layer'] = df['Shotcrete_Layer'].fillna(0)  # Replace NaN with 0
    
    return df

# Migration of the penetration test data
def penetration_test_migration():
    # Convert the Geotech_DB penetration sheet to csv
    df = pd.read_excel('Geotech_DB.xlsx', sheet_name='Penetration', usecols="A:Q")  
    df.to_csv('penetration.csv', index=False)

    # Connect to the database
    connection = connecting_to_db()

    # Create a cursor object using the cursor() method
    if connection.open:
        cursor = connection.cursor()

        # Read the CSV file
        df = pd.read_csv('penetration.csv')

        # Clean the m_MPa columns (15M_MPa, 30M_MPa, etc.)
        df = clean_all_mpa_columns(df)

        # Clean the Shotcrete_Layer column, replacing any non-numeric value with 0
        df = clean_shotcrete_layer(df)

        # Replace empty strings or non-numeric values with 0 (if any)
        df['Shotcrete_Layer'] = df['Shotcrete_Layer'].replace('', 0)
        df['Shotcrete_Layer'] = df['Shotcrete_Layer'].apply(lambda x: 0 if isinstance(x, str) and x.strip() == '' else x)


        # Replace NaN with 0
        df = df.fillna(0)

        # Write query to insert the data into the penetration table
        query = """
        INSERT INTO penetration (
            FaceID, Batch, Shotcrete_Layer, Spray_Time, Air_Temp, Shotcrete_Temp, Shotcrete_Blend,
            15M_MPa, 30M_MPa, 60M_MPa, 90M_MPa, 120M_MPa, 150M_MPa, 180M_MPa, 240M_MPa, 270M_MPa, 300M_MPa
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Insert data into MySQL table
        for _, row in df.iterrows():
            cursor.execute(query, tuple(row))

        # Commit the transaction
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

       
        # Close the cursor and connection
        cursor.close()
        connection.close()

def main():
    penetration_test_migration()
  
if __name__ == "__main__":
    main()
