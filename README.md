# Web Scraper for Amazon

This script scrapes the Amazon website to get the top 5 search results for a product
and then extracts the product details like name, price, rating, review count, and specifications for a selected product.

## What is a Web Scraper?<br>
A web scraper automates the extraction of data from websites by retrieving and parsing HTML material before storing it in a structured format. Its applications include market research, Competitive Analysis, SEO Monitoring, and more.

## How have I implemented it?<br>
This Python script functions as a Web Scraper designed specifically for Amazon.  The scraper begins by prompting the user to input a product name, which it uses to construct a search query on Amazon. It then sends a request to Amazon's search results page, extracts information about the top 5 products and displays these results to the user.<br>

Once the user selects a product of interest from the displayed list, the script accesses the specific URL of the chosen product. It then fetches additional details. These details are formatted and printed for the user's readability of the information presented.

                                                                  
## Installation

Make a clone of all the files in the repository.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install following:

```bash
pip3 install requests
pip3 install beautifulsoup4
```
Make sure you are using the correct version of Python (ideally Python 3).<br>
Run the webscraping_amazon.py file

## Output

After successfully running the code, in the terminal, there should be a prompt asking what you want to search in Amazon.<br>
After that, it will show the top 5 products in the Amazon search. If the request is not found it will display an error message accordingly.<br>
Then you can select the desired product with numbers from 1 to 5 to get more details about the product.<br>

Demo video: 

## Not functioning?
If you run into difficulties or errors in the code please feel free to reach out.<br>
Email: contact@shahmeer.xyz
