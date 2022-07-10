import os, json, time
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

def save_json(data, dfile):
    json_text = json.dumps(data)
    with open(dfile, 'w', encoding="utf-8") as ofile:
        ofile.write(json_text)

# https://unicode.org/emoji/charts/full-emoji-list.html
# https://www.unicode.org/emoji/charts-15.0/emoji-ordering.html
# https://www.unicode.org/cldr/cldr-aux/charts/34/supplemental/territory_subdivisions.html#cosap

def process_inventory_file(fname):
    inventory = []
    with open(fname, encoding="utf-8") as ifile:
        ftext = ifile.read()
        soup = BeautifulSoup(ftext, 'html.parser')
        table = soup.find('table')
        for row in table.find_all("tr"):
            contents = row.find_all(recursive=False)
            if len(contents)==1:
                head = contents[0]
                classes = head.attrs['class']
                name = head.get_text()
                if 'bighead' in classes:
                    citems = []
                    inventory.append({'name':name, 'items':citems})
                elif 'mediumhead' in classes:
                    scitems = []
                    citems.append({'name':name, 'items':scitems})
            else:
                if contents[0].name=='th':
                    continue
                #print((contents[2].get_text(),contents[-1].get_text()))
                scitems.append({'text':contents[2].get_text(), 'cldr':contents[-1].get_text()})
    #print(inventory)
    return inventory

def generate_inventory_from_list():
    url = 'https://unicode.org/emoji/charts/full-emoji-list.html'
    cfile = 'cache_inventory.html'
    if not recent_cache(cfile):
        print("Downloading inventory file")
        download_page(url,cfile)
    else:
        print("Inventory cache found")
    data = process_inventory_file(cfile)
    for i in data:
        print(i['name'])
        for j in i['items']:
            print("  %s (%d) " % (j['name'],len(j['items'])))
    save_json(data,"data_inventory.json")

generate_inventory_from_list()
