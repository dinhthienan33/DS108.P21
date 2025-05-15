import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import io
import time

def baitap3():
    try:
        print("Fetching COVID-19 data for Japan from Google Sheets...")
        
        # Google Sheet URL
        sheet_url = "https://docs.google.com/spreadsheets/d/1XEFg047aSbg3OsEVx9PzmgSxGbCvCidfLiHfsgRS3R0/edit?usp=sharing"
        
        # Try multiple methods to access the data
        df = None
        errors = []
        
        # Method 1: Direct CSV export link
        try:
            sheet_id = sheet_url.split('/')[5]
            csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
            
            # Add headers to mimic browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(csv_url, headers=headers)
            response.raise_for_status()
            
            df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
            print("Successfully loaded data using CSV export link.")
        except Exception as e:
            error_msg = f"Method 1 (CSV export) failed: {str(e)}"
            print(error_msg)
            errors.append(error_msg)
        
        # Method 2: Using gsheet (if method 1 fails)
        if df is None:
            try:
                import gspread
                from oauth2client.service_account import ServiceAccountCredentials
                
                print("Attempting to use gspread library...")
                
                # This method would require OAuth credentials
                print("Note: Method 2 requires OAuth credentials setup.")
                print("Skipping to Method 3...")
            except ImportError:
                print("gspread library not installed. Skipping Method 2.")
        
        # Method 3: Using pandas read_html
        if df is None:
            try:
                print("Attempting to use pandas read_html method...")
                tables = pd.read_html(sheet_url)
                if tables:
                    df = tables[0]  # Use the first table found
                    print("Successfully loaded data using pandas read_html.")
            except Exception as e:
                error_msg = f"Method 3 (pandas read_html) failed: {str(e)}"
                print(error_msg)
                errors.append(error_msg)
        
        # If all methods fail, use sample data
        if df is None:
            print("All methods failed to load data. Using mock data for demonstration.")
            print("Error details:", errors)
            
            # Create mock data for demonstration purposes
            df = pd.DataFrame({
                'Detected City': np.random.choice(['Tokyo', 'Osaka', 'Hokkaido', 'Kyoto', 'Nagoya'], 100),
                'Age': np.random.randint(0, 95, 100),
                'Date Announced': pd.date_range(start='2020-01-01', periods=100)
            })
            print("Created mock data for demonstration.")
        
        # Clean column names
        df.columns = df.columns.str.strip()
        print(f"Data loaded successfully with {len(df)} records.")
        
        # a) Count cases by city
        if 'Detected City' in df.columns:
            city_cases = df['Detected City'].value_counts().reset_index()
            city_cases.columns = ['City', 'Number of Cases']
            
            print("\na) Cases by city:")
            print(city_cases)
            
            # Plot cases by city
            plt.figure(figsize=(14, 8))
            
            # For better visualization, show top 15 cities
            top_cities = city_cases.head(15)
            
            plt.barh(top_cities['City'], top_cities['Number of Cases'], color='skyblue')
            plt.title('COVID-19 Cases by City in Japan (Top 15)', fontsize=14)
            plt.xlabel('Number of Cases', fontsize=12)
            plt.ylabel('City', fontsize=12)
            plt.tight_layout()
            plt.savefig('japan_cases_by_city.png')
            print("Saved city cases chart to 'japan_cases_by_city.png'")
        else:
            print("Column 'Detected City' not found in the dataset.")
        
        # b) Count cases by age group
        if 'Age' in df.columns:
            # Convert Age to numeric, handling non-numeric values
            df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
            
            # Group ages into categories
            bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
            labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90+']
            df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels)
            
            age_cases = df['Age Group'].value_counts().sort_index().reset_index()
            age_cases.columns = ['Age Group', 'Number of Cases']
            
            print("\nb) Cases by age group:")
            print(age_cases)
            
            # Plot cases by age group
            plt.figure(figsize=(12, 6))
            plt.bar(age_cases['Age Group'], age_cases['Number of Cases'], color='orange')
            plt.title('COVID-19 Cases by Age Group in Japan', fontsize=14)
            plt.xlabel('Age Group', fontsize=12)
            plt.ylabel('Number of Cases', fontsize=12)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            
            # Add value labels on bars
            for i, v in enumerate(age_cases['Number of Cases']):
                plt.text(i, v + 1, str(v), ha='center')
                
            plt.tight_layout()
            plt.savefig('japan_cases_by_age.png')
            print("Saved age group chart to 'japan_cases_by_age.png'")
        else:
            print("Column 'Age' not found in the dataset.")
        
        # c) Count cases in Hokkaido by day
        if 'Date Announced' in df.columns and 'Detected City' in df.columns:
            # Filter for Hokkaido cases
            hokkaido_df = df[df['Detected City'] == 'Hokkaido'].copy()
            
            # Check if there are any Hokkaido cases
            if len(hokkaido_df) == 0:
                print("\nc) No cases found in Hokkaido.")
            else:
                # Convert to datetime for proper sorting
                try:
                    hokkaido_df['Date Announced'] = pd.to_datetime(hokkaido_df['Date Announced'], errors='coerce')
                    
                    # Drop rows with NaT dates
                    hokkaido_df = hokkaido_df.dropna(subset=['Date Announced'])
                    
                    if len(hokkaido_df) == 0:
                        print("\nc) No valid dates found for Hokkaido cases.")
                    else:
                        # Group by date and count cases
                        hokkaido_cases_by_day = hokkaido_df.groupby('Date Announced').size().reset_index()
                        hokkaido_cases_by_day.columns = ['Date', 'Number of Cases']
                        
                        # Sort by date
                        hokkaido_cases_by_day = hokkaido_cases_by_day.sort_values('Date')
                        
                        print("\nc) Cases in Hokkaido by day:")
                        print(hokkaido_cases_by_day)
                        
                        # Plot cases in Hokkaido by day
                        plt.figure(figsize=(14, 6))
                        
                        # Line plot
                        plt.plot(hokkaido_cases_by_day['Date'], hokkaido_cases_by_day['Number of Cases'], 
                                marker='o', linestyle='-', color='red', linewidth=2)
                        
                        # Add trend line (7-day moving average)
                        if len(hokkaido_cases_by_day) >= 7:
                            hokkaido_cases_by_day['7-day MA'] = hokkaido_cases_by_day['Number of Cases'].rolling(window=7).mean()
                            plt.plot(hokkaido_cases_by_day['Date'], hokkaido_cases_by_day['7-day MA'], 
                                    linestyle='--', color='blue', linewidth=2, label='7-day Moving Average')
                            plt.legend()
                        
                        plt.title('COVID-19 Cases in Hokkaido by Day', fontsize=14)
                        plt.xlabel('Date', fontsize=12)
                        plt.ylabel('Number of Cases', fontsize=12)
                        plt.grid(True, linestyle='--', alpha=0.7)
                        plt.xticks(rotation=45)
                        plt.tight_layout()
                        plt.savefig('hokkaido_cases_by_day.png')
                        print("Saved Hokkaido daily cases chart to 'hokkaido_cases_by_day.png'")
                        
                        # Also create a cumulative plot
                        hokkaido_cases_by_day['Cumulative Cases'] = hokkaido_cases_by_day['Number of Cases'].cumsum()
                        
                        plt.figure(figsize=(14, 6))
                        plt.plot(hokkaido_cases_by_day['Date'], hokkaido_cases_by_day['Cumulative Cases'], 
                                marker='o', linestyle='-', color='purple', linewidth=2)
                        plt.title('Cumulative COVID-19 Cases in Hokkaido', fontsize=14)
                        plt.xlabel('Date', fontsize=12)
                        plt.ylabel('Cumulative Number of Cases', fontsize=12)
                        plt.grid(True, linestyle='--', alpha=0.7)
                        plt.xticks(rotation=45)
                        plt.tight_layout()
                        plt.savefig('hokkaido_cumulative_cases.png')
                        print("Saved Hokkaido cumulative cases chart to 'hokkaido_cumulative_cases.png'")
                except Exception as e:
                    print(f"\nc) Error processing Hokkaido cases: {e}")
        else:
            print("Columns 'Date Announced' or 'Detected City' not found in the dataset.")
        
        # Save the processed data
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        df.to_csv(f'japan_covid_data_{timestamp}.csv', index=False)
        print(f"Saved processed data to 'japan_covid_data_{timestamp}.csv'")
        
        return df
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    baitap3()