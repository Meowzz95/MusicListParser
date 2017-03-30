from selenium import webdriver
from bs4 import BeautifulSoup
import time
from Song import Song
from QQMusicImporter import Importer

url="http://music.163.com/#/playlist?id=23348698&userid=32116377"
#url="http://music.163.com/#/m/playlist?id=125879190"

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

songList=[]
for index,tr in enumerate(trs):
    tds=tr.find_all("td")
    if(len(tds)>0):
        name=tds[1].text.replace("MV","")
        length=tds[2].text.replace("分享","")
        singer=tds[3].text
        album=tds[4].text

        songList.append(Song(name=name,length=length,singer=singer,album=album))

driver.quit()

for songIndex,song in enumerate(songList):
    print("---"+str(songIndex+1)+"---")
    print(song)

songList.reverse()
importer=Importer(songList)
importer.start()



