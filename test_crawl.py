import requests
from bs4 import BeautifulSoup
import csv
import os

# Function to fetch and parse a single page
def fetch_and_parse(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    else:
        print(f"Failed to fetch {url}")
        return None

# Function to extract table data and headings from the parsed HTML
def extract_table_data_and_headings(soup):
    tables = []
    for table in soup.find_all('table'):
        table_data = []
        # Extract headings from the first row
        headings = [th.get_text(strip=True) for th in table.find_all('th')]
        table_data.append(headings)
        # Extract data from the remaining rows
        for row in table.find_all('tr')[1:]: # Skip the first row (headings)
            row_data = [td.get_text(strip=True) for td in row.find_all('td')]
            table_data.append(row_data)
        tables.append(table_data)
    return tables

# Function to save data to a CSV file, creating it if it doesn't exist
def save_to_csv(data, filename):
    # Check if the file exists, if not, create it
    if not os.path.isfile(filename):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write the header row from the first table
            if data and data[0]:
                writer.writerow(data[0][0]) # Write header
    # Append data to the file
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for table in data:
            for row in table[1:]: # Skip the header row if it's already written
                writer.writerow(row)

# Main function to run the crawler
def main():
    url = 'https://www.moneycontrol.com/financials/sunpharmaceuticalindustries/results/quarterly-results/SPI/19#SPI' # Replace with the URL you want to crawl
    soup = fetch_and_parse(url)
    if soup:
        tables = extract_table_data_and_headings(soup)
        save_to_csv(tables, 'fetched_data.csv')
        print("Data saved to fetched_data.csv")
    else:
        print("Failed to fetch and parse the page.")

if __name__ == '__main__':
    main()
