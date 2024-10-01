
from page_list_loader import PageListLoader
from mpm_parser import Parser



def get_test_pages_list():
    pages = []
    pages.append('https://metprommebel.ru/catalogue/shkafy-dlya-razdevalok/shkaf-garderob-kd-144k/?oid=2385')
    pages.append('https://metprommebel.ru/catalogue/sistemy-khraneniya-esd-antistaticheskie/statsionarnaya-kassetnitsa-na-2-yarusa-esd/?oid=90841')
    return pages 

def main():
    page_list_loader = PageListLoader()
    # pages = page_list_loader.get_new_pages_list()
    pages = get_test_pages_list()
    print(pages)
    ps = Parser()
    # ps.test_glob()


if __name__ == "__main__":
    main()