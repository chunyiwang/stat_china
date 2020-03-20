import requests
from bs4 import BeautifulSoup
import re
import urllib.request
import time
import csv


def get_request_years():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}
    page = requests.get("http://www.stats.gov.cn/tjsj/ndsj/", headers = headers)

    html = BeautifulSoup(page.content, 'html.parser')
    table = html.find('table', 'ztzw_tab')
    print(table)
    links = table.findAll('a')
    years_hrefs = []
    for link in links:
        years_hrefs.append(link['href'])

    print(years_hrefs)
    return years_hrefs




def get_data_for_year(year):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}
    left_link = re.sub('indexch', 'left', year)
    base_link = re.sub('indexch.htm', '', year)
    base_year = re.findall('\d+', base_link)[0]
    year_page = requests.get(left_link, headers=headers)
    year_html = BeautifulSoup(year_page.content)
    if len(year_html.findAll('ul', {'id': 'foldinglist'})) != 0:
        folding_lists = year_html.findAll('ul', {'id': 'foldinglist'})
    else:
        folding_lists = year_html.findAll('ul', {'id': re.compile('divOne_*')})


    for folding_list in folding_lists:
        li_lists = folding_list.findAll('li')

        for li_list in li_lists:
            file = li_list.find("a").get('href')
            name = li_list.find("a").text.strip()
            name = re.sub('\W+', '', name)
            print(file)

            if '.jpg' in file:
                retries = 3
                success = False
                while not success and retries >= 0:
                    if retries == 0:
                        raise Exception("cause of the problem, time out")

                    try:
                        urllib.request.urlretrieve(base_link + file,
                                                   'C:\\Users\\jocel\\OneDrive\\Desktop\\test\\' + base_year + name + '.jpg')
                        success = True
                    except Exception as e:
                        wait = retries * 30
                        time.sleep(wait)
                        retries -= 1
                        print(e)
            elif '简要说明' in name:
                pass
            elif '主要统计指标解释' in name:
                pass
            elif '.htm' in file:
                retries = 3
                success = False
                while not success and retries >= 0:
                    if retries == 0:
                        raise Exception("cause of the problem, time out")

                    try:
                        print(file)
                        print(base_link)
                        add = re.sub(r'\b.htm\b', '.xls', base_link + file)
                        print(add)
                        urllib.request.urlretrieve(add,
                                                   'C:\\Users\\jocel\\OneDrive\\Desktop\\test\\' + base_year + name + '.xls')

                        success = True
                    except Exception as e:
                        wait = retries * 30
                        time.sleep(wait)
                        retries -= 1
                        print(e)


            else:
                raise Exception("cause of the problem")

def flow():
    years_hrefs = get_request_years()
    for year_href in years_hrefs:
        print(year_href)
        get_data_for_year(year_href)



if __name__== "__main__":
  flow()
