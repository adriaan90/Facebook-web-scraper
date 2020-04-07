import requests
import random

from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from secrets import username, password

class FaceBookBot():

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-notifications')
        self.driver = webdriver.Chrome(options=options)

    def login(self,username, password):
        self.driver.get("https://www.facebook.com/login")

        sleep(2)

        email_in = self.driver.find_element_by_xpath('//*[@id="email"]')
        email_in.send_keys(username)

        password_in = self.driver.find_element_by_xpath('//*[@id="pass"]')
        password_in.send_keys(password)

        login_btn = self.driver.find_element_by_xpath('//*[@id="loginbutton"]')
        login_btn.click()

        sleep(2)



    def log_in_basic(self):
        POST_LOGIN_URL = 'https://mbasic.facebook.com/login'

        payload = {
            'email': username,
            'pass': password
        }

        with requests.Session() as session:
            post = session.post(POST_LOGIN_URL, data=payload)

    def post_likes(self):
        #This URL will be the URL that your login form points to with the "action" tag.
        POST_LOGIN_URL = 'https://mbasic.facebook.com/login'

        #This URL is the page you actually want to pull down with requests.
        post_ID = 'the-post-ID'
        limit = 200
        REQUEST_URL = f'https://mbasic.facebook.com/ufi/reaction/profile/browser/fetch/?limit={limit}&total_count=17&ft_ent_identifier={post_ID}'

        payload = {
            'email': username,
            'pass': password
        }

        with requests.Session() as session:
            post = session.post(POST_LOGIN_URL, data=payload)
            r = session.get(REQUEST_URL)
        soup = BeautifulSoup(r.content, "html.parser")
        names = soup.find_all('h3', class_='be')
        people_who_liked = []
        for name in names:
            people_who_liked.append(name.text)

        return people_who_liked

    def post_shares(self):
        #This URL will be the URL that your login form points to with the "action" tag.
        POST_LOGIN_URL = 'https://mbasic.facebook.com/login'

        post_ID = 'the-post-ID'
        #This URL is the page you actually want to pull down with requests.
        REQUEST_URL = f'https://m.facebook.com/browse/shares?id={post_ID}'

        payload = {
            'email': username,
            'pass': password
        }

        with requests.Session() as session:
            post = session.post(POST_LOGIN_URL, data=payload)
            r = session.get(REQUEST_URL)
        soup = BeautifulSoup(r.content, "html.parser")
        names = soup.find_all('span')
        people_who_shared = []
        for name in names:
            people_who_shared.append(name.text)

        return people_who_shared

    def page_likes(self):
        self.login(username, password)

        page_name = "your-page-name"
        # This URL is the page you actually want to pull down with requests.
        REQUEST_URL = f'https://www.facebook.com/{page_name}/settings/?tab=people_and_other_pages&ref=page_edit'

        self.driver.get(REQUEST_URL)

        sleep(2)

        for i in range(1,15):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)

        page = self.driver.page_source
        soup = BeautifulSoup(page, "html.parser")
        names = soup.find_all('a', class_='_3cb8')
        people_who_liked_page = []
        for name in names:
            people_who_liked_page.append(name.text)

        return people_who_liked_page

    def select_winner(self,list_A,list_B,list_C):
        eligible_to_win = []
        for name in list_A:
            if name in list_B and name in list_C:
                eligible_to_win.append(name)
        return eligible_to_win

bot = FaceBookBot()
people_who_follow = bot.page_likes()
people_who_liked = bot.post_likes()
people_who_shared = bot.post_shares()

eligible = bot.select_winner(people_who_liked,people_who_follow,people_who_shared)
winner = random.choice(eligible)
print(winner)


