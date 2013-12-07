from bs4 import BeautifulSoup
from urllib2 import urlopen
from string import Template
import urllib2
import re
import os
from datetime import datetime

ROOT_URL = "http://www.sec.gov"
SEARCH_URL  = Template("$root/cgi-bin/browse-edgar?"\
        "action=getcompany&CIK=$symbol&type="\
        "$form&dateb=&owner=exclude&count=100")

ENCODING = "utf-8"

def html_parser(url):
    """Parse html file with lxml and return a BS object"""
    
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "lxml", from_encoding=ENCODING)
    
    return soup

def check_time(time_string):
    """Check if the time string matches YYYY-MM-DD format
    if so parse the string and return a python date obj"""

    time_pattern = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}")
    if re.match(time_pattern, time_string):
        time = datetime.strptime(time_string, "%Y-%m-%d").date()
    else:
        time = None
    return time


def fetch_doc_links(symbol, form_type):
    """ Search most recent docs and return a list of links to the
    actual doc filling page"""

    my_url = SEARCH_URL.substitute(root=ROOT_URL, symbol=symbol,
            form=form_type)
    soup = html_parser(my_url)
    my_chunk = soup.findAll("a", {"id": "documentsbutton"})
    
    results = {}
    for item in my_chunk:
        if item.has_attr("href"):
            file_link = "".join([ROOT_URL, item['href']])
            time =  item.parent.parent.findAll('td')[3].string
            time = check_time(time)
            results[time] = file_link

    return results

def fetch_latest_doc(symbol, form_type):
    """get the most recent doc """
    doc_links = fetch_doc_links(symbol, form_type)
    if len(doc_links) > 0:
        sorted_doc_links = sorted(doc_links.iteritems(), key=lambda (k,v): k, reverse=True)
        latest_doc_link = sorted_doc_links[0][1]

        soup = html_parser(latest_doc_link)
        sgml_link = None

        for node in soup.findAll("a"):
            if node.has_attr("href"):
                try:
                    current_link =  node['href']
                    # only save link to the txt file
                    patrn = re.compile(".*\.txt$")
                    if re.match(patrn, current_link):
                        sgml_link = ROOT_URL + current_link
                        break
                except IndexError:
                    pass
    if sgml_link is not None:
        return sgml_link


                        
test = fetch_latest_doc(symbol="AAPL", form_type="10-K")
print test
import ipdb; ipdb.set_trace()
soup = urlopen(test).read()
hdr_index = soup.find('<TEXT>')
if hdr_index > -1:
    html_text = soup[ (hdr_index+len('<TEXT>')): ]
    tree = BeautifulSoup(html_text)

test2 = soup.findAll("<TEXT>")



