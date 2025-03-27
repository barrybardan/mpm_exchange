import re
import glob
import html
import os

def log(message):
    print(message)    


class Parser:

    root_path = 'pages/'
    data_file_path = 'data.txt'
    pic_list_path = 'pics.txt'

    def parse_all(self):
        counter = 0;
        max_number = 1000000
        # max_number = 2

        pages = self.get_pages_list()
        log(f"number of pages={len(pages)}")
        pages_info = []
        not_found = []
        not_an_article = []
        for page_file in pages:
            page_data = self.get_page_data(page_file)
            if page_data['not_an_article'] == True:
                if page_data['not_found'] == True:
                    not_found.append(page_data['full_url'])
                else:
                    not_an_article.append(page_data['full_url'])        
                continue
            counter += 1
            del page_data['not_found']
            del page_data['not_an_article']

            pages_info.append(page_data)    
            # log(page_data)
            if counter > max_number:
                break
        # self.check_result(pages_info)
        self.save_url_list(not_found,'not_found')
        self.save_url_list(not_an_article,'not_an_article')

        self.save_result(pages_info)
        self.save_pic_list(pages_info)


    def check_result(self, pages_info):
        print('TESTING...')
        self.check_description_number_of_elms(pages_info)
    
    def check_pics(self, pages_info):
        for page_info in pages_info:
            if page_info['main_pic'] == '':
                print(page_info['url'])
            for article in page_info['articles']:
                if article.get('pic','') != '':
                    print(f"{article['id']} = {article['pic']}")
        
    def check_description_number_of_elms(self, pages_info):
        article_and_number_of_description_elms = {}
        for page_info in pages_info:
            if page_info.get('description', None) == None:
                continue
            article_and_number_of_description_elms[page_info['main_article']] = len(page_info['description'])
        sorted_articles = sorted(article_and_number_of_description_elms.items(), key=lambda x:x[1])
        print(sorted_articles[-30:]) 
        articles__str = ''
        top_articles_by_number_of_desc_elms = []
        for elm in sorted_articles[-30:]:
            top_articles_by_number_of_desc_elms.append(elm[0])
        print(','.join(top_articles_by_number_of_desc_elms))


    def save_pic_list(self, pages_info):
        pics_list = []
        for page_info in pages_info:
            if page_info['main_pic'] != '':
                pics_list.append('https://'+page_info['site']+page_info['main_pic'])
            for article in page_info['articles']:
                if article.get('pic','') != '':
                    pics_list.append('https://'+page_info['site']+article['pic'])
        with open(self.pic_list_path, 'w', encoding='utf-8') as file:
            for pic in pics_list:
                file.write(str(pic)+'\n')
            file.close()    



    def save_result(self, pages_info):
        with open(self.data_file_path, 'w', encoding='utf-8') as file:
            for page_data in pages_info:
                file.write(str(page_data)+'\n')
            file.close()    

    def save_url_list(self, list, name):
        if len(list) == 0:
            return
        not_found_name= self.data_file_path.replace('data',name)
        with open(not_found_name, 'w', encoding='utf-8') as file:
            for url in list:
                file.write(url+'\n')
            file.close()    


    def get_page_data(self, page_file):
        content = self.get_file_content(page_file)
        # log(content)
        page_data = {}

        page_url = self.get_link(content)
        print('get link returned '+page_url)
        addr_arr = page_url.split(r'/')
        print(addr_arr)

        page_data['site'] = addr_arr[0]
        page_data['url'] = '/'.join(addr_arr[1:-1])
        print("URL = "+page_data['url'])

        page_data['not_found'] = False
        page_data['not_an_article'] = False


        if content.find('class="article-block"') == -1:
            page_data['full_url'] = page_url
            page_data['not_found'] = self.get_not_found(content)
            page_data['not_an_article'] = True
            return page_data


        page_data['main_pic'] = self.get_main_pic(content)
        page_data['main_article'] = self.get_main_article(content)
        page_data['articles'] = self.get_articles(content)
        page_data['description'] = self.get_description(content)
        page_data['accessories'] = self.get_accessories(content)


        pics_by_ids = self.get_pics_by_ids(content)
        for id, pic in pics_by_ids.items():
            self.add_pic_url_to_articles(id, pic, page_data['articles'])

        text_properties_by_id = self.get_text_properties_by_id(content)
        for id, properties in text_properties_by_id.items():
            self.add_properties_to_articles(id, properties, page_data['articles'])

        discontinued_by_id =  self.get_discontinued_by_ids(content)   
        for id, discontinued_vaue in discontinued_by_id.items():
            self.add_discontinued_to_articles(id, '1', page_data['articles'])

        # print(discontinued_by_id)

        return page_data

    def get_accessories(self, content):
        accessories = {}
        acc_data = re.findall('<div class="access acc_block" price="\d+" name="\d+" el-article="(\d+)" accfor="([\d\s]+)">', content)
        for item in acc_data:
            accessories['article_' + item[0]] = item[1]
        return accessories


    def get_main_article(self, content):
        blocks = re.findall('JCECommerce.selected = {\'currencyCode\':\'RUB\',\'id\':\'(\d+)\'',content)
        for block in blocks:
            return block
        return ''    

    def get_not_found(self, content):
        blocks = re.findall('<div class="page-404">',content)
        for block in blocks:
            return True
        return False    

    def get_description(self,content):
        decription_blocks = re.findall('<div class="full" itemprop="description">\s+<ul>[\s\S]+?<\/div>',content)
        print(decription_blocks)
        elms = []

        for block in decription_blocks:
            strings = re.findall('<li>([\s\S]+?)<\/li>',block)
            for st in strings:
                elms.append(self.strip_html_and_new_line(st))
            break    


        return elms        

    def strip_html_and_new_line(self, str):
        str = str.replace('&nbsp;',' ')
        str = html.unescape(str)
        str = re.sub('\\xa0', ' ', str)
        str = re.sub('<[^<]+?>|\n', '', str)
        str = re.sub('"', '«', str)
        return str

    def add_pic_url_to_articles(self, id, pic, articles):
        for article in articles:
            if article['id'] == id:
                article['pic'] = pic

    def add_properties_to_articles(self, id, properties, articles):
        for article in articles:
            if article['id'] == id:
                article['properties'] = properties

    def add_discontinued_to_articles(self, id, value, articles):
        for article in articles:
            if article['id'] == id:
                article['discontinued'] = value

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
        prop_dict['discontinued'] = '0'    
        return prop_dict     


    def get_file_content(self, file_path):
        with open(file_path, 'r', encoding="utf-8") as file:
            return file.read()
        return ''

    def get_pics_by_ids(self, content):
        ids_and_pics = re.findall('<div itemprop="offers"[\s\S]*?id="(\d+)"[\s\S]*?<a href="([^"]+)"',content)
        pics_by_ids = {}
        for item in ids_and_pics:
            id = item[0]
            pic = item[1]
            if not self.is_image_file(pic):
                continue
            pics_by_ids[id] = pic
            # print(f'id={id} pic={pic}')
        return pics_by_ids    

    def get_text_properties_by_id(self, content):
        text_blocks = re.findall('<dl data-article="(\d+)\s*"([\s\S]*?)<\/dl>',content)
        text_properties_by_id = {}
        for item in text_blocks:
            text_properties_by_id[item[0]] = self.get_text_properties_from_text(item[1])
        return text_properties_by_id

    def get_text_properties_from_text(self, text):
        # print(text)
        properties = re.findall('<dt>([^<]*)<\/dt>\s+<dd>([^<]*)<\/dd>',text)
        text_properties = []

        for item in properties:
            text_properties.append(item[0])
            text_properties.append(item[1])
        return text_properties

    def get_discontinued_by_ids(self, text):
        discontinued_items = re.findall('<div class="article">(\d+)<\/div>[\s\S]*?Снят с производства<\/div>',text)
        discontinued_by_id = {}
        for item in discontinued_items:
            discontinued_by_id[item] = True
            # print(item)
        return discontinued_by_id    
            

    def is_image_file(self, filename):
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
        lowercase_filename = filename.lower()
        for ext in image_extensions:
            if lowercase_filename.endswith(ext):
                return True
        return False

    def get_pages_list(self):
        pages = []
        for filename in glob.glob(self.root_path+'**/*index.html', recursive=True):
            pages.append(filename)
        return pages   


    def get_main_pic(self, content):
        # pic_urls = re.findall('<div class="item main-picture">\s+<a href="([^"]+)"',content)
        pic_urls = re.findall('<div class="item main-picture">[\S\s]*?<a href="([^"]+)',content)
        
        for pic_url in pic_urls:
            return pic_url
        # return self.get_main_pic_st(content)
        return ''

    def get_link(self, content):
        links = re.findall('mpm_parser_page_was_loaded_from_url="https:\/\/([^"]+)"',content)
        
        for link in links:
            return link
        # return self.get_main_pic_st(content)
        return self.get_link_from_page_content(content)

    def get_link_from_page_content(self, content):
        links = re.findall('<link rel="canonical" href="https:\/\/([^"]+)"',content)
        
        for link in links:
            return link
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