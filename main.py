# webscraping
import requests
from lxml import html
import regex as re

# data processing and archiving
import pandas as pd
import itertools

# randomly pause before switching pages
import random
import time

urlMake = 'audi' # include a hyphen between words (mercedes-benz), lowercase only
urlModel = 'a4' # include a hyphen between words (mercedes-benz), lowercase only

url = 'https://www.carvana.com/cars/' + urlMake + '-' + urlModel
content = requests.get(url).content
tree = html.fromstring(content)

# determine number of pages
txt = tree.xpath('//*[@id="pagination"]/li[2]/span/text()')
match = re.search('(?<=of )\d*',txt[0]).group()
totalPages = int(match) - 1 
pageIndex = list(range(totalPages))
print('The program will iterate over ' + str(len(pageIndex)) + ' pages.')

# function for scraping the values
def getValues():
    index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
    for i in index:
        check = tree.xpath(  '/html/body/div[1]/main/section/section/div[' + str(i) + ']/a/div/div[2]/div[2]/div/text()[2]')
        if check != ['Carvana']:
            year.append(tree.xpath(   '/html/body/div[1]/main/section/section/div[' + str(i) + ']/a/div/div[2]/div[1]/div[2]/div/text()[1]')) 
            make.append(tree.xpath(   '/html/body/div[1]/main/section/section/div[' + str(i) + ']/a/div/div[2]/div[1]/div[2]/div/text()[3]')) 
            model.append(tree.xpath(  '/html/body/div[1]/main/section/section/div[' + str(i) + ']/a/div/div[2]/div[1]/div[2]/div/text()[5]')) 
            trim.append(tree.xpath(   '/html/body/div[1]/main/section/section/div[' + str(i) + ']/a/div/div[2]/div[1]/div[3]/span[1]/text()')) 
            mileage.append(tree.xpath('/html/body/div[1]/main/section/section/div[' + str(i) + ']/a/div/div[2]/div[1]/div[3]/span[2]/text()[1]'))
            price.append(tree.xpath(  '/html/body/div[1]/main/section/section/div[' + str(i) + ']/a/div/div[2]/div[2]/div/text()[2]')) 


count = 0
for page in pageIndex:
    # create lists to store values on per page
    year = []
    make = []
    model = []
    trim = []
    mileage = []
    price = []


    if page == 0:
        url = 'https://www.carvana.com/cars/' + urlMake + '-' + urlModel
        content = requests.get(url).content
        tree = html.fromstring(content)
    else:
        url = 'https://www.carvana.com/cars/' + urlMake + '-' +  urlModel + '?page=' + str(page+1)
        content = requests.get(url).content
        tree = html.fromstring(content)

    getValues()


    # "un-nest" the nested lists
    year = list(itertools.chain.from_iterable(year))
    make = list(itertools.chain.from_iterable(make))
    model = list(itertools.chain.from_iterable(model))
    trim = list(itertools.chain.from_iterable(trim))
    mileage = list(itertools.chain.from_iterable(mileage))
    price = list(itertools.chain.from_iterable(price))

    
    # adjust string to convert to float
    for i in range(len(price)):
        price[i] = price[i].replace(',','')
    for i in range(len(mileage)):
        mileage[i] = mileage[i].replace(',', '')

    # convert years to integer and price to float
    year = list(map(int, year))
    price = list(map(float, price))
    mileage = list(map(float, mileage))

    if page == 0:
        data = {'Year':year,
                'Make':make,
                'Model':model,
                'Trim':trim,
                'Mileage':mileage,
                'Price':price}
        df = pd.DataFrame(data)

    else:
        data = {'Year':year,
                'Make':make,
                'Model':model,
                'Trim':trim,
                'Mileage':mileage,
                'Price':price}
        df1 = pd.DataFrame(data)
        df  = df.append(df1, ignore_index=True)

    # wait to go to next page
    time.sleep(random.randrange(10))
    count = count + 1
    print(count)



df.to_feather(urlModel + '.feather')
