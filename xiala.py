#!coding:utf-8
from selenium import webdriver
import time
import pandas as pd
from pandas import DataFrame
from selenium.webdriver.chrome.options import Options


class XialaSpider(object):
    driver_path = r"chromedriver.exe"

    def __init__(self):
        #创建chrome配置
        self.chrome_options = Options()
        self.chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(executable_path=XialaSpider.driver_path,chrome_options=self.chrome_options)
        self.url = "http://zhidao.baidu.com/business/profile?id=87701"


    def run(self):
        self.driver.get(self.url)
        time.sleep(2)
        self.get_down()
    

    def get_down(self):
        #将滚动条移动到页面的底部
        all_window_height = []
        all_window_height.append(self.driver.execute_script("return document.body.scrollHeight;"))
        while True:

            self.driver.execute_script("scroll(0,100000)")
            time.sleep(4)
            check_height = self.driver.execute_script("return document.body.scrollHeight;")
            if check_height == all_window_height[-1]:  
                print(">>>>>>>>已经下拉至底部,即将解析页面....")
                break
            else:
                all_window_height.append(check_height) 
                print(">>>>>>>>正在执行下拉操作......")
        self.parse_content_page()

    def parse_content_page(self):
        html = self.driver.page_source
        questions = self.driver.find_elements_by_xpath("//h2[@class='item-title']/a")
        #保存到xlsx中
        data = pd.read_excel('example.xlsx',sheet_name='Sheet1')
        row = 1
        for question in questions:
            data.loc[row,'问题'] = question.text
            row += 1
            # print(question.text)

        row = 1
        answers = self.driver.find_elements_by_xpath("//div[@class='item-right']/p")
        for answer in answers:
            data.loc[row,'答案'] = answer.text
            row += 1
            # print(answer.text)
        DataFrame(data).to_excel('test.xlsx',sheet_name='Sheet1')
        #保存成网页
        with open("index.html","wb") as f:
            f.write(html.encode())
        f.close()
        self.driver.quit()	
       
		










if __name__ == "__main__":

    spider = XialaSpider()
    spider.run()
