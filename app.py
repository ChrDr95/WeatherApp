# -*- coding: utf-8 -*-

from flask import Flask,json,jsonify
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import re
app = Flask(__name__)
WEATHER_URL = 'https://www.timeanddate.com/weather/'


@app.route('/')
def home():
    return "Please insert first the name of the Country and then the city <br /> Example:Guatemala/Guatemala"


@app.route('/<string:country>/<string:city>')
def get_weather(country, city):
    weather = get_report(country, city)
    return jsonify(weather.__dict__)


def to_num(text):
    return int(re.search(r'\d+', text).group())


def scrape_info(for_soup):

    page_soup = soup(for_soup, "html.parser")
    temperature = to_num(page_soup.find_all("div", {"id": "qlook"})[0].find_all('div')[1].text)
    humid_press = page_soup.find_all("div", {"id": "qfacts"})[0].find_all('p')
    pressure = to_num(humid_press[4].text)
    humidity = to_num(humid_press[5].text)
    city_weather = CityWeather(temperature, humidity, pressure)
    return city_weather


def get_weather_url(country, city):
    return WEATHER_URL + country + "/" + city


def get_report(country,city):
    try:
        weather_url = get_weather_url(country, city)
        request_website = urlopen(weather_url)
        report = scrape_info(request_website)

    except:
        print("Error: City couldn't be found")
    return report


if __name__ == '__main__':
    app.run()


class CityWeather:
    def __init__(self,temperature,humidity,pressure):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure

