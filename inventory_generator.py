import os, time
import requests

from bs4 import BeautifulSoup

def download_page(url, dfile):
    response = requests.get(url)
    html_text = response.text
    with open(dfile, 'w', encoding="utf-8") as ofile:
        ofile.write(html_text)

def recent_cache(file):
    if not os.path.exists(file):
        return False
    dt = time.time() - os.path.getmtime(file)
    #more recent than a week
    return dt < 7*24*3600
# https://unicode.org/emoji/charts/full-emoji-list.html
# https://www.unicode.org/emoji/charts-15.0/emoji-ordering.html

def process_inventory_file(fname):
    with open(fname, encoding="utf-8") as ifile:
        ftext = ifile.read()
        soup = BeautifulSoup(ftext, 'html.parser')
        table = soup.find('table')
        for row in table.find_all("tr"):
            contents = row.find_all(recursive=False)
            if len(contents)==1:
                head = contents[0]
                print(head.attrs['class'][0])
                print(head.get_text())
            else:
                if contents[0].name=='th':
                    continue
                print((contents[2].get_text(),contents[-1].get_text()))

def generate_inventory_from_list():
    url = 'https://unicode.org/emoji/charts/full-emoji-list.html'
    cfile = 'cache_inventory.html'
    if not recent_cache(cfile):
        print("Downloading inventory file")
        download_page(url,cfile)
    else:
        print("Inventory cache found")
    process_inventory_file(cfile)

generate_inventory_from_list()
