# from seleniumrequests import Firefox
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from statistics import mean 
import xlsxwriter
import time 
import pandas as pd
import pickle
dt = datetime.now()
outWorkbook = xlsxwriter.Workbook("data.xlsx")
outSheet = outWorkbook.add_worksheet()
outSheet.write("A1","url")
outSheet.write("B1","display url")
outSheet.write("C1","likes Count")
outSheet.write("D1","username")
outSheet.write("E1","Caption")
outSheet.write("F1","timestamp")
class Main:
    ur=""
    usn = ""
    cap = ""
    def __init__(self,urx):
        self.ur = urx
        self.options = Options()
        # self.options.add_argument("--auto-open-devtools-for-tabs")
        self.options.add_argument("--start-maximized")  
        self.options.add_argument("user-data-dir=C:\chromeprofile2")
        # self.options.add_argument('--headless')
        # self.options.add_argument('--disable-gpu')
        # self.driver = uc.Chrome(options=self.options)
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options) 
        self.actions = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 30)
    def getPost(self,pLink,count):
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(pLink)
        try:
            caption = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]/h1")))
            usrname = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[1]/div/div/div/div/div/a")))
            self.usn = usrname.text
            self.cap = caption.text
        except Exception as e:
            print(e)
        try:
            likec = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div/div/a/div/span")))
            outSheet.write(count+1,2,likec.text)
        except Exception as e:
            print(e)
            outSheet.write(count+1,2,"None")
        try:    
            print("try1")
            img = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[1]/div/div/div/div[1]/img")))
            # print(img.get_attribute('src'))
            outSheet.write(count+1,1,img.get_attribute('src'))
        except Exception as e:
            print(e)
            print("exception 2")
            imgs = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='_aagv']")))
            print(imgs.get_attribute('src'))
            outSheet.write(count+1,1,imgs.get_attribute('src'))
        
        outSheet.write(count+1,0,pLink)
        outSheet.write(count+1,3,self.usn)
        outSheet.write(count+1,4,self.cap)
        dtm = datetime.timestamp(dt)
        stmp = datetime.fromtimestamp(dtm)
        outSheet.write(count+1,5,str(stmp))
        self.driver.execute_script("window.close('');")
        self.driver.switch_to.window(self.driver.window_handles[0])
    def getHashtag(self,link):
        self.driver.get(link)
        # sup = BeautifulSoup(self.driver.page_source, 'html.parser')
        # lnks = sup.find_all()
        x = 0
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/article/div[2]/div/div[1]/div[1]/a"))).click()
        for x in range(1,50):
            url = self.driver.current_url
            print(url)
            self.driver.execute_script("window.open('');")
            self.getPost(url,x)
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div[2]/button"))).click()
            
mn = Main("B08TVDWM9W")
mn.getHashtag("https://www.instagram.com/explore/tags/memekomikindonesia/")
outWorkbook.close()
