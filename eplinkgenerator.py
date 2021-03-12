# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import json
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests


class webdriversrapconn:
    def conn(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(
            r"C:\Users\KITTU7410\Desktop\chromedriver_win32\chromedriver", options=options)
        return self.driver

    def quit(self):
        self.driver.quit()
# driver.maximize_window()


class animix():
    def __init__(self):
        d = webdriversrapconn()
        self.webd = d.conn()

    def contentlink(self, url):
        self.webd.get(url)
        self.webd.find_element_by_class_name("plyr__control").click()
        self.webd.find_element_by_class_name("plyr__control").click()
        v = self.webd.find_element_by_tag_name("source")
        # print(v.get_attribute('src'))
        cl = v.get_attribute('src')
        return cl

    def search(self, search):
        self.webd.get(f'https://animixplay.to/?q={search}')
        time.sleep(2)
        res = self.webd.find_elements_by_tag_name("li")
        img, name, release = [], [], []
        try:
            for i in res:
                div = i.find_element_by_tag_name("div")
                imglink = div.find_element_by_tag_name("a")
                l = imglink.find_element_by_tag_name("img")
                img.append(l.get_attribute("src"))
                anname = i.find_elements_by_tag_name("p")[0]
                rel = i.find_elements_by_tag_name("p")[1]
                name.append(anname.get_attribute("innerText"))
                release.append(rel.get_attribute("innerText"))
        except Exception:
            print(img, name, release)
        # div=res.find_element_by_tag_name("div")
        # imglink=div.find_element_by_tag_name("a")
        # l=imglink.find_element_by_tag_name("img")
        # print(l.get_attribute("src"))
        # print(img,name,release)

    # search()

    def getiframepage(self, epname, epnum):
        epname = epname.replace(' ', '-')
        self.webd.get(f'https://animixplay.to/v1/{epname}/ep{epnum}')
        time.sleep(1)
        res = self.webd.find_element_by_tag_name("iframe")
        # print(res.get_attribute("src"))
        l = self.contentlink(res.get_attribute("src"))
        return l


# https://stackoverflow.com/questions/46920243/how-to-configure-chromedriver-to-initiate-chrome-browser-in-headless-mode-throug


class gogoscrap:
    def search(self, anime):
        page = requests.get(
            f'https://ww.gogoanimes.org//search?keyword={anime}')
        soup = BeautifulSoup(page.content, 'html.parser')
        img = soup.find_all('div', {'class': 'img'})
        # a = soup.find_all('a')
        name = soup.find_all('p', {'class': 'name'})
        rel = soup.find_all('p', {'class': 'released'})
        # links = []
        # release = []
        # animename = []
        # thumimgs = []
        testjson = []
        for i in range(len(img)):
            # links.append(img[i].a['href'])
            # thumimgs.append(img[i].a.img['src'])
            # release.append(rel[i].getText().replace(' ', '').replace('\n', ''))
            # animename.append(name[i].getText())
            testjson.append({"anime": name[i].getText(), "link": img[i].a['href'], "thubnail": img[i].a.img['src'],
                             "release": rel[i].getText().replace(' ', '').replace('\n', '')})
        # print(links, "\n", animename, "\n", release)
        # print(json.dumps(testjson))
        return json.dumps(testjson)

    def getanimeinfo(self, animeurlname):
        filteruri = animeurlname.replace(' ', '')
        page = requests.get(
            f'https://ww.gogoanimes.org//category/{filteruri}')
        animeinfosoup = BeautifulSoup(page.content, 'html.parser')
        animeinfo = []
        reps = []
        # print(reps)
        for ep in animeinfosoup.find_all('a', {'href': '#'}):
            reps.append(ep.text)
        # for eps in reps:
        ind = reps[-1].index("-")
        epcountreps = reps[-1][ind+1:].replace(" ", "")
        # print(str(reps))

        for i in animeinfosoup.find_all('p', {'class': 'type'}):
            animeinfo.append(i.text.replace("\n", ""))
        # epcount = animeinfosoup.find_all('ul', {'id': 'episode_page'})
        # epcount2 = animeinfosoup.find_all('a', {'ep_start': '1'})
        # animeinfo.append(f"epcount:{epcount2[0].text.replace(' ', '')}")
        # for s in animeinfo[2]:

        tjson = []
        # print(animeinfo)
        tjson.append({"type": animeinfo[0][5:], "plot": animeinfo[1][13:], "genre": animeinfo[2][6:].replace(
            '  ', ''), "released": animeinfo[3], "episodes-released": epcountreps})
        return json.dumps(tjson)
