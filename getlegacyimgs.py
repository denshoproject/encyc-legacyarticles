import bs4
import urllib
import os
from urllib.request import Request, urlopen
from urllib import parse

camps = ['Tanforan', 'Santa_Anita', 'Merced', 'Pomona', 'Tulare', 'Turlock']
urls = []
for camp in camps:
    urls.append('https://encyclopedia.densho.org/{}_(detention_facility)'.format(camp))

pages = []
for url in urls:
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    print("Trying to download {}...".format(url))
    rawpage = urlopen(req).read()
    pages.append(rawpage)
    
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
    with open(imgfile, 'wb') as f:
        with urllib.request.urlopen(req) as r:
            f.write(r.read())


