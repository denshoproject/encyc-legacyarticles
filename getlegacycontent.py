import bs4
import urllib
import os
from urllib.request import Request, urlopen
from urllib import parse, error

SAVEPATH = 'content_out/'

camps = ['Portland_(detention_facility)', 
         'Mayer_(detention_facility)', 
         'Puyallup_(detention_facility)', 
         'Amache_(Granada)', 
         'Gila_River',
         'Heart_Mountain',
         'Manzanar',
         'Minidoka',
         'Poston_(Colorado_River)', 
         'Rohwer',
         'Topaz'] 

pages = []
for camp in camps:
    url = 'https://encyclopedia.densho.org/{}'.format(camp)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    print("Trying to download {}...".format(url))
    try: 
        rawpage = urlopen(req).read()
    except urllib.error.HTTPError as e:
        print("Couldn't download {} (http error: {})...".format(url,e.code))
    else:
        pages.append(rawpage)
        htmlfile = os.path.join(SAVEPATH, os.path.basename('{}.html'.format(camp)))
        with open(htmlfile, 'wb') as f:
            f.write(rawpage)
    
goodimgs = []
for page in pages:
    soup = bs4.BeautifulSoup(page, "html.parser")
    for img in soup.find_all('img'):
        if img.has_attr('large'):
            if 'cache' in img['large']:
                goodimgs.append(img['large'])

for goodimg in goodimgs:
    print(goodimg)
    req = Request(goodimg, headers={'User-Agent': 'Mozilla/5.0'})
    imgfile = os.path.basename(urllib.parse.urlparse(goodimg).path)
    print("Downloading {}...".format(imgfile))
    imgpath = os.path.join(SAVEPATH,'assets', os.path.basename(imgfile))
    with open(imgpath, 'wb') as f:
        with urllib.request.urlopen(req) as r:
            f.write(r.read())


