import requests
from bs4 import BeautifulSoup
from datetime import datetime

# import sched, time
# s = sched.scheduler(time.time, time.sleep)
# def do_something(sc):
#     # do your stuff
#     s.enter(60, 1, do_something, (sc,))
#
# s.enter(60, 1, do_something, (s,))
# s.run()

# Парсер новостей с сайта news.pn.
class ParsePN:

    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
        }
        self.url = 'https://news.pn/'
        self.prev_news = ''

    def parse_news(self):
        try:
            # Логика нашего парсера.
            r = requests.get(self.url, headers=self.headers, timeout=5)
            soup = BeautifulSoup(r.content, 'html.parser')
            last_news = soup.find('div', class_="feedlast").find('a').get('href')

            if last_news and last_news[0] == '/':
                last_news = self.url + last_news

            if self.prev_news != last_news:
                self.prev_news = last_news
                return self.prev_news
            else:
                return ''

        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            with open('log.txt', 'a') as output_file:
                output_file.write(str(datetime.now()) + ' ' + self.url + ' ' + str(e) + '\n')
            print(str(e))
        except requests.Timeout as e:
            print("OOPS!! Timeout Error")
            with open('log.txt', 'a') as output_file:
                output_file.write(str(datetime.now()) + ' ' + self.url + ' ' + str(e) + '\n')
            print(str(e))
        except requests.RequestException as e:
            print("OOPS!! General Error")
            with open('log.txt', 'a') as output_file:
                output_file.write(str(datetime.now()) + ' ' + self.url + ' ' + str(r.status_code) + str(e) + '\n')
            print(str(e))
        except KeyboardInterrupt:
            print("Someone closed the program")
            with open('log.txt', 'a') as output_file:
                output_file.write(str(datetime.now()) + ' ' + self.url + ' ' + str(r.status_code) + 'Someone closed the program' + '\n')

# Парсер новостей по региону Николаевской области с сайта ukr.net.
class ParseUkrNetMk:

    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
        }
        self.url = 'https://www.ukr.net/ua/news/nikolaev.html'
        self.prev_news = ''

    def parse_news(self):
        try:
            # Логика нашего парсера.
            r = requests.get(self.url, headers=self.headers, timeout=5)
            soup = BeautifulSoup(r.content, 'html.parser')
            last_news = soup.find('div', class_="im-tl").find('a').get('href')

            if self.prev_news != last_news:
                self.prev_news = last_news
                return self.prev_news
            else:
                return ''

        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            with open('log.txt', 'a') as output_file:
                output_file.write(str(datetime.now()) + ' ' + self.url + ' ' + str(e) + '\n')
            print(str(e))
        except requests.Timeout as e:
            print("OOPS!! Timeout Error")
            with open('log.txt', 'a') as output_file:
                output_file.write(str(datetime.now()) + ' ' + self.url + ' ' + str(e) + '\n')
            print(str(e))
        except requests.RequestException as e:
            print("OOPS!! General Error")
            with open('log.txt', 'a') as output_file:
                output_file.write(str(datetime.now()) + ' ' + self.url + ' ' + str(r.status_code) + str(e) + '\n')
            print(str(e))
        except KeyboardInterrupt:
            print("Someone closed the program")
            with open('log.txt', 'a') as output_file:
                output_file.write(str(datetime.now()) + ' ' + self.url + ' ' + str(r.status_code) + 'Someone closed the program' + '\n')





