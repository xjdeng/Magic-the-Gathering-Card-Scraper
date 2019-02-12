import requests, bs4

randURL = "http://gatherer.wizards.com/Pages/Card/Details.aspx?action=random"

class Card(object):
    
    def __init__(self, url = randURL):
        res = requests.get(url)
        res.raise_for_status()
        self.soup = bs4.BeautifulSoup(res.text, 'lxml')
        self.title = self.soup.select('div[class="contentTitle"]')[0].text.strip()