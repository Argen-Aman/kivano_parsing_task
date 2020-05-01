import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')

    pages = soup.find('ul', class_='pagination pagination-sm').find_all('a')[-1].get('href')
    total_pages = pages.split('=')[1]

    return int(total_pages)


def write_csv(data):
    with open('kivano.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow( (data['Name of product'],
                          data['Price'],
                          data['Link to photo']) )


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    ads = soup.find('div', class_='list-view').find_all('div', class_='item product_listbox oh')

    for ad in ads:
        # title, price, link to photo
        try:
            title = ad.find('div', class_='pull-right rel').find('div', class_='product_text pull-left').find('div', class_='listbox_title oh').text.strip()
        except:
            title = ''

        try:
            price = ad.find('div', class_='motive_box pull-right').find('div', class_='listbox_price text-center').find('strong').text.strip()
        except:
            price = ''

        try:
            link = 'https://www.kivano.kg' + ad.find('div', class_='listbox_img pull-left').find('a').find('img').get('src')
        except:
            link = ''

        data = {'Name of product': title,
                'Price': price,
                'Link to photo': link}
        write_csv(data)


def main():
    url = 'https://www.kivano.kg/mobilnye-telefony?page=1'
    base_url = 'https://www.kivano.kg/mobilnye-telefony?'
    page_part = 'page='

    total_pages = get_total_pages(get_html(url))

    for i in range(1, total_pages + 1):
        url_gen = base_url + page_part + str(i)
        # print(url_gen)
        html = get_html(url_gen)
        get_page_data(html)

if __name__ == '__main__':
    main()