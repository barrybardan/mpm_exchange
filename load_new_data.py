import os
import requests
from page_list_loader import PageListLoader
from mpm_parser import Parser
from datetime import date
from urllib.parse import urlparse
from urllib.parse import parse_qs

def get_test_pages_list():
    pages = []
    pages.append('https://metprommebel.ru/catalogue/shkafy-dlya-razdevalok/shkaf-garderob-kd-144k/?oid=2385')
    pages.append('https://metprommebel.ru/catalogue/sistemy-khraneniya-esd-antistaticheskie/statsionarnaya-kassetnitsa-na-2-yarusa-esd/?oid=90841')
    return pages 

def save_pages(pages, dir_path):
    if len(pages) == 0:
        return 
    if not os.path.exists(dir_path):
        os.makedirs(dir_path,)  
    for page_url in pages:
        oid = extract_param(page_url, 'oid')
        file_name = oid + '_index.html'
        file_path = os.path.join(dir_path, file_name)
        print(file_path)
        r = requests.get(page_url)  
        with open(file_path, 'wb') as f:
            f.write(r.content)
    return dir_path


def extract_param(url, param_name):
    parsed_url = urlparse(url)
    return parse_qs(parsed_url.query)[param_name][0]


def load_new_data():
    page_list_loader = PageListLoader()
    # pages = page_list_loader.get_new_pages_list()
    pages = get_test_pages_list()
    print(pages)
    date_str = date.today().strftime("%Y-%m-%d")
    dir_path = 'pages_'+date_str
    save_pages(pages, dir_path)
    ps = Parser()

    ps.root_path = dir_path + '/'
    ps.data_file_path = 'data_' + date_str + '.txt'
    ps.pic_list_path = 'pics_' + date_str + '.txt'
    ps.parse_all()

    # ps.test_glob()

def main():
    load_new_data()

if __name__ == "__main__":
    main()