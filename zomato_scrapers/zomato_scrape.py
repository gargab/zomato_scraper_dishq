from .serializers import *
from .models import *

import urllib2
from bs4 import BeautifulSoup
import requests


def zomato_scrape():

    #Everytime the scraper runs, it deletes all the previous entries and then feteches data
    restaurant.objects.all().delete()
    review.objects.all().delete()

    #Headers mimic web browser kind of call
    zomato='https://www.zomato.com/bangalore/restaurants?page=1'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    response = requests.get(zomato,headers=headers)
    content = response.content
    soup = BeautifulSoup(content,"html.parser")

    #Use parse a particular div to get the total number of pages
    pages = soup.find_all("div",attrs={"class": "col-l-4 mtop pagination-number"})
    total_pages = int(pages[0]['aria-label'].split('of ')[1])
    print total_pages

    for page in range(1,total_pages+1):
        zomato='https://www.zomato.com/bangalore/restaurants?page='+str(page)
        response = requests.get(zomato,headers=headers)
        content = response.content
        soup = BeautifulSoup(content,"html.parser")

        #top_rest finds all the cards of restaurants
        top_rest = soup.find_all("div",attrs={"class": "card search-snippet-card search-card "})

        #Finds the script that contains Lat and Long values of restaurants
        script = soup.find_all("script",attrs={"type": "text/javascript"})[8]
        text_script = script.text.strip().split('zomato.DailyMenuMap.mapData =')[1]
        print zomato

        list_rest =[]
        i = 1
        for tr in top_rest:
            dataframe ={}
            #specific places to find particular values
            dataframe["name"] = (tr.find("a",attrs={"data-result-type": "ResCard_Name"})).text.strip().replace('\n', ' ').encode('unicode-escape')
            dataframe["url"] = (tr.find("a",attrs={"data-result-type": "ResCard_Name"}))['href'].encode('unicode-escape')
            dataframe["address"] = (tr.find("div",attrs={"class":"col-m-16 search-result-address grey-text nowrap ln22"})).text.replace('\n', ' ').encode('unicode-escape')
            dataframe["lat"] = text_script.split('"lat":')[i][0:13].split(",")[0].encode('unicode-escape')
            dataframe["long"] = text_script.split('"lon":')[i][0:13].split(",")[0].encode('unicode-escape')
            dataframe["rating"] = text_script.split('"rating":')[i][1:4].encode('unicode-escape')
            i=i+1
            list_rest.append(dataframe)

        #Save to the model
        serial_rest = restaurantSerializer(data=list_rest,many=True)

        if serial_rest.is_valid():
            serial_rest.save()
        else:
            print serial_rest.errors

        #Iterate through all restaurant links and find reviews
        for rest in list_rest:
            all_reviews=[]
            response = requests.get(rest['url'],headers=headers)
            content = response.content
            soup = BeautifulSoup(content,"html.parser")
            reviews = soup.find_all("div",attrs={"data-snippet": "restaurant-review"})

            for rev in reviews:
                review_val={}
                name = rev.find('div',attrs={"class": "header nowrap ui left"})
                content = rev.find('div',attrs={"class": "rev-text mbot0 "})

                if name and content is not None:
                    review_val['cust_name'] = name.find('a').text.strip().replace('\n','').encode('unicode-escape')
                    review_val['content'] = content.text.split('Rated')[1].strip().replace('\n','').encode('unicode-escape')
                    review_val['rest_name'] = rest['name']
                    all_reviews.append(review_val)

            serial_review = reviewSerializer(data=all_reviews,many=True)
            if serial_review.is_valid():
                serial_review.save()
            else:
                print serial_review.errors
