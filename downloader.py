import requests, bs4, cv2, tempfile
import numpy as np
from path import Path as path

randURL = "http://gatherer.wizards.com/Pages/Card/Details.aspx?action=random"

def download(folder, mincards = 500, min_per_folder = 100):
    path(folder).mkdir_p()
    path(folder + "/red").mkdir_p()
    path(folder + "/blue").mkdir_p()
    path(folder + "/black").mkdir_p()
    path(folder + "/green").mkdir_p()
    path(folder + "/white").mkdir_p()
    r,u,b,g,w = 0,0,0,0,0
    while((r+u+b+g+w < mincards) or (min(r,u,b,g,w) < min_per_folder)):
        try:
            card = Card()
            if len(card.colors) == 1:
                color = card.colors[0]
                dest = "{}/{}/{}".format(folder, color, card.generate_filename())
                if path(dest).exists() == False:
                    card.download_image(dest)
                    if color == "red":
                        r += 1
                    elif color == "blue":
                        u += 1
                    elif color == "black":
                        b += 1
                    elif color == "green":
                        g += 1
                    elif color == "white":
                        w += 1
        except Exception as e:
            print("Exception: {}, continuting".format(e))
                

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
            dest = self.generate_filename()
        res = requests.get(self.imgurl)
        res.raise_for_status()
        savefile = open(dest, 'wb')
        for chunk in res:
            savefile.write(chunk)
        savefile.close()
    
    def download_image(self, dest = None):
        if dest is None:
            dest = self.generate_filename()
        tempdir = tempfile.TemporaryDirectory()
        tempdest = tempdir.name + "/" + self.generate_filename()
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
    
    def generate_filename(self):
        return self.title.replace(" ","") + ".jpg"