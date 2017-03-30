import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchWindowException


class Importer(object):
    searchUrl = "https://y.qq.com/portal/search.html?w="
    songList = []

    def __init__(self, songList):
        self.songList = songList
        options = webdriver.ChromeOptions()
        options.add_argument("user-data-dir=C:\\Users\\jjzzz\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
        self.driver = webdriver.Chrome(chrome_options=options)

    def start(self):
        failList = []
        successCount = 0
        for song in self.songList:
            link = self.parse_link(song)
            skipped, info = self.favorite(link)
            if skipped:
                print("[SKIPPED]" + song.name)
                if info:
                    print("  [Reason]" + info)
                    failList.append(song)

            else:
                print("[ADDED]" + song.name)
                successCount += 1

        print(failList, sep="\n")
        print("---FINISH---")
        print("Total processed:" + str(len(self.songList)))
        print("Success:" + str(successCount))
        print("Failure:" + str(len(failList)))
        print("Failure list is shown above")
        self.driver.quit()

    def parse_link(self, song):
        url = self.searchUrl + song.name + " " + song.singer
        self.driver.get(url)
        # initialize songLink as a invalid result page
        # so if no result is found, the invalid page will be redirected to
        songLink = self.searchUrl

        while True:
            time.sleep(2)
            searchResultTableHtml = self.driver.find_element_by_id("song_box").get_attribute("outerHTML")

            bs = BeautifulSoup(searchResultTableHtml, "html.parser")
            # the UL containing all the search results, there should be only one UL found
            songListUls = bs.find_all("ul", attrs={"class": "songlist__list"})
            if len(songListUls) == 0:
                # if there's no Ul found, it's possible that this song is not available
                # so we check if there's "no result" message
                divNoResult = self.driver.find_element_by_class_name("mod_search_none")

                if "暂时没有找到" in divNoResult.text:
                    print("[ERROR] $" + song.name + "$ No such song is available, skipping...")
                    break

                #if there's no "no result" message, the reason is likely to be caused by a slow network, just retry
                print("[ERROR] $" + song.name + "$ Result list not found(may due to low network speed), try again...")
                continue
            # each li represents one song
            songLis = songListUls[0].find_all("li")
            # take first one and get the song page url
            songAs = songLis[0].find_all("a")
            songLink = songAs[0].get('href')
            break

        return songLink

    def favorite(self, link, skipExist=True):
        info = None
        # open another page to get song details
        self.driver.get(link)
        time.sleep(2)
        try:
            elementFavorite = self.driver.find_element_by_css_selector("a.mod_btn.js_all_like")
        except:
            # if the page does not contain the favorite button, return true(meaning this song is skipped)
            info = "Fail to find favorite button, skipping..."
            return True, info

        skipped = False

        if skipExist:
            if "已收藏" in elementFavorite.text:
                skipped = True

        if not skipped:
            elementFavorite.click()

        time.sleep(1)
        return skipped, info
