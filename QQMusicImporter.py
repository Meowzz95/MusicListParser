import time
from selenium import webdriver
from bs4 import BeautifulSoup


searchUrl="https://y.qq.com/portal/search.html?w="
keyword="动物世界"

url=searchUrl+keyword


options=webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\\jjzzz\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
driver=webdriver.Chrome(chrome_options=options)
driver.get(url)
time.sleep(2)
searchResultTableHtml=driver.find_element_by_id("song_box").get_attribute("outerHTML")

bs=BeautifulSoup(searchResultTableHtml,"html.parser")
#the UL containing all the search results, there should be only one UL found
songListUls=bs.find_all("ul",attrs={"class":"songlist__list"})
#each li represents one song
songLis=songListUls[0].find_all("li")
#take first one and get the song page url
songAs=songLis[0].find_all("a")
songLink=songAs[0].get('href')


#open another page to get song details
driver.get(songLink)
time.sleep(2)
driver.find_element_by_css_selector("a.mod_btn.js_all_like").click()



#driver.quit()
