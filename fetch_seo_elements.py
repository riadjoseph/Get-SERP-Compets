import requests
import csv
from bs4 import BeautifulSoup

def fetch_seo_elements(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"An error occurred while fetching the URL {url}: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.title.string if soup.title else "No title"
    
    h1_tag = soup.find('h1')
    h1 = h1_tag.string if h1_tag else "No H1"
    
    meta_description_tag = soup.find('meta', {'name': 'description'})
    meta_description = meta_description_tag['content'] if meta_description_tag else "No meta description"
    
    return {'url': url, 'title': title, 'h1': h1, 'meta_description': meta_description}

# Read URLs from urls.txt file
with open('urls.txt', 'r') as f:
    urls = [line.strip() for line in f.readlines()]

# Initialize CSV file
with open('seo_elements.csv', 'w', newline='') as csvfile:
    fieldnames = ['url', 'title', 'h1', 'meta_description']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Fetch and write SEO elements to CSV
    for url in urls:
        elements = fetch_seo_elements(url)
        if elements:
            writer.writerow(elements)
