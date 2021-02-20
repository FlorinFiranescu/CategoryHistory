import requests
from bs4 import BeautifulSoup

#container class
class product:
    def __init__(self):
        self.title = ""
        self.category = ""
        self.old_price = ""
        self.new_price = ""
        self.link = ""

def getProductPrice(productSoup):
    #product soup is a list. On position 0, main price. On 1, <sup>price</sup>
    mainPrice = productSoup.contents[0]
    if productSoup.sup is not None:
        restPrice = productSoup.sup.string
    return "{},{}".format(mainPrice, restPrice)

def request2BfSoupObj(root_url, url_path):
    page = requests.get("{}{}".format(root_url,url_path))
    print("\nRequesting Page URL: {}{}\n".format(root_url,url_path))
    if page.status_code == 200: print("\nRequest OK: Status code {}\n".format(page.status_code))
    else:
        print("\nError with the request:response: {}\n".format(page.status_code))
        raise ConnectionError("\nError with the request:response: {}\n".format(page.status_code))
        return 0
    page.encoding = 'ISO-885901'
    soup = BeautifulSoup(page.text, 'html.parser')      #using the html parser, easier to search in browser
    return soup

def main():
    listOfProducts = []
    emag_URL = "https://www.emag.ro/"
    category_URL = "televizoare/rating,star-5/c"
    soup = request2BfSoupObj(emag_URL, category_URL)
    #Grid container <=> our grid containing all the products
    gridContainer = soup.find(id="card_grid")
    for product in gridContainer.find_all(class_='js-product-data'):
        myProduct = product()
        myProduct.title = product['data-name']
        myProduct.category = product['data-category-name']
        myProduct.link = product.find(class_="card-section-top").a['href']
        prices = product.find('div', class_="pricing-old_preserve-space")
        oldPrice = prices.find('p', class_='product-old-price')
        newPrice = prices.find('p', class_='product-new-price')
        print(myProduct.title)
        if oldPrice.s is not None:
            myProduct.old_price = getProductPrice(oldPrice.s)
        else:
            myProduct.old_price = getProductPrice(newPrice)
        myProduct.new_price = getProductPrice(newPrice)
        print(myProduct.old_price)
        print(myProduct.new_price)

    #print(soup)

main()