import requests
from bs4 import BeautifulSoup

# website_link = 'https://qualibar.com/'
website_link = 'https://848mitchell.com'

# To store the hierarchy of URLs
site_structure = {}
rejected_urls = []

# Initialize the list of discovered URLs
# with the first page to visit
urls = [website_link]
all_urls = []

# Helper function to add URLs to the site structure
def add_to_structure(structure, url_path, new_url):
    if len(url_path) == 0:
        structure[new_url] = {}
    else:
        current_level = url_path.pop(0)
        if current_level not in structure:
            structure[current_level] = {}
        add_to_structure(structure[current_level], url_path, new_url)

# Until all pages have been visited
while len(urls) != 0:
    # Get the page to visit from the list
    current_url = urls.pop()
    print(f'Total URL count to be processed = {len(urls)}')

    # Crawling logic
    if website_link in current_url and current_url not in all_urls:
        response = requests.get(current_url)
        soup = BeautifulSoup(response.content, "html.parser")

        all_urls.append(current_url)

        # Track hierarchy
        url_path = current_url.replace(website_link, '').strip('/').split('/')
        add_to_structure(site_structure, url_path, current_url)

        link_elements = soup.select("a[href]")

        for link_element in link_elements:
            url = link_element['href']

            if url.startswith('/'):
                url = website_link + url
            elif not url.startswith('http'):
                url = website_link + '/' + url

            if url not in all_urls and url not in urls and url not in rejected_urls:
                urls.append(url)
    else:
        rejected_urls.append(current_url)

# Function to print the site structure
def print_structure(structure, indent=0):
    for key, value in structure.items():
        print(' ' * indent + key)
        if isinstance(value, dict):
            print_structure(value, indent + 4)

# Print the number of unique URLs found and the hierarchy
print(f'Total unique URLs found: {len(all_urls)}')
print_structure(site_structure)
