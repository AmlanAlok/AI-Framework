#!/usr/bin/python3
# Date: 29-June-2024
# PROJECT: QaiTS Bot/Crawler
# VERSION: 1.0.0
# AUTHOR: JERISH BALAKRISHNAN, AMLAN ALOK

# Disable pylint errors/warnings
# pylint: disable=C0301

# Import all modules
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse, urldefrag
import time
from tqdm import tqdm
from rich.progress import Progress, BarColumn, TextColumn
import pyfiglet
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import argparse

class_template = """
public class {file_name} {{
    public {file_name}() {{
        // Constructor
    }}

    public void exampleMethod() {{
        // Example method
        System.out.println("Hello from {file_name}");
    }}

    public static void main(String[] args) {{
        {file_name} instance = new {file_name}();
        instance.exampleMethod();
    }}
}}
"""


class Node:
    """
    Node class to represent each URL and its children
    """

    def __init__(self, url):
        self.url = url
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def __repr__(self):
        return f"Node(url={self.url}, children={len(self.children)})"


class WebCrawler:
    """
    WebCrawler Class
    """

    def __init__(self, base_url, login_url=None, username=None, password=None):
        """
        Constructor
        """
        self.base_url = self.normalize_url(base_url)
        self.login_url = login_url
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.visited_urls = set()
        self.urls_to_visit = [self.base_url]
        self.internal_urls = set()
        self.file_extensions_to_ignore = {
            ".pdf",
            ".zip",
            ".exe",
            ".deb",
            ".app",
            ".apk",
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".bmp",
            ".mp3",
            ".mp4",
            ".avi",
            ".mov",
            ".wmv",
            ".mkv",
        }
        self.url_to_node = {self.base_url: Node(self.base_url)}

        if self.login_url and self.username and self.password:
            self.login()

    def normalize_url(self, url):
        """
        Normalize the URL's to treats URL's with different schemes,
        www prefixes, and fragments as equivalent
        """
        parsed_url = urlparse(url)
        scheme = parsed_url.scheme
        netloc = parsed_url.netloc.lstrip("www.")
        path = parsed_url.path
        normalized_url = urlunparse((scheme, netloc, path, "", "", ""))
        return normalized_url

    def is_internal_url(self, url):
        """
        Check if the URL belongs to the same domain
        """
        base_netloc = urlparse(self.base_url).netloc
        return urlparse(url).netloc.rstrip(".").endswith(base_netloc)

    def is_file_url(self, url):
        """
        Check if the URL is to download a file & ignore it
        """
        return any(url.lower().endswith(ext) for ext in self.file_extensions_to_ignore)

    def login(self):
        """
        Login to the website to handle authenticated pages using Selenium
        """
        # Setup Selenium WebDriver
        # options = webdriver.ChromeOptions()
        options = webdriver.ChromeOptions()
        # Run in headless mode
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

        try:
            # Open the login page
            driver.get(self.login_url)
            # Find the username and password fields and enter the credentials
            driver.find_element(By.ID, "email").send_keys(self.username)
            driver.find_element(By.ID, "password").send_keys(self.password)
            # Submit the login form
            driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
            # Wait for the login to complete and redirect
            time.sleep(5)
            # Get cookies from the Selenium session
            cookies = driver.get_cookies()
            for cookie in cookies:
                self.session.cookies.set(cookie["name"], cookie["value"])
            print("Logged in successfully")
        except Exception as e:
            print(f"Failed to log in: {e}")
        finally:
            driver.quit()

    def crawl(self):
        with Progress(
                TextColumn("[bold green]{task.description}"),
                BarColumn(bar_width=None),
                TextColumn("[progress.percentage]{task.percentage:>3.1f}%"),
                TextColumn("[green]{task.completed}/{task.total} URLs Crawled"),
                transient=True,
        ) as progress:
            task = progress.add_task("Crawling URLs", total=len(self.urls_to_visit))
            while self.urls_to_visit:
                # print(len(self.urls_to_visit))
                current_url = self.urls_to_visit.pop(0)
                if current_url not in self.visited_urls:
                    progress.update(task, description=f"Crawling: {current_url}")
                    self.visit_url(current_url)
                    progress.update(
                        task,
                        advance=1,
                        total=len(self.visited_urls) + len(self.urls_to_visit),
                    )
                    # time.sleep(1)

    def visit_url(self, url):
        try:
            # response = requests.get(url)
            response = self.session.get(url)
            if response.status_code == 200:
                self.visited_urls.add(url)
                soup = BeautifulSoup(response.text, "html.parser")
                all_links = soup.find_all("a", href=True)
                parent_node = self.url_to_node[url]

                for link in all_links:
                    absolute_url = urljoin(url, link["href"])
                    normalized_url = self.normalize_url(urldefrag(absolute_url)[0])
                    if (
                            self.is_internal_url(normalized_url)
                            and normalized_url not in self.visited_urls
                            and not self.is_file_url(normalized_url)
                    ):
                        self.urls_to_visit.append(normalized_url)
                        self.internal_urls.add(normalized_url)
                        if normalized_url not in self.url_to_node:
                            child_node = Node(normalized_url)
                            self.url_to_node[normalized_url] = child_node
                            parent_node.add_child(child_node)
        except requests.RequestException as e:
            print(f"Failed to fetch {url}: {e}")

    def get_internal_urls(self):
        """
        Return all the internal URL's
        """
        return self.internal_urls

    def print_hierarchy(self):
        """
        Print the hierarchy of the URLs
        """

        def print_node(node, indent=0):
            print(" " * indent + node.url)
            for child in node.children:
                print_node(child, indent + 4)

        root_node = self.url_to_node[self.base_url]
        print_node(root_node)

    def clean_url(self, url):
        pass

    # Function to extract the last word from the URL
    def get_last_word(self, url):
        return url.rstrip('/').split('/')[-1]

    def get_file_names(self):

        file_names = []

        def print_node(node):
            last_word = self.get_last_word(node.url)
            file_names.append(last_word)

            for child in node.children:
                print_node(child)

        root_node = self.url_to_node[self.base_url]
        print_node(root_node)
        return file_names

    def create_java_class_files(self, file_names, output_directory):

        # Directory to save the Java class files
        # output_directory = "default_folder_name"

        # Ensure the output directory exists
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Create a Java class file for each file name
        for file_name in file_names:
            # print(file_name)
            class_content = class_template.format(file_name=file_name)
            file_path = os.path.join(output_directory, f'{file_name}.java')
            with open(file_path, "w") as java_file:
                java_file.write(class_content)

        print(f"Java class files created in the '{output_directory}' directory.")

    def generate_java_files(self, output_directory="default_output_directory"):
        file_names = self.get_file_names()
        self.create_java_class_files(file_names, output_directory)
        pass


def main():
    parser = argparse.ArgumentParser(description="Command line interface for QaiTS")

    # Flag for controlling the crawler to get the sitemap
    parser.add_argument("--get-sitemap", action="store_true", help="Control the crawler to get the sitemap")

    # Flag for controlling generating Java class files
    parser.add_argument("--generate-java", action="store_true", help="Control generating Java class files")

    # Flag for finding new pages generated from the last execution
    parser.add_argument("--find-new-pages", action="store_true",
                        help="Find new pages generated from the last execution")

    # Flag for storing execution details
    parser.add_argument("--store-details", action="store_true",
                        help="Store details of the crawler execution like sitemap and files generated in log or DB")

    # Flag for comparing current execution to previous execution
    parser.add_argument("--compare-executions", action="store_true",
                        help="Compare current execution details to the previous execution and show prompt if there are any differences")

    parser.add_argument("--domain-url", type=str, help="Domain you want to crawl")
    parser.add_argument("-login", action="store_true", help="Choose crawler with login capability")
    parser.add_argument("--login-url", type=str, help="Login URL")
    parser.add_argument("-u", "--username", type=str, help="Username for login")
    parser.add_argument("-p", "--password", type=str, help="Password for login")
    parser.add_argument("-f", "--output-directory", type=str, help="Directory name where java classes are created")

    args = parser.parse_args()

    if args.get_sitemap:
        print("Crawling to get the sitemap...")
        domain_to_crawl = args.domain_url

        if args.login:
            login_url = args.login_url
            username = args.username
            password = args.password
            crawler = WebCrawler(domain_to_crawl, login_url, username, password)
        else:
            crawler = WebCrawler(domain_to_crawl)

        crawler.crawl()

        internal_urls = crawler.get_internal_urls()
        print(f"Found {len(internal_urls)} internal URLs:")
        # for url in internal_urls:
        #     print(url)

        print("\nHierarchy of the web pages:")
        crawler.print_hierarchy()

        # print("-----Printing Dictionary----")
        # print(crawler.url_to_node)
        if args.generate_java:
            print("Generating Java class files...")
            # Add logic to generate Java class files here
            if args.output_directory:
                crawler.generate_java_files(args.output_directory)
            else:
                crawler.generate_java_files()

'''
# Future scope of work

    if args.find_new_pages:
        print("Finding new pages generated from the last execution...")
        # Add logic to find new pages here

    if args.store_details:
        print("Storing execution details...")
        # Add logic to store execution details in log or DB here

    if args.compare_executions:
        print("Comparing current execution details to previous execution...")
        # Add logic to compare current execution details to previous execution here
'''

if __name__ == "__main__":
    # Generate and print ASCII art
    ascii_art = pyfiglet.figlet_format("QaiTS")
    print(ascii_art)

    # Print the version number below the ASCII art
    version = "Version 1.0.0"
    ascii_art_lines = ascii_art.split("\n")
    max_line_length = max(len(line) for line in ascii_art_lines)
    version_padding = " " * ((max_line_length - len(version)) // 2)
    print(f"{version_padding}{version}\n")

    main()

'''
python3 ./qualibar_crawler.py --get-sitemap --domain-url https://qaits.qualibar.com -login --login-url https://qaits.qualibar.com/login -u test@yopmail.com -p test --generate-java --output-directory QaitsQualibar
python3 ./qualibar_crawler.py --get-sitemap --domain-url https://848mitchell.com --generate-java --output-directory Housing
python3 ./qualibar_crawler.py --get-sitemap --domain-url https://qualibar.com --generate-java --output-directory Qualibar
python3 ./qualibar_crawler.py --get-sitemap --domain-url https://letshavana.com --generate-java --output-directory Havana
'''
