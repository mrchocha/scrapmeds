from bs4 import BeautifulSoup
import requests
import os
import pandas as pd

'''
Solution by
Name :Rahul Chocha
Email: rahul.c@ahduni.edu.in
'''

# function for scrap netmeds.com based of category and no of pages


def scrap_netmeds(name, url, pages):
    # make pandas dataframe to store data of all the products
    scraped_data = pd.DataFrame([], columns=[
                                'product_name', 'drug_varient', 'product_photo_url', 'product_photo_url', 'final_price', 'original_price', 'offer', 'is_in_stock'])

    # repeat the process for all the pages
    for page in range(1, pages+1):

        # make new url relative to page no.
        url_with_page = url+"/page/"+str(page)

        # fetch data from the url in html form
        avalable_data = requests.get(url_with_page).text

        # parse data to beautifulsoup
        soup = BeautifulSoup(avalable_data, 'html.parser')

        # get all the html div that has product details
        all_product_divs = soup.find_all(
            "div", {"class": "all-product"})

        # get the lists of products
        for all_product_lists in all_product_divs:

            product_list = all_product_lists.find_all(
                "div", {"class": "cat-item"})

            # for each product repeat the following process
            for product in product_list:
                # print(product)

                # store all the relevent details of product
                product_name = product.find(
                    "span", {"class": "clsgetname"}).text
                drug_varient = product.find(
                    "span", {"class": "drug-varients"}).text
                product_photo_url = product.find(
                    "img", {"class": "product-image-photo"})['src']
                product_url = product.find(
                    "a", {"class": "category_name"})['href']
                final_price = product.find(
                    "span", {"id": "final_price"}).text
                original_price = product.find(
                    "strike", {"id": "price"})
                if (original_price != None):
                    original_price = original_price.text
                else:
                    original_price = "None"

                offer = product.find(
                    "span", {"class": "save-badge"})
                if (offer != None):
                    offer = offer.text
                else:
                    offer = "None"

                is_in_stock = product.find("button", {"class": "toCart"})
                if (is_in_stock != None):
                    is_in_stock = "True"
                else:
                    is_in_stock = "False"

                # store data in pandas dataframe
                scraped_data.loc[len(scraped_data.index)] = [
                    product_name,
                    drug_varient,
                    product_photo_url,
                    product_url,
                    final_price,
                    original_price,
                    offer,
                    is_in_stock]

        print("fetched page", page, "for", name)

    # store all the data o CSV file with relevent name
    scraped_data.to_csv(name+".csv", index=False)
    print("=============================================================")
    print("=         All the data is stored in "+name+".csv            =")
    print("=============================================================")


# fetch the categories from netmeds
def get_total_features():

    # url of netmeds
    url = "https://www.netmeds.com"

    # fetch the html data from website
    avalable_data = requests.get(url).text

    # parse data to beautifulsoup
    soup = BeautifulSoup(avalable_data, 'html.parser')

    # find all the categories
    nav__links = soup.find_all("a", {"class": "level-top"})
    nav__text__link = {}
    cnt = 1

    # store the name and link of each categories
    for link in nav__links:
        nav__text__link[cnt] = {
            'text': link.text,
            'url': url+link['href']
        }
        cnt += 1
    return (nav__text__link)


if(__name__ == "__main__"):
    os.system('clear')
    while True:
        print("==============================================================")
        print("=                          WELCOME                           =")
        print("=                            TO                              =")
        print("=                         SCRAPMEDS                          =")
        print("==============================================================")
        print("=                  Developed by Rahul Chocha                 =")
        print("==============================================================")
        nav_data = get_total_features()
        for data_id in nav_data.keys():
            print(data_id, nav_data[data_id]['text'])
        print("**write break to stop program")
        print("=============================================================")
        try:
            selected_id = (
                input("Please Select the area of the intrest..(i.e. 1) :"))
            if selected_id == 'break':
                print("bye....")
                break
            selected_id = int(selected_id)
            pages = int(input("Enter the no. of pages you want to scrap:"))

            try:
                print("You have selected: ", nav_data[selected_id]['text'])
                scrap_netmeds(nav_data[selected_id]['text'],
                              nav_data[selected_id]['url'], pages)
                print("=============================================================\n")
            except:
                print("Some thing went wrong !!")
        except:
            print("Please check the inputs..\n\n")
