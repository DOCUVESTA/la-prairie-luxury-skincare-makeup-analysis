# import libraries
import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict
import csv


# create a dataclass to store data
@dataclass
class Product:
    product_line: str
    product_name: str
    benefits: str
    price: str


# get information from each country of origin (us, gb, hk)
def get_data(country):
    url = f"https://www.laprairie.com/en-{country}/skincare"
    response = httpx.get(url)
    return HTMLParser(response.text)


# parsing the data from website and storing it into a dict
def parse_products(html):
    products = html.css("div.product-tile.js-product-tile-container")

    results = []
    for product in products:
        new_product = Product(
            product_line = product.css_first("div.category-name-link.product-tile__category-name").text().replace('\n','') if product.css_first("div.category-name-link.product-tile__category-name") else "LA PRAIRIE" ,    
            product_name = product.css_first("div.name-link.product-tile__name").text().replace('\n',''),
            benefits = product.css_first("ul.product-benefits-tags.js-product-benefits-tags").text().replace('\n',',').strip(','),
            price = product.css_first("span.js-sales-price.js-calculate-total-price.js-product-price").text().replace('\n','') if product.css_first("span.js-sales-price.js-calculate-total-price.js-product-price") else ""        )
        results.append(asdict(new_product))
    return results


# saving data in a csv file
def csv_data(final_data):
    with open("laprairie_data_0.csv", "a") as f:
        writer = csv.DictWriter(f, fieldnames=["product_line", "product_name", "benefits", "price"])
        writer.writerows(final_data)

# main function
def main():
    countries = ['us', 'gb', 'hk']
    for country in countries:
        print(f"Scrapping data for {country}")
        html = get_data(country)
        final_data = parse_products(html)
        csv_data(final_data)

# calling the main function
if __name__ == '__main__':
    main()

