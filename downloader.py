import requests, bs4

randURL = "http://gatherer.wizards.com/Pages/Card/Details.aspx?action=random"

class Card(object):
    
    def __init__(self, url = randURL):
        res = requests.get(url)
        res.raise_for_status()
        self.soup = bs4.BeautifulSoup(res.text, 'lxml')
        self.title = self.soup.select('div[class="contentTitle"]')[0].text.strip()
        self.imgurl = "http://gatherer.wizards.com/" + \
        self.soup.select('img[id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cardImage"]')[0].get('src').strip("../../")
        colors = set()
        manarow = self.soup.select('div[id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_manaRow"]')
        manaimgs = manarow[0].select('img[alt]')
        for m in manaimgs:
            trial = m.get('alt').lower()
            if trial.isdigit() == False:
                colors.add(trial)
        self.colors = list(colors)
    
    def download(self, dest = None):
        if dest is None:
            dest = self.title.replace(" ","") + ".jpg"
        res = requests.get(self.imgurl)
        res.raise_for_status()
        savefile = open(dest, 'wb')
        for chunk in res:
            savefile.write(chunk)
        savefile.close()