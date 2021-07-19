from bs4 import BeautifulSoup
import os, re

RAWPATH = 'content/'
SAVEPATH = 'processed/'

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


def processRaw(soup):
    #perform all soup processing
    #1. Remove share and print elements
    soup.select_one("#share").decompose()
    soup.select_one('script[src="//s7.addthis.com/js/300/addthis_widget.js#pubid=densho"]').decompose()
    #2. Remove next/previous nav, cite and print from sidebar and next/previous nav from mobile version
    prevtag = soup.select_one("#sidebar-left > div > dl:nth-of-type(3)")
    nexttag = soup.select_one("#sidebar-left > div > dl:nth-of-type(4)")
    prevtag.decompose()
    nexttag.decompose()
    soup.select_one("#sidebar-left > div > p").decompose()
    soup.select_one(".visible-phone table").decompose()
    #3. Remove more info links from primary source items
    moretags = soup.select(".more")
    for tag in moretags:
        tag.decompose()
    #4. Remove links from primary source items
    pslinks = soup.select(".primarysource > a")
    for pslink in pslinks:
        pslink.unwrap()
    #5. edit thumbnail cache links; and single mobile version header img
    psimgs = soup.select(".primarysource > img")
    mpsimg = soup.select_one("#media-pointer > a > img")
    if mpsimg:
        psimgs.append(mpsimg)
    for psimg in psimgs:
        psimg['src'] = re.sub('front/media/cache/[a-f0-9]{2,2}/[a-f0-9]{2,2}/','media/encyc-legacy/assets/',psimg['src'])
        del psimg['more']
        del psimg['large']
    #6. Remove from the archive feature
    ftablocks = soup.select(".ddr_objects")
    for ftablock in ftablocks:
        ftablock.decompose()
    #6. Insert legacy article alert immediately after the article title in the body
    ltag = soup.new_tag("div", attrs={'class':'alert alert-info'})
    notetag = soup.new_tag('b')
    notetag.string = "Note:"
    alerttext = "  This is a legacy article that appeared in the Densho Encyclopedia from 2012 to 2021. You can find the current article for this detention facility at: "
    ltag.insert(1, alerttext)
    linkurl = 'https://encyclopedia.densho.org/{}'.format(camp)
    linktag = soup.new_tag('a', href=linkurl)
    linktag.string = linkurl
    ltag.append(linktag)
    soup.select_one('#article').insert(2, ltag)
    
    return soup

#main
for camp in camps:

    htmlfile = os.path.basename('{}.html'.format(camp))
    
    if os.path.exists(os.path.join(RAWPATH, htmlfile)):
        print("Processing {}...".format(htmlfile))
        with open(os.path.join(RAWPATH, htmlfile)) as rawfile:
            soup = BeautifulSoup(rawfile, "html.parser")
            # do all the processing
        soup = processRaw(soup)
   
        with open(os.path.join(SAVEPATH, htmlfile), 'w') as outfile:
            outfile.write(soup.prettify())
    else:
        print("Warning: {} not found...".format(htmlfile))