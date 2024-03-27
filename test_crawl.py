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

# Function to extract "Total Income From Operations" data from the parsed HTML
def extract_total_income_from_operations(soup):
    income_data = []
    for table in soup.find_all('table'):
        # Check if the table contains the heading "Income"
        if any('Income' in th.get_text(strip=True) for th in table.find_all('th')):
            for row in table.find_all('tr')[1:]: # Skip the header row
                row_data = [td.get_text(strip=True) for td in row.find_all('td')]
                # Check if the row contains "Total Income From Operations"
                if "Total Income From Operations" in row_data:
                    income_data.append(row_data)
                    break # Stop after finding the first occurrence
    return income_data

# Function to save data to a CSV file, creating it if it doesn't exist
def save_to_csv(data, filename):
    # Check if the file exists, if not, create it
    if not os.path.isfile(filename):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write the header row from the first table
            if data and data[0]:
                writer.writerow(data[0]) # Write header
    # Append data to the file
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in data[1:]: # Skip the header row if it's already written
            writer.writerow(row)

# Main function to run the crawler
def main():
    url = 'https://www.moneycontrol.com/financials/sunpharmaceuticalindustries/results/consolidated-quarterly-results/SPI#SPI' # Replace with the URL you want to crawl
    soup = fetch_and_parse(url)
    if soup:
        income_data = extract_total_income_from_operations(soup)
        if income_data:
            save_to_csv(income_data, 'total_income_from_operations.csv')
            print("Total Income From Operations data saved to total_income_from_operations.csv")
        else:
            print("No Total Income From Operations data found.")
    else:
        print("Failed to fetch and parse the page.")

if __name__ == '__main__':
    main()
