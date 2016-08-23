import os
import random
import requests
from bs4 import BeautifulSoup as Soup
from urllib.parse import urlparse
title = "firstHeading"

randoURL = "http://www.wikihow.com/Special:Randomizer"
images = {"class": "whcdn"}
title = {"class": "firstHeading"}

def getwikihow():
    r = requests.get(randoURL)
    xml = r.text;
    soup = Soup(xml, "html.parser" )
    wikititle = soup.find("h1", title).string or "WHAT DID YOU DO"
    wikiimages = soup.findAll("img", images)
    print(len(wikiimages))
    valid_urls = []
    for img in wikiimages:
        if 'src' in img.attrs:
            valid_urls.append(img['src'])
        elif 'data-src' in img.attrs:
            valid_urls.append(img['data-src'])
    print(len(valid_urls))
    if len(valid_urls) > 0:
        wikiimg = random.choice(valid_urls)
    else:
        wikiimg = "http://i0.kym-cdn.com/photos/images/original/000/581/658/b04.png"
    return (wikititle, wikiimg)


