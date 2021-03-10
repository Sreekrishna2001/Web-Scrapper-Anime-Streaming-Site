# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
options = Options()
options.headless = True
driver = webdriver.Chrome(
    r"C:\Users\KITTU\Desktop\chromedriver_win32\chromedriver", options=options)
# from selenium.webdriver.common.keys import Keys

# print("sample test case started")

# driver = webdriver.Chrome(executable_path=r"C:\Users\KITTU\Desktop\chromedriver_win32\chromedriver")


# driver.maximize_window()
def contentlink(url):
    driver.get(url)
    driver.find_element_by_class_name("plyr__control").click()
    driver.find_element_by_class_name("plyr__control").click()
    v = driver.find_element_by_tag_name("source")
    # print(v.get_attribute('src'))
    cl = v.get_attribute('src')
    return cl
# navigate to the url

# identify the Google search text box and enter the value
# driver.find_element_by_id("q").send_keys("naruto")
# time.sleep(1)
# driver.find_element_by_id("searchbutton").click()
# driver.find_elements_by_class_name("playbutton btn btn-primary")[0].click()

# time.sleep(3)

# click on the Google search button
# driver.find_element_by_name("btnK").send_keys(Keys.ENTER)
# time.sleep(3)

# time.sleep(1)
# driver.find_element_by_class_name("plyr__control").click()

# close the browser
# v = driver.find_element_by_tag_name("source")

# print(v.get_attribute('src'))
# driver.close()


def search():
    driver.get('https://animixplay.to/?q=naruto')
    time.sleep(2)
    res = driver.find_elements_by_tag_name("li")
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


def getiframepage(epname, epnum):
    epname = epname.replace(' ', '-')
    driver.get(f'https://animixplay.to/v1/{epname}/ep{epnum}')
    time.sleep(1)
    res = driver.find_element_by_tag_name("iframe")
    # print(res.get_attribute("src"))
    l = contentlink(res.get_attribute("src"))
    return l


def quit():
    driver.quit()

# getiframepage()

# print("sample test case successfully completed")


# def search():
#     driver.get('https://animixplay.to/?q=naruto')
#     res=driver.find_elements_by_class_name("img")
#     print(res)


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
        links = []
        release = []
        animename = []
        for i in range(len(img)):
            links.append(img[i].a['href'])
            release.append(rel[i].getText().replace(' ', '').replace('\n', ''))
            animename.append(name[i].getText())
        print(links, animename, release)
        return list(links, animename, release)

    def getanimeinfo(self, animeurlname):
        page = requests.get(
            f'https://ww.gogoanimes.org//category/{animeurlname}')
        animeinfosoup = BeautifulSoup(page.content, 'html.parser')
        animeinfo = []
        for i in animeinfosoup.find_all('p', {'class': 'type'}):
            animeinfo.append(i.text.replace("\n", ""))
        # epcount = animeinfosoup.find_all('ul', {'id': 'episode_page'})
        epcount2 = animeinfosoup.find_all('a', {'ep_start': '1'})
        animeinfo.append(f"epcount:{epcount2[0].text.replace(' ', '')}")
        return animeinfo
