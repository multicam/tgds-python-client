import sys
from datetime import datetime
import requests
from bs4 import BeautifulSoup

RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"
REVERSE = "\033[;7m"


def unit_file_name(unit):
    return 'data/units/'+unit+'.html'


def show_item(item):
    print('//', item['label'], item['slug'])
    for i in item['children']:
        print('--', i.name)


def parse_one(page_content):
    soup = BeautifulSoup(page_content, "html.parser")
    root = soup.find(id='layoutContentWrapper')

    links = []
    parse_links = root.find_all('a', href=True)
    for i in parse_links:
        link_url = i['href']
        links.append({'label': i.text.strip(), 'url': link_url})

    print('LINKS', links)

    # Unit of Competency
    parse_items = root.select('.content body > *')
    item = {'slug': '', 'label': '', 'children': []}

    for i in parse_items:
        # print('--', i.name)
        if i.name == 'h2':
            show_item(item)
            item = {
                'slug': i.text.strip().replace(' ', '_').lower(),
                'label': i.text.strip(),
                'children': []
            }
        else:
            item['children'].append(i)

    print('--- AAA ---')
    # Assessment Requirements
    parse_items = root.select('.content')[1].select
    temp = {'slug': '', 'label': '', 'children': []}

    if parse_items:
        # for j in parse_items:
        #     # print('--', j.name)
        #     if j.name == 'h2':
        #         show_item(item)
        #         item = {
        #             'slug': i.text.strip().replace(' ', '_').lower(),
        #             'label': i.text.strip(),
        #             'children': []
        #         }
        #     else:
        #         item['children'].append(i)
        print('-- AAA parsed --')


def scrape_one(unit):
    file = open(unit_file_name(unit), 'r')
    page = file.read()
    file.close()
    parse_one(page)


def save_one(unit):
    root_url = 'https://training.gov.au/Training/Details/'
    url = root_url + unit
    print(url)

    page = requests.get(url)

    file = open(unit_file_name(unit), 'w')
    file.write(page.text)
    file.close()


def scrape_cuv_40720():
    units = ['BSBCRT411',  'CUADES411', 'CUADES412', 'CUADES301', 'CUADES302', 'CUADES303', 'CUADES304', 'CUADES305', 'CUAGRD312', 'CUAPPR411',  'CUAACD411', 'CUAGRD411', 'CUAPHI411',  'CUAPHI403', 'CUAWHS312']

    for i in units:
        # save_one(i)
        scrape_one(i)
        # break

    print('done.')


