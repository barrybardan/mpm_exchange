import re
import glob


def log(message):
    print(message)    


class Parser:

    root_path = 'pages/'

    def parse_all(self):
        pages = self.get_pages_list()
        # print(pages)
        for page_file in pages:
            page_data = self.get_page_data(page_file)
            if page_data == None:
                continue
            log(page_data)
            break 

    def get_page_data(self, page_file):
        content = self.get_file_content(page_file)
        # log(content)
        if content.find('class="article-block"') == -1:
            return None

        page_data = {}
        addr_arr = page_file.split('/')
        page_data['site'] = addr_arr[1]
        page_data['url'] = '/'.join(addr_arr[2:-1])
        return page_data

    def get_file_content(self, file_path):
        with open(file_path, 'r', encoding="utf-8") as file:
            return file.read()
        return ''

    def get_pages_list(self):
        pages = []
        for filename in glob.glob(self.root_path+'**/index.html', recursive=True):
            pages.append(filename)
        return pages   


    def test_glob(self):
        for filename in glob.glob(self.root_path+'**/index.html', recursive=True):
            print(filename)  
    


def main():
    ps = Parser()
    ps.parse_all()
    # ps.test_glob()


if __name__ == "__main__":
    main()