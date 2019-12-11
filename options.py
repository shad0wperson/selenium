from selenium.webdriver.chrome.options import Options

#创建chrome浏览器驱动，无头模式
chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)


#禁止弹窗，妨碍点击操作
prefs = {'profile.default_content_setting_values':{'notifications':2}}
chrome_options.add_experimental_option('prefs',prefs)

#设置浏览器为开发者模式，绕过windows.navigator.webdriver=Ture检测
chrome_options.add_experimental_option('excludeSwitches',['enable-automation'])

#开启无图模式
prefs = {'profile.default_content_setting_values':{'images':2}}
chrome_options.add_experimental_option('prefs',prefs)
