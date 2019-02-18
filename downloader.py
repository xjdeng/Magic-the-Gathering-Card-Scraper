import requests, bs4, cv2, tempfile
import numpy as np

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
    
    def download_image(self, dest = None):
        if dest is None:
            dest = self.title.replace(" ","") + ".jpg"
        tempdir = tempfile.TemporaryDirectory()
        tempdest = tempdir.name + "/" + self.title.replace(" ","") + ".jpg"
        self.download(tempdest)
        img = cv2.imread(tempdest)
        h,w,_ = img.shape
        left = round(0.09*w)
        top = round(0.125*h)
        right = round(0.905*w)
        bottom = round(0.5484*h)
        newimg = np.zeros((bottom - top, right - left, 3))
        for i in range(left, right):
            for j in range(top, bottom):
                newimg[j-top, i-left, :] = img[j, i, :]
        cv2.imwrite(dest, newimg)
        tempdir.cleanup()