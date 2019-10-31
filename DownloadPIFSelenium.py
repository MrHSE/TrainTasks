from selenium import webdriver as sel
from selenium.webdriver.common.keys import Keys
import requests as rq
from bs4 import BeautifulSoup as bs
from datetime import datetime
import csv


def get_html(url):
    r = rq.get(url) # verify=False
    return r.text

def get_last_link(html):
    soup = bs(html, 'lxml')
    pages = soup.find('ul', {'class': 'paging indent_top_30'}).find_all('a', class_='js_pagination item')[-1].get('href')
    last_page = pages.split('&')[-1].split('=')[-1]

    return int(last_page)

def get_all_links(html):
    print('Получаем список ссылок...')
    soup = bs(html, 'lxml')
    a_s = soup.find('div', {'class': 'long_table indent_top_20 js_fixed_table js_names_table'}).find('table', {
        'class': 'table table_data fixed js_form_parent js_fixed'}).find('tbody').find_all('a', href=True)
    links = []

    for a_ in a_s:
        a = a_.get('href')
        link = 'https://investfunds.ru' + a
        links.append(link)

    return links

def main():
    url = 'https://investfunds.ru/funds/?qual=on&showID=82&stat=0-3m&type=0-2&cat=0-a&obj=0-cuu&sortId=82&limit=50&page=1'
    base_link = 'https://investfunds.ru/funds/?qual=on&showID=82&stat=0-3m&type=0-2&cat=0-a&obj=0-cuu&sortId=82&limit=50&'
    page_part = 'page='
    last_page = get_last_link(get_html(url)) + 1
    links = []
    missed_links = []
    for i in range(1, last_page):
        gen_url = base_link + page_part + str(i)
        links.append(gen_url)
    all_page_links = []
    for link in links:
        all_page_links += get_all_links(get_html(link))
    browser = sel.Firefox()
    date_start1 = datetime.now()
    browser.implicitly_wait(0.5)
    z = 0
    for urls in all_page_links:
        browser.get(urls)
        html_elem = browser.find_element_by_tag_name('html')
        try:
            z += 1
            print("Скачиваем ссылку № " + str(z))
            # links_local = browser.find_elements_by_tag_name('a')
            links_local = browser.find_element_by_xpath("//*[@class='left item js_tab_item js_load_excel']")
            links_local.click() # [56]
            date_start = browser.find_element_by_id('date_start')
            browser.execute_script("window.scrollTo(0, 500)")
            for q in range(10):
                date_start.send_keys(Keys.BACK_SPACE)
            date_start.send_keys('01.01.1991')
            inputs = browser.find_elements_by_xpath("//*[@type='submit']")
            inputs[2].click()
        except:
            missed_links.append(urls)
    date_end = datetime.now()
    print('Итоговое время скачки файлов: ' + str(date_end - date_start1))
    print('Пропущено ' + str(len(missed_links)) + ' ссылок')
    with open('Missed links', 'wb') as result_missed_data:
        wr = csv.writer(result_missed_data, dialect='excel')
        wr.writerows(missed_links)
    browser.quit()
main()
