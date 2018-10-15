# -*- coding: utf-8 -*-

from flask import Flask,jsonify, render_template
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
app = Flask(__name__)


@app.route('/')
def home():

    return "Please insert first the name of the Country and then the city <br /> Example:Guatemala/Guatemala"


@app.route('/<string:country>/<string:city>')
def city_name(country,city):
    try:
        # Get the weather page to scrap the info (adding the info of the country and city to know the page to access)
        city_web = 'https://www.timeanddate.com/weather/'+country+"/"+city
        uClient = uReq(city_web)
        for_soup = uClient.read()
        page_soup = soup(for_soup, "html.parser")
        # Scrap the Temperature
        temp = page_soup.find_all("div", {"id": "qlook"})[0].find_all('div')
        # Scrap Humidity and Pressure
        info_weather = page_soup.find_all("div", {"id": "qfacts"})[0].find_all('p')
        # turn into normal text so it becomes easier to read
        temperature = temp[1].text
        pressure = info_weather[4].text
        humidity = info_weather[5].text
        # Change the text into integers
        tempint=int(re.search(r'\d+',temperature).group())
        preint=int(re.search(r'\d+',pressure).group())
        humint=int(re.search(r'\d+',humidity).group())

        report= {'Temperature: ':tempint,'Humidity: ':humint,'Pressure: ':preint}
    except:
        print("Error: City couldn't be found")
        report=" Couldn't find the requested city"
    return jsonify({('Weather '+country+' '+city):report})


if __name__ == '__main__':
    app.run()
