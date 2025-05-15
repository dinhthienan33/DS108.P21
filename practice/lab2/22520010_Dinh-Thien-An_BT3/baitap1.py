import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt 
import time

def baitap1():
    print("Fetching COVID-19 data from Worldometers...")
    
    # Get data from website
    url = "https://www.worldometers.info/coronavirus/#countries"
    
    # Add a user-agent header to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Note: As of April 13, 2024, Worldometers stopped updating COVID data
        # but historical data remains accessible
        print("Note: Worldometers stopped updating COVID data as of April 13, 2024, but historical data is available.")
        
        # Find the main table
        table = soup.find('table', id='main_table_countries_today')
        
        if not table:
            print("Could not find the COVID-19 data table. The website structure may have changed.")
            return None
        
        # Extract headers
        headers = []
        thead = table.find('thead')
        if thead:
            for th in thead.find_all('th'):
                headers.append(th.text.strip())
        
        if not headers:
            print("Could not extract table headers.")
            return None
        
        # Extract data rows
        rows = []
        tbody = table.find('tbody')
        if tbody:
            for tr in tbody.find_all('tr'):
                row = []
                for td in tr.find_all('td'):
                    row.append(td.text.strip())
                if len(row) == len(headers):
                    rows.append(row)
        
        if not rows:
            print("Could not extract data rows.")
            return None
        
        # Create DataFrame
        df = pd.DataFrame(rows, columns=headers)
        
        # Identify and clean numeric columns
        # Column names may have changed, so we'll check for expected columns
        expected_columns = [
            'Total Cases', 'TotalCases', 
            'New Cases', 'NewCases', 
            'Total Deaths', 'TotalDeaths', 
            'New Deaths', 'NewDeaths', 
            'Total Recovered', 'TotalRecovered', 
            'New Recovered', 'NewRecovered', 
            'Active Cases', 'ActiveCases', 
            'Serious, Critical', 'Serious,Critical'
        ]
        
        # Create a mapping of actual columns to expected columns
        column_mapping = {}
        for exp_col in expected_columns:
            for col in df.columns:
                if exp_col.lower().replace(' ', '').replace(',', '') == col.lower().replace(' ', '').replace(',', ''):
                    column_mapping[exp_col] = col
        
        # List of columns to process as numeric
        numeric_columns = []
        for col in df.columns:
            # Check if column name contains specific keywords indicating numeric data
            if any(keyword in col.lower() for keyword in ['cases', 'deaths', 'recovered', 'critical']):
                numeric_columns.append(col)
        
        # Clean data - convert numeric columns
        for col in numeric_columns:
            if col in df.columns:
                # Replace non-numeric characters and convert to numeric
                df[col] = df[col].str.replace(',', '').str.replace('+', '').str.replace(' ', '').str.replace('N/A', '')
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Fill NaN values with 0 for calculations
        df.fillna(0, inplace=True)
        
        # Identify country column
        country_col = next((col for col in df.columns if 'country' in col.lower() or 'other' in col.lower()), None)
        if not country_col:
            country_col = df.columns[1]  # Usually the second column is the country name
            
        # Identify case columns
        total_cases_col = next((col for col in df.columns if 'total' in col.lower() and 'case' in col.lower() and 'active' not in col.lower()), None)
        new_cases_col = next((col for col in df.columns if 'new' in col.lower() and 'case' in col.lower()), None)
        total_recovered_col = next((col for col in df.columns if 'recover' in col.lower() or ('total' in col.lower() and 'recov' in col.lower())), None)
        
        if not total_cases_col or not new_cases_col or not total_recovered_col:
            print("Warning: Some required columns were not found. Using fallback column names.")
            # Fallback to column positions (risky but might work)
            if not total_cases_col and len(df.columns) > 2:
                total_cases_col = df.columns[2]  # Usually the third column is total cases
            if not new_cases_col and len(df.columns) > 3:
                new_cases_col = df.columns[3]  # Usually the fourth column is new cases
            if not total_recovered_col and len(df.columns) > 5:
                total_recovered_col = df.columns[6]  # Usually the seventh column is total recovered
        
        print(f"Using columns: Country={country_col}, Total Cases={total_cases_col}, New Cases={new_cases_col}, Total Recovered={total_recovered_col}")
        
        # a) Tìm 5 quốc gia có số ca nhiễm (Total case) nhiều nhất.
        if total_cases_col:
            top_cases = df.sort_values(total_cases_col, ascending=False).head(5)
            print("\na) Top 5 quốc gia có số ca nhiễm (Total case) nhiều nhất:")
            print(top_cases[[country_col, total_cases_col]])
            
            # Plot top 5 countries by total cases
            plt.figure(figsize=(12, 6))
            plt.bar(top_cases[country_col], top_cases[total_cases_col])
            plt.title('Top 5 quốc gia có số ca nhiễm (Total case) nhiều nhất')
            plt.ylabel('Total Cases')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('top5_covid_cases.png')
        else:
            print("Could not find total cases column.")
        
        # b) Quốc gia nào có số ca nhiễm mới cao nhất?
        if new_cases_col:
            top_new_cases = df.sort_values(new_cases_col, ascending=False).head(1)
            print("\n b) Quốc gia có số ca nhiễm mới cao nhất là:")
            print(top_new_cases[[country_col, new_cases_col]])
        else:
            print("Không tìm tháy cột tương ứng.")
        
        # c) Tính tỉ lệ tổng số ca bình phục trên tổng số ca nhiễm. Xác định 3 quốc gia có tỉ lệ bình phục cao nhất.
        if total_cases_col and total_recovered_col:
            # Lọc các quốc gia có ít nhất 1000 ca nhiễm và có số ca hồi phục dương để đảm bảo ý nghĩa thống kê
            significant_countries = df[(df[total_cases_col] >= 1000) & (df[total_recovered_col] > 0)].copy()
            significant_countries['Recovery Rate'] = (significant_countries[total_recovered_col] / significant_countries[total_cases_col] * 100).round(2)
            top_recovery = significant_countries.sort_values('Recovery Rate', ascending=False).head(3)
            
            print("\nc) Top 3 countries with highest recovery rates (among countries with 1000+ cases):")
            print(top_recovery[[country_col, total_cases_col, total_recovered_col, 'Recovery Rate']])
            print(f"Average recovery rate worldwide: {(df[total_recovered_col].sum() / df[total_cases_col].sum() * 100).round(2)}%")
            
            # Vẽ biểu đồ cho top 3 quốc gia có tỉ lệ bình phục cao nhất
            plt.figure(figsize=(12, 6))
            plt.bar(top_recovery[country_col], top_recovery['Recovery Rate'])
            plt.title('Top 3 Countries by COVID-19 Recovery Rate')
            plt.ylabel('Recovery Rate (%)')
            plt.xticks(rotation=45)
            plt.grid(axis='y')
            plt.tight_layout()
            plt.savefig('top3_recovery_rates.png')
        else:
            print("Could not find total cases or total recovered columns.")
        
        # Optional: Save data to CSV with timestamp
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        df.to_csv(f'worldometer_covid_data_{timestamp}.csv', index=False)
        
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Error processing data: {e}")
        return None

if __name__ == "__main__":
    baitap1()