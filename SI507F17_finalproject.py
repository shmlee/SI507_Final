from bs4 import BeautifulSoup as Soup
import unittest
import requests
import csv
from datetime import datetime
import json
import sys
import psycopg2
import psycopg2.extras
from flask import Flask, render_template
from flask_script import Manager
from config import *

# from section-week-6 
CACHE_FNAME = 'cache_file.json'
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
DEBUG = True
db_connection = None
db_cursor = None

try:
    with open(CACHE_FNAME, 'r') as cache_file:
        cache_json = cache_file.read()
        CACHE_DICTION = json.loads(cache_json)
except:
    CACHE_DICTION = {}


def get_from_cache(url):
    """If URL exists in cache and has not expired, return the html, else return None"""
    if url in CACHE_DICTION:
        url_dict = CACHE_DICTION[url]

        html = CACHE_DICTION[url]['html']
    else:
        html = None

    return html


def set_in_cache(url, html):
    """Add URL and html to the cache dictionary, and save the whole dictionary to a file as json"""
    CACHE_DICTION[url] = {
        'html': html,
        'timestamp': datetime.now().strftime(DATETIME_FORMAT),
        # 'expire_in_days': expire_in_days
    }

    with open(CACHE_FNAME, 'w') as cache_file:
        cache_json = json.dumps(CACHE_DICTION)
        cache_file.write(cache_json)


def get_html_from_url(url):
    """Check in cache, if not found, load html, save in cache and then return that html"""
    # check in cache
    html = get_from_cache(url)
    if html:
    	if DEBUG:
            print('Loading from cache: {0}'.format(url))
            print()
    else:
        if DEBUG:
            print('Fetching a fresh copy: {0}'.format(url))
            print()

        # fetch fresh
        response = requests.get(url)

        html = response.text

        # cache it
        set_in_cache(url, html)

    return html


##################Cached pages##################
most_popular_html = get_html_from_url("https://www.fontsquirrel.com/fonts/list/popular")
most_popular_soup= Soup(most_popular_html, 'html.parser')
# print(most_popular_soup)

hottest_web_html = get_html_from_url("https://www.fontsquirrel.com/fonts/list/hot_web")
hottest_web_soup = Soup(hottest_web_html, 'html.parser')


# Defining first class, table 1

class Font:
	def __init__(self, font_name, img, font_style):
		self.font_name = font_name
		self.img = img
		self.font_style = font_style
		

	def __str__(self):
		return "This font name is {}, has {} styles".format(self.font_name,len(self.font_style))

	def __contains__(self,any_font):
		return any_font in self.font_name

	def __repr__ (self):
		return "Name is {}, has {} styles".format(self.font_name, len(self.font_style))

	def get_dict(self):
		return {
			"font_name": self.font_name,
			"img": self.img,
			"font_style": self.font_style,
		}


# Define second class, table 2

class Top_fonts:
	def __init__(self):
		self.hot_fonts = []
		self.popular_fonts = []

	def get_hot_fonts(self):
		return self.hot_fonts

	def get_popular_fonts(self):
		return self.popular_fonts

	def add_font(self, font, type):
		if type == 'trend':
			self.hot_fonts.append(font)
		elif type == 'popular':
			self.popular_fonts.append(font)





three_fonts = ['sans serif', 'serif', 'slab serif']
fonts_obj = [] #this is a list of font instances with font_name, img, etc attributes

my_top_fonts = Top_fonts()

##################Using popular_page cache##################

popular_links = most_popular_soup.find("div",{"id":"font_list"}).find_all("div",{"class":"fontlistitem"})
# popular_front_img = most_popular_soup.find('div',{"id":"listing_image"}).find_all("img")
# print (popular_front_img)
	# souping individual font's url
for i in range(0, 20):
	open_font = popular_links[i].find('a')['href']
	# print('font url:', open_font)
	open_web_html = get_html_from_url(open_font)
	open_font_soup = Soup(open_web_html, 'html.parser')

	classification = open_font_soup.find('div',{'id':'product_info'}).find_all('table')[1].find_all("a") 
	# print(classification)
	# font_lang = open_font_soup.find('td',{'id':'js_full_langs'}).find_all('a')
	
	
	for link in classification:
	    if (three_fonts[0] in link['href']) or (three_fonts[1] in link['href']) or (three_fonts[2] in link['href']):
	    	# print('true')
	    	img = open_font_soup.find("div", id="panel_sample").find("img").get('src')
	    	font_name = open_font_soup.find_all('h1')[0].text.strip()
	    	# had gaps between styles and filter function helps out to solve this question
	    	font_style = open_font_soup.find('div',{'id':'product_info'}).find_all('table')[0].text.strip()
	    	font_style = "\n".join(filter(None, font_style.split("\n"))).strip()
	    	font_style_list = font_style.split("\n")
	    	count = len(font_style_list)

	    	font_obj = Font(font_name, img, font_style_list) #class Font
	    	my_top_fonts.add_font(font_obj, 'popular') #class Top_fonts

	    	fonts_obj.append(font_obj)
	    	# print(img)

# for font in fonts_obj:
# 	print(str(font))
##################Using hottest_font_page cache##################

hot_web_links = hottest_web_soup.find("div",{"id":"font_list"}).find_all("div",{"class":"fontlistitem"})
hot_web_img = hottest_web_soup.find('div',{"class":"listing_image"}).find_all("img")
fonts_obj2 = [] #this is a list of hot font instances with font_name, img, etc attributes

for x in range(0,20):
	hot_font = hot_web_links[x].find('a')['href']
	open_web_html2 = get_html_from_url(hot_font)
	open_font_soup2 = Soup(open_web_html2, 'html.parser')

	classification2 = open_font_soup2.find('div',{'id':'product_info'}).find_all("a")
	
	for link2 in classification2:
		if (three_fonts[0] in link2['href']) or (three_fonts[1] in link2['href']) or (three_fonts[2] in link2['href']):
			imgs2 = open_font_soup.find("div", id="panel_sample").find("img").get('src')
			font_name = open_font_soup2.find_all('h1')[0].text.strip()
			font_style = open_font_soup2.find('div',{'id':'product_info'}).find_all('table')[0].text.strip()
			font_style = "\n".join(filter(None, font_style.split("\n"))).strip()
			font_style_list = font_style.split("\n")
			count = len(font_style_list)


			font_obj2 = Font(font_name, img, font_style_list)
			my_top_fonts.add_font(font_obj2, 'trend')
			
			fonts_obj2.append(font_obj2)

# for font in fonts_obj2:
# 	print(str(font))

# print(font_tag)
# styles = len([style.text for style in font_style])
# print (styles)
# print(font_lang)
# print (type(font_name))
# print (type(fonts_obj))
# print (type(font_obj))


def get_connection_and_cursor():
    global db_connection, db_cursor
    if not db_connection:
        try:
            db_connection = psycopg2.connect("dbname='{0}' user='{1}' password='{2}'".format(db_name, db_user, db_password))
            print("Success connecting to database")
        except:
            print("Unable to connect to the database. Check server and credentials.")
            sys.exit(1) # Stop running program if there's no db connection.

    if not db_cursor:
        db_cursor = db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    return db_connection, db_cursor


def setup_database():
    conn, cur = get_connection_and_cursor()

 
    cur.execute("""DROP TABLE IF EXISTS Fonts""")


    cur.execute("""CREATE TABLE IF NOT EXISTS Fonts(
    font_name VARCHAR (255) PRIMARY KEY, 
    img TEXT,
    font_style TEXT,
    font_tag VARCHAR (255)
    )""")

    cur.execute("""DROP TABLE IF EXISTS Top_fonts""")

    cur.execute("""CREATE TABLE IF NOT EXISTS Top_fonts(
    type TEXT,
    font TEXT
    )""")

	# img VARBINARY(MAX),

    db_connection.commit()

setup_database()

hot_fonts_list = my_top_fonts.get_hot_fonts()
for font in hot_fonts_list:
	# print(type(font))
	db_cursor.execute("""INSERT INTO Fonts(font_name,img,font_style) VALUES (%(font_name)s, %(img)s, %(font_style)s) ON CONFLICT DO NOTHING""", font.get_dict())
	hot_font_dict = {"type":"hot_font","font":font.font_name} # values are converting to VALUES
	db_cursor.execute("""INSERT INTO Top_fonts(type, font) VALUES (%(type)s, %(font)s)""",hot_font_dict)
db_connection.commit()

popular_fonts_list = my_top_fonts.get_popular_fonts()
for font in popular_fonts_list:
	db_cursor.execute("""INSERT INTO Fonts(font_name,img,font_style) VALUES (%(font_name)s, %(img)s, %(font_style)s) ON CONFLICT DO NOTHING""", font.get_dict())
	popular_font_dict = {"type":"popular_font","font":font.font_name}
	db_cursor.execute("""INSERT INTO Top_fonts(type, font) VALUES (%(type)s, %(font)s)""",popular_font_dict)
db_connection.commit()


app = Flask(__name__)

@app.route('/')
def comparing_fonts():
	popular_font_str_list = []
	for font in popular_fonts_list:
		popular_font_str_list.append(str(font))
	return render_template('values.html', long_name='Sharon', popular_fonts=popular_font_str_list)

	hot_fonts_str_list = []
	for font in hot_fonts_list:
		hot_font_str_list.append(str(font))
	return render_template('values.html', long_name='Sharon', hot_fonts=hot_font_str_list)

if __name__ == '__main__':
	#app.run('localhost', 8080, debug=True)
	app.run('localhost', 8080, debug=True)




 
