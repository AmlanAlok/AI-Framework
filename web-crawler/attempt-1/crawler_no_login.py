# https://www.zenrows.com/blog/web-crawler-python#what-is-a-web-crawler-in-python

import requests
from bs4 import BeautifulSoup

website_link = 'https://qualibar.com/'

all_urls = []
rejected_urls = []

# initialize the list of discovered urls
# with the first page to visit
urls = [website_link]

# until all pages have been visited
while len(urls) != 0:
    # get the page to visit from the list
    current_url = urls.pop()
    print(f'total url count to be processed = {len(urls)}')

    # crawling logic
    if website_link in current_url and current_url not in all_urls:
        response = requests.get(current_url)
        soup = BeautifulSoup(response.content, "html.parser")

        all_urls.append(current_url)

        link_elements = soup.select("a[href]")

        for link_element in link_elements:
            url = link_element['href']

            '''To identify '''
            if url[-5:] == '.html':
                url = website_link + url
            if url not in all_urls and url not in urls and url not in rejected_urls:
                urls.append(url)
    else:
        rejected_urls.append(current_url)


print(len(all_urls))
# print(all_urls)
for url in all_urls:
    print(url)

# print(len(rejected_urls))
# for url in rejected_urls:
#     print(url)
