import pickle
import requests
import json
from datetime import date, timedelta 


def daterange(start_date: date, end_date: date):
    days = int((end_date - start_date).days)
    for n in range(days):
        yield start_date + timedelta(n)

def save_list_to_text_file(list, file_name):

    with open(file_name, 'w') as f:
        for line in list:
            f.write(f"{line}\n")


class PageListLoader:
    progress_data: None


    def get_new_pages_list(self):
        self.load_progress_data()
        print('last_loaded_date = '+str(self.progress_data['last_loaded_date']))
        date_start = self.progress_data['last_loaded_date']
        date_end = date.today() - timedelta(hours=23)  

        pages = self.get_page_list_from_task_file()

        try:
            for single_date in daterange(date_start, date_end):
                pages = pages + self.get_page_list_from_site(single_date)
        except Exception as e:
            print(f'Error while loading pages from site: {e}')
            
        pages = list(set(pages))

        self.progress_data['last_loaded_date'] = date_end
        print(f'last_loaded_date = {date_end}')

        return pages


    def get_page_list_from_task_file(self):
        try:
            lines_list = open('y:\\temp\\mpm_site_data\\tasks\\pages.txt',  mode='r', encoding='utf-8-sig').read().splitlines()
        except:
            lines_list = []
        return  lines_list   

    def load_new_pages(self):
        pages = self.get_new_pages_list()
        save_list_to_text_file(pages, 'pages_list.txt')


    def get_page_list_from_site(self, load_date):
        str_date = load_date.strftime("%Y-%m-%d")
        url =  f'https://metprommebel.ru/local/ajax/url_products.php?city=spb&from={str_date}&to={str_date}'
        response = requests.get(url)
        pages = []
        if response.status_code == 200:
            pages_json = response.json()
            if pages_json != None:
                for node in pages_json:
                    pages.append(node['URL'])
        else:
            print(f"Failed to download: {url}")
        return pages
            



    def load_progress_data(self):
        try:
            with open('progress_data.txt', 'rb') as fp:
                self.progress_data = pickle.load(fp)
        except:
            self.progress_data = {} 
        
        if not 'last_loaded_date' in self.progress_data:
            self.progress_data['last_loaded_date'] = date.fromisoformat('2024-08-17')
            # self.progress_data['last_loaded_date'] = date.fromisoformat('2024-09-01')


    def save_progress_data(self):
        with open('progress_data.txt', 'wb') as fp:
            pickle.dump(self.progress_data, fp)
