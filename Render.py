from selenium import webdriver
from bs4 import BeautifulSoup
import time

url="http://music.163.com/#/playlist?id=23348698&userid=32116377"

driver = webdriver.Chrome()
driver.get(url)
time.sleep(3)
#must switch to the i frame which contains the song list table
driver.switch_to.frame("g_iframe")
#dk why searching for this works, but printing out the whole i frame dom does not work
songListTable=driver.find_element_by_class_name("j-flag").get_attribute("innerHTML")

#parse using bs4
bsFile=BeautifulSoup(songListTable,"html.parser")

#get all rows , each is one song
trs=bsFile.find_all("tr")

for index,tr in enumerate(trs):
    print("---"+str(index)+"---")
    #print(tr)
    tds=tr.find_all("td")
    if(len(tds)>0):
        print("***TITLE***"+tds[1].text.replace("MV",""))
        print("***LENGTH***"+tds[2].text.replace("分享",""))
        print("***ARTIEST***"+tds[3].text)
        print("***ALBUM***"+tds[4].text)
    print("------")




