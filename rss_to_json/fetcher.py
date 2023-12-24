from json import loads
import urllib.request as ulrr

class News:

    @staticmethod
    def irna_news():
        url = "https://api.rss2json.com/v1/api.json?rss_url=https://www.irna.ir/rss"
        response = ulrr.urlopen(url).read().decode('utf8')
        disarray_data = loads(response)
        raw_information = disarray_data['items']

        titles_list = []
        authors_list = []
        dates_list = []
        for ele in range(len(raw_information)):
            titles_list.append((raw_information[ele])['title'])
            authors_list.append((raw_information[ele])['author'])
            dates_list.append((raw_information[ele])['pubDate'])

        cnt = 0
        data = []
        for cnt in range(10):
            data_dict = {
                'title' : titles_list[cnt],
                'author' : authors_list[cnt],
                'publish date' : dates_list[cnt],
            }
            data.append(data_dict)

        return data


if __name__ == '__main__':
    def fetch_and_print_news():
        print(News.irna_news())

    fetch_and_print_news()
