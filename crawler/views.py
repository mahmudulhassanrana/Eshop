from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
from .models import ProductInfo,product_user_compare
import requests
import json
# Create your views here.

def BDShopCrawler(max_pages, search_item):
    baseurl = "https://www.bdshop.com/"

    headers = {'user agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

    url = 'https://www.bdshop.com/search/?q=' + search_item 
    print(url)
    r= requests.get(url)
    soup = BeautifulSoup(r.content,'lxml')
    productlist = soup.find_all('div', class_='prolabels-wrapper')

    #print(productlist)

    productlinks = []

    for item in productlist:
        for link in item.find_all('a',href=True):       
            #print(link['href'])
            productlinks.append(link['href'])
        #print(productlinks)
    #return productlinks
    product_description = []
    information = {}
    driver = webdriver.Firefox()
    for link in productlinks:
        driver.get(link)
        sleep(10) # Sleep 10 seconds while waiting for the page to load...

        html = driver.page_source
        soup = BeautifulSoup(html, "lxml") 
        title = soup.find('span', class_='base').text.strip()
        price=soup.find('span', {'class': 'price'}).text.strip()
        img = soup.find('img', {'class': 'fotorama__img'})['src']
        try:
            ratings = soup.find('div', class_='aggregated-rating-absolute').text.strip()
        except:
            ratings = 'not found'
        
        

        product_detaills = ProductInfo(title=title,price=price,img=img,search_item=search_item,ratings=ratings)
        product_detaills.save()

        information = {
            'name':title,
            
            'image':img,
            'price':price
        }
        
        product_description.append(information)
    driver.close()
    return product_description

def PickabooCrawler(search_item):
        list_of_product_details = []
        url = 'https://www.pickaboo.com/catalogsearch/result/?q=+' + search_item + "'"
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, features="html.parser")
        for link in soup.findAll('a', {'class': 'product photo product-item-photo'}):
            href = link.get('href')
            list_of_product_details.append(getPickabooProductDetails(href))
        return list_of_product_details   


def getPickabooProductDetails(product_url):
    
        product_details = {}

        chrome_path = r"E:\University\10th Semester\Web Project II\Project Workspace\Budget Commerce\version1\chromedriver.exe"
        driver = webdriver.Chrome(chrome_path)

        driver.get(product_url)
        sleep(10) # Sleep 10 seconds while waiting for the page to load...

        source_code = driver.page_source
        soup = BeautifulSoup(source_code, "lxml")
        product_info = soup.findAll('div', {'class': 'column main'})
        
        for product in product_info:
            img     = product.find('img', {'class': 'fotorama__img magnify-opaque'})['src']
            brand   = product.find('div', {'class': 'manufacturer'}).find('span').text
            title   = product.find('span', {'class': 'base'}).text
            price   = product.find('span', {'class': 'price'}).text

        product_details = {
            'title' : title,
            'brand' : brand,
            'price' : price,
            'img' : img
        }

        driver.close()

        return (product_details)


def jadrooCrawler(max_pages,search_item):
    baseurl = "https://www.jadroo.com/"

    headers = {'user agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

    page= 1

    while page <= max_pages:
        url = 'https://www.jadroo.com/shop?s=' + search_item 
        print(url)
        r= requests.get(url)
        soup = BeautifulSoup(r.content,'lxml')
        productlist = soup.find_all('div', class_='product-info text-left')

        #print(productlist)
        
        productlinks = []

        for item in productlist:
            for link in item.find_all('a',href=True):       
                #print(link['href'])
                productlinks.append(link['href'])
            #print(productlinks)
        #return productlinks
        information = {}
        product_description=[]
        driver = webdriver.Firefox()
        for link in productlinks:
            driver.get(link)
            sleep(10) # Sleep 10 seconds while waiting for the page to load...

            html = driver.page_source
            soup = BeautifulSoup(html, "lxml") 
            title = soup.find('h1', class_='name').text.strip()
            try:
                ratings = soup.find('div', class_='col-md-6 single-rating-number').text.strip()
            except:
                ratings = 'not found'
            try:
                img = soup.find('img', {'class': 'img-responsive single-large-image featured_image'})['src']
            except:
                img = 'not found'
            try:
                price=soup.find('span', {'class': 'price'}).text.strip()
            except:
                price = 'not found'
            try:
                old_price=soup.find('span', {'class': 'price-strike'}).text.strip()
            except:
                old_price = 'not found'
            product_detaills = ProductInfo(title=title,price=price,img=img,search_item=search_item,ratings=ratings)
            product_detaills.save()


            information = {
                'title':title,
                
                'img':img,
                'price':price,
                'old_price':old_price,
                'search_item':search_item
            }
            
            product_description.append(information)


        driver.close()

        return product_description




def showProduct(request):
    search_item = request.GET['search_item']
    search_item.replace('','+')
    productsInfo = ProductInfo.objects.filter(search_item = search_item)
    if productsInfo.exists():
        context={
            'products':productsInfo         
        }
        return render(request, 'search_product.html', context)
    else:
        product  = BDShopCrawler(1,search_item)
        #products     += PickabooCrawler(1,search_item)
        product     += jadrooCrawler(1,search_item)
        productsInfo = ProductInfo.objects.filter(search_item = search_item)
        context={
            'products':productsInfo
        }
        return render(request, 'search_product.html', context)
    
def single_Product(request,id):
    ProductsInfo = ProductInfo.objects.get(pk=id)
    context={
        'products':ProductsInfo,
        
    }
    return render(request, 'single_product.html', context)
