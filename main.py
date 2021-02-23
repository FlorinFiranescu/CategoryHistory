import requests
import time
import Database
from bs4 import BeautifulSoup
from datetime import datetime
#container class
class product:
    def __init__(self):
        self.title = ""
        self.category = ""
        self.base_price = 0.0
        self.reduced_price = 0.0
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
def getNextPage(pageSoups):
    nextPageLink = None
    for page in pageSoups:
        if 'aria-label' in page.attrs:
            if page['aria-label'] == "Next" and page.string == "Pagina urmatoare":
                nextPageLink = page['href']
    return nextPageLink


def main():
    listOfProducts = []
    emag_URL = "https://www.emag.ro"
    category_URL = "/televizoare/c"
    nextPageLink = category_URL
    #day for adding it into the db
    day = datetime.date(datetime.now())
    #open the database
    dbName = "Product"
    tableName = "TV"
    connection = Database.connectToDB(DBName=dbName)
    cursor = connection.cursor()
    if (Database.checkIfTableExists(cursor, dbName, tableName)):
        print("The table {} exists".format(tableName))
    else:
        print("The table {} does not exist. Attempting to create it.".format(tableName))
        try:
            Database.createTable(cursor, tableName)
        except:
            print("Error while trying to create a table called {} in the database called {}".format(tableName, dbName))
            exit()
    if (Database.checkDayInDB(cursor=cursor,table=tableName, day=day) != 0):
        print("For the day = {}, the database has been updated".format(day))
        connection.close()
        exit(0)

    while nextPageLink is not None:
        soup = request2BfSoupObj(emag_URL, nextPageLink)
        #Grid container <=> our grid containing all the products
        gridContainer = soup.find(id="card_grid")
        nextPages = soup.find_all(class_="js-change-page")
        #nextPageLink = nextPage['href']
        for product in gridContainer.find_all(class_='js-product-data'):
            myProduct = product()
            myProduct.title = product['data-name']
            myProduct.category = product['data-category-name']
            myProduct.link = product.find(class_="card-section-top").a['href']
            prices = product.find('div', class_="pricing-old_preserve-space")
            oldPrice = prices.find('p', class_='product-old-price')
            newPrice = prices.find('p', class_='product-new-price')
            try:
                if oldPrice.s is not None:
                    old_price = getProductPrice(oldPrice.s)
                    myProduct.base_price = float(old_price.replace(".","").replace(",","."))
                else:
                    old_price = getProductPrice(newPrice)
                    myProduct.base_price = float(old_price.replace(".", "").replace(",", "."))
                new_price = getProductPrice(newPrice)
                myProduct.reduced_price = float(new_price.replace(".", "").replace(",", "."))
            except:
                print("Error encountered while decoding the price for product {} with link {}".format(myProduct.title, myProduct.link))
                continue

            #insert the element in the DB
            try:
                Database.insertProduct(cursor=cursor,day=day, table=tableName, product=myProduct)
            except Exception as E:
                print("Error occured while inserting a product in the DB")
                print(E)

            #listOfProducts.append(myProduct)
            print(myProduct.title, myProduct.category, myProduct.link, myProduct.base_price, myProduct.reduced_price)
        nextPageLink = getNextPage(nextPages)
        connection.commit()
        time.sleep(5)

    connection.close()
    #print(soup)

main()