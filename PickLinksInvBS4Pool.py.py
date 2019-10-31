from bs4 import BeautifulSoup as bs
from multiprocessing import Pool
from datetime import datetime
import requests as rq, csv


def get_html(url):
    r = rq.get(url) # verify=False
    return r.text

def get_last_link(html):
    soup = bs(html, 'lxml')
    pages = soup.find('ul', class_='paging indent_top_30').find_all('a', class_='js_pagination item')[-1].get('href')
    last_page = pages.split('&')[-1].split('=')[-1]

    return int(last_page)

def get_all_links(html):
    print('Получаем список ссылок...')
    soup = bs(html, 'lxml')
    a_s = soup.find('div', class_='long_table indent_top_20 js_fixed_table js_names_table').find('table',
                                                                                                 class_='table table_data fixed js_form_parent js_fixed').find(
        'tbody').find_all('a', href=True)
    links = []

    for a_ in a_s:
        a = a_.get('href')
        link = 'https://investfunds.ru' + a
        links.append(link)

    return links

def get_page_data(html):
    soup = bs(html, 'lxml')

    try:
        name = soup.find('h1', class_='widget_info_ttl').text.strip()
    except:
        name = ''

    try:
        current_price = soup.find('div', class_='roll_table full js_roll_table').find('tbody').find('td',class_='nowrap main').find_next_sibling('td').text.strip()
    except:
        current_price = ''

    try:
        net_asset_value = soup.find('div', class_='roll_table full js_roll_table').find('tbody').tr.find_next_sibling('tr').find('b').text.strip()
    except:
        net_asset_value = ''

    try:
        P1PR = soup.find('div', class_='roll_table full js_roll_table').find('tbody').find('td', class_='nowrap').find_next_sibling('td').find_next_sibling('td').find_next_sibling('td').find_next_sibling('td').find_next_sibling('td').text.strip()
    except:
        P1PR = ''

    try:
        register_date = soup.find('div', class_='widget_list wdg_step').find('ul', class_='param_list').find('li').find_next_sibling('li').find_next_sibling('li').find('div', class_='value').text.strip()
    except:
        name = ''

    data = {'Name': name,
            'Current price': current_price,
            'Net asset value': net_asset_value,
            'P1PR': P1PR,
            'Register Date': register_date}
    return data

def write_csv(data):
    with open('PIF1.csv', 'a') as file:
        writer = csv.writer(file)

        writer.writerow((data['Name'],
                         data['Current price'],
                         data['Net asset value'],
                         data['P1PR'],
                         data['Register Date']))

        print(data['Name'] + ' parsed')

def make_all(links):
    all_page_links = get_all_links(get_html(links))
    for link in all_page_links:
        write_csv(get_page_data(get_html(link)))

def main():
    url = 'https://investfunds.ru/funds/?showID=99&cstm=0-2w7bbi6.1-2&stat=0-3u&type=0-2&cat=0-a&limit=50&page=1'
    base_link = 'https://investfunds.ru/funds/?showID=99&cstm=0-2w7bbi6.1-2&stat=0-3u&type=0-2&cat=0-a&limit=50&'
    page_part = 'page='
    links = []
    start = datetime.now()
    last_page = get_last_link(get_html(url)) + 1
    for i in range(1, last_page):
        gen_url = base_link + page_part + str(i)
        links.append(gen_url)

    with Pool(20) as p:
        p.map(make_all, links)
    end = datetime.now()
    print('Итоговое время выполнения скрипта: ' + str(end - start))

if __name__ == '__main__':
    main()
