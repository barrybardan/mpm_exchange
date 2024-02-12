import re
import glob


def log(message):
    print(message)    


class Parser:

    root_path = 'pages/'
    data_file_path = 'data.txt'


    def parse_all(self):
        counter = 0;
        max_number = 1000000
        pages = self.get_pages_list()
        log(f"number of pages={len(pages)}")
        pages_info = []
        for page_file in pages:
            page_data = self.get_page_data(page_file)
            if page_data == None:
                continue
            counter += 1
            pages_info.append(page_data)    
            # log(page_data)
            if counter > max_number:
                break
        # self.check_result(pages_info)
        self.save_result(pages_info)


    def check_result(self, pages_info):
        print('TESTING...')
        for page_info in pages_info:
            if page_info['main_pic'] == '':
                print(page_info['url'])


    def save_result(self, pages_info):
        with open(self.data_file_path, 'w', encoding='utf-8') as file:
            for page_data in pages_info:
                file.write(str(page_data)+'\n')
            file.close()    


    def get_page_data(self, page_file):
        content = self.get_file_content(page_file)
        # log(content)
        if content.find('class="article-block"') == -1:
            return None

        page_data = {}
        addr_arr = page_file.split('/')
        page_data['site'] = addr_arr[1]
        page_data['url'] = '/'.join(addr_arr[2:-1])
        page_data['main_pic'] = self.get_main_pic(content)
        page_data['articles'] = self.get_articles(content)

        return page_data


    def get_articles(self, content):
        articles_strings = re.findall('<div itemprop="offers"[^>]+>',content)
        
        articles = []
        for article_str in articles_strings:
            properties = self.get_properties(article_str)
            articles.append(properties.copy())
        return  articles   


    def get_properties(self, article):
        properties = re.findall('(\w+)="([^"]+)"',article)
        prop_dict = {}
        for property in properties:
            prop_dict[property[0]] = property[1]
        return prop_dict     


    def get_file_content(self, file_path):
        with open(file_path, 'r', encoding="utf-8") as file:
            return file.read()
        return ''


    def get_pages_list(self):
        pages = []
        for filename in glob.glob(self.root_path+'**/index.html', recursive=True):
            pages.append(filename)
        return pages   


    def get_main_pic(self, content):
        # pic_urls = re.findall('<div class="item main-picture">\s+<a href="([^"]+)"',content)
        pic_urls = re.findall('<div class="item main-picture">[\S\s]*?<a href="([^"]+)',content)
        
        for pic_url in pic_urls:
            return pic_url
        # return self.get_main_pic_st(content)
        return ''

    # def get_main_pic_st(self, content):
    #     pic_urls = re.findall('<div class="st_pic" id="firpic">\s*<img src="([^"]+)"',content)
    #     for pic_url in pic_urls:
    #         return pic_url
    #     return ''


    def test_glob(self):
        for filename in glob.glob(self.root_path+'**/index.html', recursive=True):
            print(filename)  
    

def main():
    ps = Parser()
    ps.parse_all()
    # ps.test_glob()


if __name__ == "__main__":
    main()