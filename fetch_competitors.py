import csv
import requests
import json

# Your Google Custom Search API Key
api_key = "AIzaSyAvWCfFiTwjVMR9BRi2uGQYxew0nyn0Sgo"

# Your Custom Search Engine ID
cx = "06f500a591d3b47aa"

# Function to fetch top 5 competitors using Google Search API
def fetch_competitors(keywords):
    search_url = "https://www.googleapis.com/customsearch/v1"
    
    params = {
        "key": api_key,
        "cx": cx,
        "q": keywords,
        "num": 5  # Number of results to fetch (Top 5 competitors)
    }
    
    response = requests.get(search_url, params=params)
    
    if response.status_code == 200:
        search_results = json.loads(response.text)
        competitors = [result["link"] for result in search_results.get("items", [])]
        return competitors
    else:
        print(f"Failed to fetch competitors for keywords '{keywords}': {response.text}")
        return []

# Read URLs and keywords from gsc_data.csv
url_keyword_map = {}
with open('gsc_data.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    next(reader)  # Skip header
    for row in reader:
        if len(row) == 2:  # Check that each row has exactly two values
            url, keywords = row
            url_keyword_map[url] = keywords.split('; ')
        else:
            print(f"Skipping row: {row}")

# Write results to a new CSV file (competitors.csv)
with open('competitors.csv', 'w', newline='') as csvfile:
    fieldnames = ['url', 'keywords', 'competitors']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()

    for url, keywords in url_keyword_map.items():
        competitors = fetch_competitors(keywords)
        writer.writerow({'url': url, 'keywords': '; '.join(keywords), 'competitors': '; '.join(competitors)})
