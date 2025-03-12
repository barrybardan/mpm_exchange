import os
import requests
import shutil
from page_list_loader import PageListLoader
from convert_to_png import convert_webp_to_png
from mpm_parser import Parser
from datetime import date
from urllib.parse import urlparse
from urllib.parse import parse_qs


SHARE_DIR =  'y:\\temp\\mpm_site_data\\'

def get_test_pages_list():
    pages = []
    pages.append('https://spb.metprommebel.ru/catalogue/pochtovye-yashchiki-serii-bazis-plyus/pochtovyy-yashchik-4-sektsionnyy-seriya-bazis-plyus/')
    pages.append('https://spb.metprommebel.ru/catalogue/pochtovye-yashchiki-serii-bazis/metallicheskiy-pochtovyy-yashchik-4-sektsionnyy-seriya-bazis/')
    return pages 



def save_pages(pages, dir_path):
    if len(pages) == 0:
        return 
    if not os.path.exists(dir_path):
        os.makedirs(dir_path,)  
    counter = 0    
    for page_url in pages:
        file_name = 'index.html'
        print(page_url)
        page_path = str(counter).zfill(5)
        page_dir = os.path.join(dir_path, page_path)
        print(page_dir)
        if not os.path.exists(page_dir):
            os.makedirs(page_dir,)  

        file_path = os.path.join(page_dir, file_name)
        print(file_path)
        r = requests.get(page_url) 
        page_content = r.content.decode("utf-8")
        page_content += page_content + '<!-- mpm_parser_page_was_loaded_from_url="' + page_url+'" --!>'

        with open(file_path, 'w', encoding="utf-8") as f:
            f.write(page_content)
        counter += 1   

    return dir_path


def get_page_path(page_url):
    page_path = page_url.replace('https://','')
    return page_path


def extract_param(url, param_name):
    parsed_url = urlparse(url)
    return parse_qs(parsed_url.query)[param_name][0]

def save_pics(date_str):
    filename = 'pics_'+date_str+'.txt'
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    print(lines)
    root_pics_dir = 'y:\\temp\\mpm_site_data\\pics'
    for pic_url in lines:
        pic_dir_path, file_name = get_pic_dir_and_file_name(pic_url)
        # print(f'pic_dir_path = {pic_dir_path}')
        # print(f'file_name = {file_name}')
        pic_dir = os.path.join(root_pics_dir, pic_dir_path)
        pic_path = os.path.join(pic_dir, file_name)
        print(pic_path)
        if os.path.isfile(pic_path):
            print('found downloaded')
            continue
        if not os.path.exists(pic_dir):
            os.makedirs(pic_dir,)  

        r = requests.get(pic_url)  
        with open(pic_path, 'wb') as f:
            f.write(r.content)


def get_pic_dir_and_file_name(pic_url):
    pic_path = pic_url.replace('https://','')
    pic_path_arr = pic_path.split('/')
    file_name = pic_path_arr[-1] 
    pic_path_arr = pic_path_arr[:-1] 
    pic_dir_path = '/'.join(pic_path_arr)
    return pic_dir_path,  file_name

def load_new_data():
    page_list_loader = PageListLoader()
    pages = page_list_loader.get_new_pages_list()
    print(pages)

    date_str = date.today().strftime("%Y-%m-%d")
    dir_path = 'pages/pages_'+date_str
    save_pages(pages, dir_path)

    ps = Parser()
    ps.root_path = dir_path + '/'
    ps.data_file_path = 'data_' + date_str + '.txt'
    ps.pic_list_path = 'pics_' + date_str + '.txt'
    ps.parse_all()

    save_pics(date_str)
    shutil.copyfile(ps.data_file_path, SHARE_DIR + ps.data_file_path)
    page_list_loader.save_progress_data()
    convert_webp_to_png('y:/temp/mpm_site_data/pics')

def main():
    load_new_data()

if __name__ == "__main__":
    main()