import json

def generate_cardpairs_format(in_file, out_file, category):
    odata = []
    with open(in_file, encoding="utf-8") as ifile:
        data = json.load(ifile)
        for i in data:
            #print(i['name'])
            if i['name'] == category:
                for j in i['items']:
                    for k in j['items']:
                        odata.append((k['text'],k['cldr']))
    with open(out_file, 'w', encoding="utf-8") as ofile:
        ofile.write(json.dumps(odata))

ref = [
    ("Smileys & Emotion","cards-utf8-smileys.json"),
    ("People & Body","cards-utf8-people.json"),
    ("Animals & Nature","cards-utf8-animals.json"),
    ("Food & Drink","cards-utf8-food.json"),
    ("Travel & Places","cards-utf8-travel.json"),
    ("Activities","cards-utf8-activities.json"),
    ("Objects","cards-utf8-objects.json"),
    ("Symbols","cards-utf8-symbols.json"),
]

for cat, ofile in ref:
    generate_cardpairs_format("data_inventory.json",ofile,cat)