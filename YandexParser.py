from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, parse_qs
from unicodedata import normalize
from fake_headers import Headers

headless_headers = {'accept': '*/*',
           'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,hi;q=0.7,la;q=0.6',
           'cache-control': 'no-cache',
           'dnt': '1',
           'pragma': 'no-cache',
           'referer': 'https',
           'sec-fetch-mode': 'no-cors',
           'sec-fetch-site': 'cross-site',
           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
           }

fake_header = Headers()

def parse_queries(url):
    parsed_url = urlparse(url)
    return parse_qs(parsed_url.query)


class YandexPage():
    def __init__(self, url):
        self.url = url
        self.content = requests.get(
            url, headers=fake_header.generate()).content.decode('utf-8')
        self.soup = BeautifulSoup(self.content, 'html.parser')

    def parse(self):
        pass


class YandexNews(YandexPage):
    def __init__(self, url):
        super().__init__(url)
        self.stories = {}

    def parse(self):
        for story in self.soup.find_all('a', class_='mg-card__link', href=True):
            st_url = story['href']
            st_id = parse_queries(st_url)['persistent_id'][0]
            st_name = normalize('NFKC', story.get_text())
            self.stories[st_id] = (st_name, st_url)


class YandexStory(YandexPage):
    def __init__(self, url):
        super().__init__(url)
        self.trend_instories = []
        self.id = parse_queries(url)['persistent_id'][0]

    def parse(self):  # retrieve all trending instories
        # TODO order of instories does not match visible page
        for instory in self.soup.find_all('a', class_='mg-snippet__url', href=True):
            ist_url = instory['href']
            ist_name = normalize('NFKC', instory.get_text())
            print(ist_name)
            self.trend_instories.append((ist_name, ist_url))


class YandexInstory(YandexPage):
    def __init__(self, url):
        super().__init__(url)
        self.instories = []
        self.st_id = parse_queries(url)['persistent_id'][0]

        story = self.soup.find('a', class_='news-search-story__title-link', href=True)
        self.st_title = normalize('NFKC', story.get_text())
        self.st_url = story['href']

    def parse(self):
        for instory in self.soup.select('div.mg-snippet__content'):
            instory_content = instory.select_one('a.mg-snippet__url')
            ist_url = instory_content['href']
            ist_title = normalize('NFKC', instory_content.get_text())

            agency_name = instory.select_one('.mg-snippet-source-info__agency-name').get_text()
            agency_url = urlparse(ist_url).netloc
            time = instory.select_one('.mg-snippet-source-info__time').get_text()

            self.instories.append((ist_title, ist_url, agency_name, agency_url, time))


if __name__ == '__main__':

    #uncomment each section to test out each class

    news = YandexNews('https://yandex.ru/news/region/kazan')
    news.parse()
    print(news.stories)

    # story = YandexStory('https://yandex.ru/news/story/Okolo_30_mesyachnoj_normy_osadkov_vypadet_vTatarstane_vblizhajshie_dni--f222818b27ac4cd9ea819acdbe382a58?lang=ru&rubric=Kazan&fan=1&stid=TguKoHOf0D9Zf0MyuT7E&t=1643908727&persistent_id=178640252')
    # story.parse()
    # print(story.trend_instories)

    # instory = YandexInstory('https://yandex.ru/news/instory/Okolo_30_mesyachnoj_normy_osadkov_vypadet_vTatarstane_vblizhajshie_dni--f222818b27ac4cd9ea819acdbe382a58?lr=121642&content=alldocs&stid=TguKoHOf0D9ZuT7Ef0My&persistent_id=178640252&from=story')
    # instory.parse()
    # print(instory.st_title)
    # print(instory.st_url)
    # print(instory.st_id)
    # print(instory.url)
    # print(instory.instories)
