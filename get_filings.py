#!/usr/bin/env python

"""
Functions for accessing data from sec.gov and extracting specific information

"""

from network import load_url
from string import Template
from lxml import etree
from os import path

USER_AGENT   = "#NastyBoys/1.0 +http://github.com/csytan/nastyboys"

ENCODING     = "utf-8"
SEC_ROOT_URL = "http://www.sec.gov"
SEARCH_URL   = Template("""$root/cgi-bin/browse-edgar?action=getcompany&CIK=$symbol&type=$form&dateb=&owner=exclude&count=100""")

def parse_html (html):
    """Parse the html text with lxml and return the document tree"""

    myparser = etree.HTMLParser(encoding=ENCODING)
    return etree.HTML(html, parser=myparser)

def fetch_document_links (symbol, form_type):
    """Search for the most recent sec form_type filings for symbol and 
    and return a list of the most recent links which point to document
    filing detail pages (the actual document will be a single link within
    the document filing detail page)."""

    results = []
    matches = load_url(SEARCH_URL.substitute(symbol=symbol, form=form_type, root=SEC_ROOT_URL), USER_AGENT)
    if matches is not None:
        tree = parse_html(matches)
        for node in tree.xpath('//a[@id="documentsbutton"]'):
            if node.attrib.has_key('href'):
                results.append( ''.join([SEC_ROOT_URL, node.attrib['href']]) )
    return results

def fetch_latest_document (symbol, form_type):
    """Get the most recent document filing page for this symbol and form type,
    find the link to the complete submission (sgml) text, and return the html
    of the given filing."""

    document_links = fetch_document_links (symbol, form_type)
    if len(document_links) > 0:
        # the first link is the latest one
        document_detail_page = load_url(document_links[0], USER_AGENT)
        if document_detail_page is not None:

            # find the sgml text link containing the full submission
            tree = parse_html(document_detail_page)
            sgml_link = None

            for node in tree.xpath('//a'):
                if node.attrib.has_key('href'):
                    # the first url pointing to a '.txt' file is the complete submission
                    try:
                        if path.splitext(node.attrib['href'])[1] == '.txt':
                            sgml_link = ''.join([SEC_ROOT_URL, node.attrib['href']])
                            break
                    except IndexError:
                        pass

            # with the complete submission link in hand, load it and return it
            if sgml_link is not None:
                return load_url(sgml_link, USER_AGENT)

def get_latest_document (symbol, form_type='10-Q'):
    """Attempt to retrieve the latest filing of form_type for the given symbol,
    parse the text out of the html, and return it as a single string. This function
    returns None if the symbol is invalid, or if there is no such filing, etc."""

    sgml_text = fetch_latest_document (symbol, form_type)
    if sgml_text is not None:
        hdr_index = sgml_text.find('<TEXT>')
        if hdr_index > -1:

            data = []
            html_text = sgml_text[ (hdr_index+len('<TEXT>')): ]
            tree = parse_html(html_text)

            for node in tree.xpath('//body'):
                data.append( ''.join(node.xpath('descendant-or-self::text()')) )

            return ''.join(data)
