#!coding:utf-8
from selenium import webdriver
from lxml import etree
import time
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LagouSpider(object):
    driver_path = r"f://chromedriver.exe"
    def __init__(self):
        #创建chrome配置
        self.chrome_options = Options()
        #设置浏览器为开发者模式，绕过windows.navigator.webdriver=Ture检测
        self.chrome_options.add_experimental_option('excludeSwitches',['enable-automation'])
        #禁止弹窗，妨碍点击操作
        self.prefs = {'profile.default_content_setting_values':{'notifications':2}}
        self.chrome_options.add_experimental_option('prefs',self.prefs)
        #无界面展示
        self.chrome_options.add_argument('--headless')
        self.chrome_options.set_headless(headless=True)
        #开启无图模式
        self.prefs = {'profile.default_content_setting_values':{'images':2}}
        self.chrome_options.add_experimental_option('prefs',self.prefs)
        self.driver = webdriver.Chrome(executable_path=LagouSpider.driver_path,options=self.chrome_options)
        self.url = 'http://www.lagou.com/jobs/list_python/p-city_198?&cl=false&fromSearch=true&labelWords=&suginput='
        self.positions = []
        
        
        
    def run(self):
        self.driver.get(self.url)
        while True:

            
            source = self.driver.page_source
            time.sleep(3)
            
            
            ad_btn = self.driver.find_element_by_xpath("//div[@class='body-btn']")
            ad_btn.click()
            

            self.parse_list_page(source)
            # WebDriverWait(driver=self.driver,timeout=10).until(EC.presence_of_element_located((By.XPATH,
            # "//div[@class='pager_container']/span[last()]")))

            next_btn = self.driver.find_element_by_xpath("//div[@class='pager_container']/span[last()]")
            if "pager_next_disabled" in next_btn.get_attribute("class"):
                break
            
            next_btn.click()
            time.sleep(1)


    def parse_list_page(self,source):
        html = etree.HTML(source)
        links = html.xpath("//a[@class='position_link']/@href")
        for link in links:
            self.request_detail_page(link)
            time.sleep(1)


    def request_detail_page(self,url):
        # self.driver.get(url)
        
        self.driver.execute_script("window.open('%s')" % url)
        self.driver.switch_to.window(self.driver.window_handles[1])
        WebDriverWait(self.driver,timeout=10).until(EC.presence_of_element_located((By.XPATH,
        "//h1[@class='name']"))
        )
        source = self.driver.page_source
        self.parse_detail_page(source)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])


    def parse_detail_page(self,source):
        
        html = etree.HTML(source)
        position_name = html.xpath("//h1[@class='name']/text()")[0]
        job_request_span = html.xpath("//dd[@class='job_request']//span")
        salary = job_request_span[0].xpath(".//text()")[0].strip()
        city = job_request_span[1].xpath(".//text()")[0].strip()
        city = re.sub(r"[\s/]","",city)
        experience = job_request_span[2].xpath(".//text()")[0].strip()
        experience = re.sub(r"[\s/]","",experience)
        education = job_request_span[3].xpath(".//text()")[0].strip()
        education = re.sub(r"[\s/]","",education)
        des = "".join(html.xpath("//dd[@class='job_bt']//text()")).strip()
        position = {
            'name':position_name,
            'salary':salary,
            'city':city,
            'experience':experience,
            'education':education,
            'description':des
        }
        self.positions.append(position)
        print(position)
        print('='*40)






if __name__ == "__main__":
    spider = LagouSpider()
    spider.run()
