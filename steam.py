import requests
from bs4 import BeautifulSoup
from time import sleep



def get_html(url):
    r = requests.get(url)    # response

    if not r.ok:    # status 200
        print(f'Code: {r.status_code}, url: {url}')
    return r.text


def main():
    # url = 'https://store.steampowered.com/search/?tags=1702'    # page with tag crafting
    # url_popup = 'https://store.steampowered.com/apphoverpublic/1086940?review_score_preference=0&l=english&pagev6=true'
  
    start = 0
    url_loadpage = f'https://store.steampowered.com/search/results/?query&start={start}&count=100&tags=1702&infinite=1'

    while True:

        print(url_loadpage)

        if True:
            start += 100
            url_loadpage = f'https://store.steampowered.com/search/results/?query&start={start}&count=100&tags=1702&infinite=1'
        else:
            break    

        sleep(0.4)    # slow cycle


# plan
# 1) gat all id's
# 2) change id in url and get data 





if __name__ == "__main__":
    main()