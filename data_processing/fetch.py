#!/usr/bin/python

import os
import requests
from lxml import html
from urlparse import urlparse, urljoin

URL = "http://www.aph.gov.au/Parliamentary_Business/Hansard/Search?page=1&q=&ps=25&drt=2&drv=7&drvH=7&f=28%2f09%2f2010&to=01%2f06%2f2013&pnu=43&pnuH=43&pi=0&chi=2&coi=2&st=1"


def get_data(url):
    page = requests.get(url)
    tree = html.fromstring(page.text)
    for link in tree.cssselect("ul.search-filter-results p.action a"):
        href = link.attrib["href"]
        if "fileType=text%2Fxml" in href:
            filename = urlparse(href).path.split("/")[-1]
            if os.path.exists(filename):
                continue
            print "DOWNLOADING: %s" % href
            open(filename, "w").write(requests.get(href).text.encode("utf8"))

    next = tree.cssselect("li.button.next a")[0]
    return urljoin(URL, next.attrib["href"]), page


def crawl(url=URL):
    while True:
        print "READING: %s" % url
        url, page = get_data(url)
    return page
