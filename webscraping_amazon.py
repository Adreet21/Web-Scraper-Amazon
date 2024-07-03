'''
Description: This script scrapes the Amazon website to get the top 5 search results for a product
and then extracts the product details like name, price, rating, review count, and specifications for a selected product.
'''

# Importing the required libraries
import requests
import textwrap
from bs4 import BeautifulSoup

# For printing dictionaries in a formatted way
def dic_print(dict):
    for key, value in dict.items():
        print(f'{key}: {value}')

# Function for a product information on Amazon
def search_product(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Config/94.2.7641.42",
        "Accept-Language": "en-US,en;q=0.9"
        }
 
    resp = requests.get(url, headers = headers)
    soup = BeautifulSoup(resp.text,'html.parser')

    # Extracting the product title
    title_element = soup.find('span', {'id':"productTitle"})
    if title_element:
        title = title_element.text.strip()
    else:
        title = 'Title not available.'
    
    # Extracting the product price
    pricing_element = soup.find("span",{"class":"a-offscreen"})
    if pricing_element:
        pricing = pricing_element.text.strip()
    else:
        pricing = 'Price not available'
    
    # Extracting the product rating
    rating_element = soup.select_one('#acrPopover .a-color-base')
    if rating_element:
        rating = rating_element.text.strip()
    else:
        rating = 'Rating not available'
    
    
    specifications = {}
    prodct_attrs = []
    prodct_values = []
    
    # Extracting the product specifications
    for element in soup.find_all("tr", class_="a-spacing-small"):
        prodct_attrs.append(element.select_one("span.a-text-bold").text.strip())
        prodct_values.append(element.select_one(".po-break-word").text.strip())
    
    specifications = dict(zip(prodct_attrs, prodct_values))

    # Function to print the product details
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

    # Printing the product details
    pretty_print("PRODUCT", title)
    pretty_print("SPECIFICATIONS", specifications)
    pretty_print("PRICE", pricing)
    pretty_print("RATING", rating,)
    

def search_amazon(product_name):
    url = f"https://www.amazon.com/s?k={product_name.replace(' ', '+')}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'https://www.amazon.com/',
        'Connection': 'keep-alive',
    }

    try:
        response = requests.get(url, headers=headers, timeout = 10)

        # Check if the request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            products = soup.find_all('div', {'data-component-type': 's-search-result'})

            results = []
            for idx, product in enumerate(products[:5], start=1):  # Limiting the top 5 results

                # Extract product name
                product_name = product.find('span', {'class': 'a-size-medium'}).text.strip()
                
                # Check if the product price is available
                price_tag = product.find('span', {'class': 'a-offscreen'})
                if price_tag:
                    product_price = price_tag.text.strip()
                else:
                    product_price = 'Price not available'
                
                # Extract rating
                rating_tag = product.find('span', {'class': 'a-icon-alt'})
                if rating_tag:
                    product_rating = rating_tag.text.split()[0]  # Extract the rating value
                else:
                    product_rating = 'Rating not available'
                
                # Extract review count
                review_count_tag = product.find('span', {'class': 's-underline-text'})
                if review_count_tag:
                    product_review_count = review_count_tag.text.strip()
                else:
                    product_review_count = 'Review count not available'

                # Extract product URL
                product_url = 'https://www.amazon.com' + product.find('a', {'class': 'a-link-normal'})['href']

                # Append the product details to the results list
                results.append({
                    'Product Name': product_name,
                    'Product Price': product_price,
                    'Product Rating': product_rating,
                    'Product Review Count': product_review_count,
                    'Product URL': product_url
                })
            return results
        
        # If the request was not successful, print the error code
        else:
            print(f"Failed to retrieve Amazon page: {response.status_code}")
            return None
        
    # Handle exceptions
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {str(e)}")
        return None

# Function to print the search results
def print_search_results(results):
    print(f"\nTop 5 search results:\n")

    # Labels for the product details
    labels = ["Price:", "Rating:", "Review Count:"]
    max_label_length = max(len(label) for label in labels)
    max_product_name_length = 70  # Maximum length for product names

    # Print the search results
    for idx, result in enumerate(results, start=1):
        product_name = result['Product Name']
        wrapped_product_name = textwrap.fill(product_name, max_product_name_length, subsequent_indent='   ')
        
        print(f"{idx}. {wrapped_product_name}")
        print(f"   {'Price:'.ljust(max_label_length)} {result['Product Price']}")
        print(f"   {'Rating:'.ljust(max_label_length)} {result['Product Rating']}/5")
        print(f"   {'Review Count:'.ljust(max_label_length)} {result['Product Review Count']}")
        print()

# Main function
if __name__ == "__main__":
    search_query = input("Enter the product name to search on Amazon: ")
    search_results = search_amazon(search_query)

    # If search results are found, print them
    if search_results:
        print_search_results(search_results)

        try:
            selection = int(input("Enter the number (1-5) of the product to get more details: "))
            if 1 <= selection <= 5:
                product_url = search_results[selection - 1]['Product URL']
                search_product(product_url)
            else:
                print("Invalid selection. Please enter a number between 1 and 5.\n")
        except ValueError:
            print("Invalid input. Please enter a number.\n")
    else:
        print("No results found.")