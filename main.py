import csv
import requests
from bs4 import BeautifulSoup
import cloudscraper as cs
import regex as re

scraper = cs.create_scraper()

data_rows = []


def scrape_real_estate_website(url, location):
    # Send a GET request to the URL
    current_page = 1
    csv_filename = f'{location}.csv'  # Move this line outside the loop

    while current_page != 3:
        current_page += 1

        if current_page != 1:
            modified = f'{url}{current_page}_p/'

            response = scraper.get(modified)
        else:
            response = scraper.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all <ul> elements on the page
            div_elements = soup.find('div', id='grid-search-results')
            li_elements = div_elements.find_all('article')

            # Check if there are no more articles on the current page
            if not li_elements:
                break

            # Extract and print the content from each <ul>
            for index, li_element in enumerate(li_elements, start=1):
                li_content = li_element.get_text(separator='\t')
                if li_element.find('a'):
                    href_value = li_element.find('a').get('href')
                print(f"Content of <li> {index}:\n{li_content}\n{href_value}\n {'=' * 30}")
                pattern = re.compile(r'\$\d{1,3}(?:,\d{3})*')
                price = pattern.findall(li_content)
                price = price[:1]
                data_rows.append({
                    'Index': index,
                    'Li Content': li_content,
                    'Href Value': href_value,
                    'Prices': ', '.join(price),  # Join multiple prices with a comma
                })

            # Open the CSV file in append mode ('a') outside the loop
            header = ['Index', 'Li Content', 'Href Value', 'Prices']
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.DictWriter(csvfile, fieldnames=header)
                # Write the header only if the file is empty
                if csvfile.tell() == 0:
                    csv_writer.writeheader()
                csv_writer.writerows(data_rows)

            print(f"Data appended to CSV file '{csv_filename}' successfully.")
        else:
            print(f"Failed to retrieve data. Status Code: {response.status_code}")
            return -1


url = ''
url_original = 'https://www.zillow.com/'
location = input('Enter zip code or location name : ')
if location.isdigit():
    url = url_original + location + '_rb/'
    print('if statement isdigit')
else:
    modified_location = location.replace(' ', '-').lower()
    url = url_original + modified_location + '/'

scrape_real_estate_website(url, location)
