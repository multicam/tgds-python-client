import sys
from datetime import datetime
import requests
import json
from bs4 import BeautifulSoup


def unit_file_name(unit):
    return 'data/units/'+unit+'.html'


def unit_json_name(unit):
    return 'data/json/'+unit+'.json'


def show_item(item):
    print('//', item['label'], item['slug'])
    for i in item['children']:
        print('/-', i)


def parse_items_fn(items):
    item = {'slug': '', 'label': '', 'children': []}
    bootstrapped = False
    res = []


    for i in items:
        # print('--', i.name)
        if i.name == 'h2':
            if bootstrapped:
                res.append(item)
            else:
                bootstrapped = True

            show_item(item)
            item = {
                'slug': i.text.strip().replace(' ', '_').lower(),
                'label': i.text.strip(),
                'children': []
            }
        else:
            for tag in i.recursiveChildGenerator():
                try:
                    del tag.attrs
                except AttributeError:
                    pass

            del i['class']
            del i['style']
            del i['width']
            item['children'].append(str(i).replace('\n', '').replace(' ', ''))

    return res


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
    res = parse_items_fn(parse_items)

    return res

    # print('--- AAA ---')
    # # Assessment Requirements
    # parse_items = root.select('.content')[1]
    # parse_items = parse_items.select('body > *')
    #
    # if parse_items:
    #     # parse_items_fn(parse_items)
    #     print('-- AAA parsed --')
    #


def scrape_one(unit):
    file = open(unit_file_name(unit), 'r')
    page = file.read()
    file.close()
    print('---')
    print('--- ', unit, '-----------------------------------------------------------------')
    print('---')
    res = parse_one(page)

    print(res)
    with open(unit_json_name(unit), 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=4)


def save_one(unit):
    root_url = 'https://training.gov.au/Training/Details/'
    url = root_url + unit
    print(url)

    page = requests.get(url)

    file = open(unit_file_name(unit), 'w')
    file.write(page.text)
    file.close()


def scrape_cuv_40720():
    units = ['BSBCRT411', 'CUADES411', 'CUADES412', 'CUADES301', 'CUADES302', 'CUADES303', 'CUADES304', 'CUADES305', 'CUAGRD312', 'CUAPPR411',  'CUAACD411', 'CUAGRD411', 'CUAPHI411',  'CUAPHI403', 'CUAWHS312']

    for i in units:
        # save_one(i)
        scrape_one(i)
        # break

    print('done.')


