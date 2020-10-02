from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

from bs4 import BeautifulSoup
import json
import sys

config_dict = {}
with open('config.json') as file:
    config_dict = json.load(file)

ID = config_dict["ID"]
PW = config_dict["PW"]


def dict2jsonfile(dict, filename):
    file = open(filename, 'w')
    json.dump(dict, file, ensure_ascii=False, indent=4)
    file.close()


def get_html_from_labpage():
    URL = 'https://www.mlab.im.dendai.ac.jp/bthesis2021/StudentDeploy.jsp'

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
    driver.get(URL)

    driver.find_element_by_name('id').send_keys(ID)
    driver.find_element_by_name('code').send_keys(PW)
    driver.find_element_by_css_selector('input[type="submit"]').click()

    page_source = driver.page_source

    return page_source


def get_student_lab_dict(page_source):
    student_lab_dict = {}

    soup = BeautifulSoup(page_source, 'html.parser')
    rows = soup.select(".entry_table tbody tr:nth-of-type(n+2)")

    for row in rows:
        student_id = row.select_one('td:nth-child(1)').get_text()
        lab = row.select_one('td:nth-child(3)').get_text().strip()
        student_lab_dict[student_id] = lab
    return student_lab_dict


def get_num_lab_dict(page_source):
    num_lab_dict = {}

    soup = BeautifulSoup(page_source, 'html.parser')
    rows = soup.select(".remain_table tr:nth-of-type(n+2)")

    for row in rows:
        professor_name = row.select_one('td:nth-child(1)').get_text()
        member_num = int(row.select_one('td:nth-child(3)').get_text())
        num_lab_dict[professor_name] = member_num

    return num_lab_dict


def get_str_numjson_diff(before_dict, after_dict):
    cnt = 0
    ret_str = ""
    for key in before_dict.keys():
        numdiff = after_dict[key] - before_dict[key]
        if numdiff > 0:
            cnt += 1
            ret_str += key+"研の希望人数が" + str(numdiff) + "人増えました\n"
            ret_str += "[Before]" + str(before_dict[key]) + \
                "人→ [After]" + str(after_dict[key]) + "人\n"

        elif numdiff < 0:
            cnt += 1
            ret_str += key + "研の希望人数が" + str(-numdiff) + "人減りました\n"
            ret_str += "[Before]" + str(before_dict[key]) + \
                "人→ [After]" + str(after_dict[key]) + "人\n"

    if cnt == 0:
        ret_str = "希望人数に差異はありませんでした"
    return ret_str


if __name__ == "__main__":
    page_source = ""
    if len(sys.argv) < 2:
        page_source = get_html_from_labpage()
        with open('index.html', 'w') as file:
            file.write(page_source)
    else:
        with open(sys.argv[1]) as file:
            page_source = file.read()

    student_lab_dict = get_student_lab_dict(page_source)
    num_lab_dict = get_num_lab_dict(page_source)

    before_num_lab_dict = {}
    with open('num_lab.json') as file:
        before_num_lab_dict = json.load(file)

    print(get_str_numjson_diff(before_num_lab_dict, num_lab_dict))
    dict2jsonfile(student_lab_dict, 'student_lab.json')
    dict2jsonfile(num_lab_dict, 'num_lab.json')
