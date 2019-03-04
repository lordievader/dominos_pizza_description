#!/usr/bin/env python3
"""Dominos menu parser.
"""
import sys
import urllib.request
from bs4 import BeautifulSoup

BASE_URL = 'https://www.dominos.nl/'
MENU_URL = 'https://www.dominos.nl/menu'
USER_AGENT = (
    'Mozilla/5.0 (X11; Linux x86_64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.39 Safari/537.36')


def get(url, user_agent=''):
    """Grabs a web page.

    :param url: url to grab
    :type url: str
    :param user_agent: user agent to use
    :type user_agent: str
    """
    request = urllib.request.Request(url)
    request.add_header('User-Agent', user_agent)
    with urllib.request.urlopen(request) as webpage:
        data = webpage.read()

    return data


def parse_links(html):
    """Parse an html file for Dominos menu links.

    :param html: the webpage to parse
    :type html: str
    :return: dictionary of {name: url}
    """
    soup = BeautifulSoup(html, features='html.parser')
    links = {}
    for link in soup.find_all('a'):
        if link.has_attr('aria-label'):
            name = link.get('aria-label').replace(', ', '').lower()
            url = link.get('href')
            links[name] = url

    return links


def info(links, search):
    """Grab the description for the requested pizza.

    :param links: dictionary of where to find the pizza info pages
    :type links: dictionary
    :param search: pizza to search for
    :type search: str
    """
    for name, url in links.items():
        if search.lower() in name:
            full_url = BASE_URL + url
            html = get(full_url)
            break

    else:
        html = ''

    soup = BeautifulSoup(html, features='html.parser')
    for paragraph in soup.find_all('p'):
        if (paragraph.has_attr('itemprop') and
                paragraph.get('itemprop') == 'description'):
            description = paragraph.text
            break

    else:
        description = ''

    return description


def main():
    """Main function.
    """
    search = sys.argv[1]
    html = get(MENU_URL)
    links = parse_links(html)
    description = info(links, search)
    print(description)


if __name__ == '__main__':
    main()
