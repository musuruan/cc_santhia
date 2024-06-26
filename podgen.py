#!/usr/bin/env python3

from datetime import datetime
import requests
from feedgen.feed import FeedGenerator
from bs4 import BeautifulSoup

BASEURL = "https://www.comune.santhia.vc.it/"
PODCASTPAGE = BASEURL + "registrazioni?RTipo=24"
PODCASTNAME = "audio_cc_santhia.xml"
GITHUBBASE = "https://raw.githubusercontent.com/musuruan/cc_santhia/main/"
PODCASTURL =  GITHUBBASE + PODCASTNAME
LOGOURL = GITHUBBASE + "logo.jpg"

def main():
    fg = FeedGenerator()
    fg.title("Registrazioni Consiglio Comunale Santhià")
    fg.description("Podcast non ufficiale con le registrazioni audio del Consiglio Comunale di Santhià")
    fg.logo(LOGOURL)
    fg.link(href=PODCASTPAGE, rel="alternate")
    fg.language("it")
    fg.load_extension("podcast")
    # https://podcasters.apple.com/support/1691-apple-podcasts-categories
    fg.podcast.itunes_category("News", "Politics")

    html_text = requests.get(PODCASTPAGE).text
    soup = BeautifulSoup(html_text, "html.parser")
    
    for recPage in soup.find("div", {"id": "ctl00_ContentPlaceHolder1_ctl00_SiscomRegistrazioni1_Panel1"}).find_all("a", href=True):
        # parse mp3 page
        url = BASEURL + recPage["href"]
        desc = recPage.text
        print(url)
        
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, "html.parser")
        # Ci possono essere più registrazioni per consiglio comunale
        recs = soup.find("div", {"id": "ctl00_ContentPlaceHolder1_ctl00_SiscomDettaglioRegistrazioni1_Panel1"}).findAll("a", href=True)
        
        for rec in recs:
            if rec is not None:
                fe = fg.add_entry()
                mp3 = rec["href"]
                if not mp3.startswith("http"):
                    mp3 = BASEURL + mp3
                title = rec.text
                dt = datetime.strptime(desc[desc.find("-")+2:] + " 21:00:00 +0100", "%d/%m/%Y %H:%M:%S %z")
                fe.id(mp3)
                fe.title(title)
                fe.description(title)
                fe.published(dt)
                fe.enclosure(mp3, 0, "audio/mpeg")

    fg.rss_str(pretty=True)
    fg.rss_file(PODCASTNAME)

if __name__ == "__main__":
    main()

