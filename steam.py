import requests
from bs4 import BeautifulSoup
import re
import csv


def write_csv(d):
    with open('steam.csv', 'a') as f:
        order = ['title', 'release', 'view', 'tag_str']
        write = csv.DictWriter(f, fieldnames=order)
        write.writerow(d)


def get_html(url):
    r = requests.get(url)    # response

    if not r.ok:    # status 200
        print(f'Code: {r.status_code}, url: {url}')
    return r.text


def get_link(html):
    soup = BeautifulSoup(html, 'lxml')

    patern = r'^https://store.steampowered.com/app/'    # '^' - begin string
    tags_a = soup.find_all('a', href=re.compile(patern))
    return tags_a


def popup_data(id):    # get links with new id
        url_popup = f'https://store.steampowered.com/apphoverpublic/{id}'
        html = get_html(url_popup)
        soup = BeautifulSoup(html, 'lxml')
        try:
            title = soup.find('h4', class_='hover_title').text.strip()
        except:
            title = ''
            print(url_popup)

        try:
            release = soup.find('div', class_='hover_release').span.text.split(':')[-1].strip()
            # Released: 30 Apr, 2018
        except:
            release = ''
            print(url_popup)

        try:
            review = soup.find('div', class_='hover_review_summary').text
            # Very Positive (179,858 reviews)
        except:
            view = ''
            print(url_popup)
        else:
            patern = r'\d+'
            view = int(''.join(re.findall(patern, review)))

        try:
            tags = soup.find_all('div', class_='app_tag')
        except:
            tag_str = ''
            print(url_popup)
        else:
            tag_list = [tag.text for tag in tags]
            tag_str = ', '.join(tag_list)

        data = {'title': title,
                'release': release,
                'view': view,
                'tag_str': tag_str}

        write_csv(data)



def main():
  
    tags_a_all = []
    start = 0
    url_loadpage = f'https://store.steampowered.com/search/results/?query&start={start}&count=100&tags=1702'

    while True:

        links_a = get_link(get_html(url_loadpage))
        
        if links_a:
            tags_a_all.extend(links_a)
            start += 100
            url_loadpage = f'https://store.steampowered.com/search/results/?query&start={start}&count=100&tags=1702'
        else:
            break    
    
    for link in tags_a_all:    # get ids with links
        id = link.get('data-ds-appid')
        popup_data(id)


if __name__ == "__main__":
    main()