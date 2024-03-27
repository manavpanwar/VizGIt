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

# Function to extract links from the parsed HTML
def extract_links(soup):
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            links.append(href)
    return links

# Function to save data to a CSV file, creating it if it doesn't exist
def save_to_csv(data, filename):
    # Check if the file exists, if not, create it
    if not os.path.isfile(filename):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Link']) # Write header
    # Append data to the file
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for item in data:
            writer.writerow([item])

# Function to clean a URL
def clean_url(url):
    url = url.strip()
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    return url

# Function to remove duplicates from a list
def remove_duplicates(data):
    return list(set(data))

# Function to clean fetched data
def clean_fetched_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader) # Skip the header
        data = [row[0] for row in reader]
    
    cleaned_data = [clean_url(url) for url in data]
    cleaned_data = remove_duplicates(cleaned_data)
    
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Cleaned Link']) # Write header
        for item in cleaned_data:
            writer.writerow([item])
    
    print(f"Cleaned data saved to {filename}")

# Main function to run the crawler and clean the data
def main():
    url = 'https://www.moneycontrol.com/financials/sunpharmaceuticalindustries/results/quarterly-results/SPI/19#SPI' # Replace with the URL you want to crawl
    soup = fetch_and_parse(url)
    if soup:
        links = extract_links(soup)
        save_to_csv(links, 'fetched.csv')
        print("Data saved to fetched.csv")
        clean_fetched_data('fetched.csv')
    else:
        print("Failed to fetch and parse the page.")

if __name__ == '__main__':
    main()
