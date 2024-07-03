import requests
import textwrap
from bs4 import BeautifulSoup

# Constants
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'https://www.amazon.com/',
    'Connection': 'keep-alive'
}
BASE_URL = "https://www.amazon.com"

def dic_print(dictionary):
    for key, value in dictionary.items():
        print(f'{key}: {value}')

def get_soup(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_product_info(soup):
    title = soup.find('span', {'id': "productTitle"})
    price = soup.find("span", {"class": "a-offscreen"})
    rating = soup.select_one('#acrPopover .a-color-base')
    
    specifications = {}
    for element in soup.find_all("tr", class_="a-spacing-small"):
        key_element = element.select_one("span.a-text-bold")
        value_element = element.select_one(".po-break-word")
        if key_element and value_element:
            key = key_element.text.strip()
            value = value_element.text.strip()
            specifications[key] = value

    return {
        'title': title.text.strip() if title else 'Title not available.',
        'price': price.text.strip() if price else 'Price not available',
        'rating': rating.text.strip() if rating else 'Rating not available',
        'specifications': specifications
    }

def search_product(url):
    soup = get_soup(url)
    if not soup:
        return

    product_info = extract_product_info(soup)
    print_divider("PRODUCT")
    print(product_info['title'])
    pretty_print("SPECIFICATIONS", product_info['specifications'])
    pretty_print("PRICE", product_info['price'])
    pretty_print("RATING", product_info['rating'])

def search_amazon(product_name):
    url = f"{BASE_URL}/s?k={product_name.replace(' ', '+')}"
    soup = get_soup(url)
    if not soup:
        return []

    products = soup.find_all('div', {'data-component-type': 's-search-result'}, limit=5)
    results = []
    for product in products:
        name = product.find('span', {'class': 'a-text-normal'}).text.strip()
        price = product.find('span', {'class': 'a-offscreen'})
        price = price.text.strip() if price else 'Price not available'
        rating = product.find('span', {'class': 'a-icon-alt'})
        rating = rating.text.split()[0] if rating else 'Rating not available'
        review_count = product.find('span', {'class': 's-underline-text'})
        review_count = review_count.text.strip() if review_count else 'Review count not available'
        url = BASE_URL + product.find('a', {'class': 'a-link-normal'})['href']
        
        results.append({
            'Product Name': name,
            'Product Price': price,
            'Product Rating': rating,
            'Product Review Count': review_count,
            'Product URL': url
        })
    return results

def print_divider(title, underline_char="="):
    print(f"\n{title}")
    print(underline_char * len(title))

def pretty_print(title, content):
    print_divider(title)
    if isinstance(content, dict):
        max_key_length = max(len(key) for key in content.keys())
        for key, value in content.items():
            print(f"{key.ljust(max_key_length)} : {value}")
    else:
        print(content)

def print_search_results(results):
    print(f"\nTop 5 search results:\n")
    labels = ["Price:", "Rating:", "Review Count:"]
    max_label_length = max(len(label) for label in labels)
    max_product_name_length = 70

    for idx, result in enumerate(results, start=1):
        product_name = result['Product Name']
        wrapped_product_name = textwrap.fill(product_name, max_product_name_length, subsequent_indent='   ')
        print(f"{idx}. {wrapped_product_name}")
        print(f"   {'Price:'.ljust(max_label_length)} {result['Product Price']}")
        print(f"   {'Rating:'.ljust(max_label_length)} {result['Product Rating']}")
        print(f"   {'Review Count:'.ljust(max_label_length)} {result['Product Review Count']}")
        print()

def main():
    while True:
        search_query = input("Enter the product name to search on Amazon: ")
        search_results = search_amazon(search_query)
        if search_results:
            print_search_results(search_results)
            while True:
                try:
                    selection = int(input("Enter the number (1-5) of the product to get more details: "))
                    if 1 <= selection <= 5:
                        product_url = search_results[selection - 1]['Product URL']
                        search_product(product_url)
                        break
                    else:
                        print("Invalid selection. Please enter a number between 1 and 5.\n")
                except ValueError:
                    print("Invalid input. Please enter a number.\n")
            break
        else:
            print("No results found. Please try again.\n")

if __name__ == "__main__":
    main()
