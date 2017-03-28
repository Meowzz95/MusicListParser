

from selenium import webdriver
from bs4 import BeautifulSoup
import time

url="http://music.163.com/#/playlist?id=23348698&userid=32116377"

driver = webdriver.Chrome()
driver.get(url)
time.sleep(3)
driver.switch_to.frame("g_iframe")
# time.sleep(3)
songListTable=driver.find_element_by_class_name("j-flag").get_attribute("innerHTML")
#print(songListTable)

bsFile=BeautifulSoup(songListTable,"html.parser")
#print(bsFile.prettify())
trs=bsFile.find_all("tr")

for index,tr in enumerate(trs):
    print("---"+str(index)+"---")
    #print(tr)
    tds=tr.find_all("td")
    if(len(tds)>0):
        print("***TITLE***"+tds[1].text)
        print("***LENGTH***"+tds[2].text)
        print("***ARTIEST***"+tds[3].text)
        print("***ALBUM***"+tds[4].text)
    print("------")





# driver.set_script_timeout(3)
# bodies = driver.execute_async_script("var result= document.documentElement.outerHTML;arguments[0](result)")
# print(bodies)