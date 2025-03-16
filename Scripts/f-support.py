#!/bin/python3
import sys

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

req = Request('https://docs.fedoraproject.org/en-US/releases/eol/', headers={'User-Agent': 'Mozilla/5.0'})
html_page = urlopen(req).read()

soup = BeautifulSoup(html_page, 'html.parser')

supported = []
for blocks in soup.findAll('span', attrs={'class': 'nav-text'}):
    if blocks.text == 'Supported Releases':
        items = blocks.parent.findAll('li', attrs={'class': 'nav-item'})
        for item in items:
            supported.append(item.findAll('a')[0].text)

eol = []
nav_lists = soup.findAll('a', attrs={'class': 'nav-link'})
for menu in nav_lists:
    if menu.text == 'EOL Releases':
        items = menu.parent.findAll('li', attrs={'class': 'nav-item'})
        for item in items:
            eol.append(item.findAll('a', attrs='nav-link')[0].text)

try:
    version = sys.argv[1]
    if not version.startswith('F'):
        print('First parameter must have this format: [ F39, F40... ]')
        sys.exit(3)

    if version in supported:
        print(f'Fedora: {version} is supported')
        sys.exit(0)
    elif version in eol:
        print(f'Fedora: {version} is not supported')
        sys.exit(1)
    else:
        print(f'Fedora: {version} not found')
        sys.exit(2)
except IndexError as _:
    print('First parameter required: [ F39, F40... ]')
    sys.exit(3)