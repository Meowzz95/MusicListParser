import time
from selenium import webdriver
from bs4 import BeautifulSoup

class Importer(object):
    searchUrl = "https://y.qq.com/portal/search.html?w="
    songList=[]
    def __init__(self,songList):
        self.songList=songList
        options = webdriver.ChromeOptions()
        options.add_argument("user-data-dir=C:\\Users\\jjzzz\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
        self.driver = webdriver.Chrome(chrome_options=options)

    def start(self):
        for song in self.songList:
            link=self.parse_link(song)
            skipped=self.favorite(link)
            if skipped:
                print("[SKIPPED]"+song.name)
            else:
                print("[ADDED]"+song.name)
        self.driver.quit()


    def parse_link(self,song):
        url=self.searchUrl+song.name+" "+song.singer
        self.driver.get(url)
        time.sleep(2)
        searchResultTableHtml = self.driver.find_element_by_id("song_box").get_attribute("outerHTML")

        bs = BeautifulSoup(searchResultTableHtml, "html.parser")
        # the UL containing all the search results, there should be only one UL found
        songListUls = bs.find_all("ul", attrs={"class": "songlist__list"})
        # each li represents one song
        songLis = songListUls[0].find_all("li")
        # take first one and get the song page url
        songAs = songLis[0].find_all("a")
        songLink = songAs[0].get('href')

        return songLink

    def favorite(self, link,skipExist=True):
        # open another page to get song details
        self.driver.get(link)
        time.sleep(2)
        elementFavorite=self.driver.find_element_by_css_selector("a.mod_btn.js_all_like")

        skipped=False

        if skipExist:
            if "已收藏" in elementFavorite.text:
                skipped=True

        if not skipped:
            elementFavorite.click()

        time.sleep(1)
        return skipped





