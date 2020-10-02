from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

from bs4 import BeautifulSoup
import scrape
from scrape import dict2jsonfile, get_html_from_labpage, get_num_lab_dict
import json

print("student_id?")
print('->', end='')
ID = input()

print("student_pw?")
print('->', end='')
PW = input()

print("discord_channel_id?")
print("->", end='')

DISCORD_CHANNEL_ID = int(input())

print("discord_token?")
print("->", end='')

DISCORD_TOKEN = input()

config_dict = {
    "ID": ID,
    "PW": PW,
    "DISCORD_CHANNEL_ID": DISCORD_CHANNEL_ID,
    "DISCORD_TOKEN": DISCORD_TOKEN
}

dict2jsonfile(config_dict, 'config.json')

print("Success for generating config.json")

print("generating num_lab.json ...")

URL = 'https://www.mlab.im.dendai.ac.jp/bthesis2021/StudentDeploy.jsp'

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
driver.get(URL)

driver.find_element_by_name('id').send_keys(ID)
driver.find_element_by_name('code').send_keys(PW)
driver.find_element_by_css_selector('input[type="submit"]').click()

page_source = driver.page_source

num_lab_dict = get_num_lab_dict(page_source)

dict2jsonfile(num_lab_dict, 'num_lab.json')
