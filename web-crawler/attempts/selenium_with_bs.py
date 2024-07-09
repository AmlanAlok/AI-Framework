from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Set up the Selenium WebDriver (e.g., Chrome)
driver_path = '/path/to/chromedriver'  # Replace with the actual path to your ChromeDriver
driver = webdriver.Chrome(executable_path=driver_path)

# Open the webpage
url = 'https://example.com'
driver.get(url)

# Wait for the page to load completely
time.sleep(5)  # Adjust the sleep time as needed for the page to fully load

# Get the page source (the fully rendered HTML)
html_content = driver.page_source

# Close the browser
driver.quit()

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the <app-root> element and its children
app_root = soup.find('app-root')
if app_root:
    children = app_root.find_all()
    for child in children:
        print(child)
else:
    print("No <app-root> element found")
