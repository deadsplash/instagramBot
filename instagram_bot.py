from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from auth_data import username, password
import time
import datetime
import random

"""

INSTAGRAM BOT

Important! Please, don't forget to add user login data to 'auth_data.py'.
After logging in is done, you can work with a program.

"""




class InstagramBot:

    def __init__(self, username, password):
        print('Getting username and password and logging in Instagram.')
        time.sleep(1)
        print("Please, don't close Chrome window! It will proceed by itself.")
        time.sleep(1)
        print("Open this console after logging in is done!")
        time.sleep(3)
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome('./chromedriver')

    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    def save_urls_to_file(self, posts_urls, filename):

        with open(f'saved_urls/{filename}_urls.txt', 'a', encoding='utf-8') as f:
            for i in posts_urls:
                f.writelines(f'{i}\n')

        print(f'File "{filename}_urls" is successfully saved!')

    def login(self):

        browser = self.browser

        try:
            browser.get('https://www.instagram.com/')
            time.sleep(random.randrange(3, 5))

            username_input = browser.find_element_by_name('username')
            username_input.clear()
            username_input.send_keys(username)

            time.sleep(2)

            password_input = browser.find_element_by_name('password')
            password_input.clear()
            password_input.send_keys(password)

            password_input.send_keys(Keys.ENTER)
            time.sleep(5)

            # we let user to check if everything is OK, and then come back
            '''
            //////////////////////////////////////////////////
            Check if you are logged in before choosing options.
            //////////////////////////////////////////////////
            '''

        except Exception as ex:
            print(f'Something went wrong: {ex}')
            browser.close()
            browser.quit()

    def parse_posts_by_hashtag(self, hashtag, rolls=5):
        browser = self.browser
        print(f"Parsing urls with hashtag #{hashtag}.")

        try:
            browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
            time.sleep(5)

            for i in range(1, rolls, 1):
                browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(random.randrange(3, 7))
                # here we scroll to get as much urls as possible

            hrefs = browser.find_elements_by_tag_name('a')

            posts_urls = []
            for item in hrefs:
                href = item.get_attribute('href')

                if "/p/" in href:
                    posts_urls.append(href)

            print(f'Successfully parsed urls for #{hashtag}.')
            return posts_urls

        except Exception as ex:
            print(ex)
            browser.close()
            browser.quit()

    def xpath_exists(self, xpath):
        # checks if xpath exist in your page
        browser = self.browser
        try:
            browser.find_element_by_xpath(xpath)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    def wrong_post_checker(self):
        # if opened post is not valid - it will return False
        wrong_page = "/html/body/div[1]/section/main/div/div/h2"
        if self.xpath_exists(wrong_page):
            print("This post doesn't exist.")
            return False
        else:
            return True

    def account_checker(self, url):
        # we need to know if account exists, and if it's opened for you
        browser = self.browser
        browser.get(url)

        exist_xpath = '/html/body/div[1]/section/main/div/header/section/div[1]/h2'
        closed_xpath = '/html/body/div[1]/section/main/div/div/article/div[1]/div/h2'

        if self.xpath_exists(exist_xpath) == True:
            if self.xpath_exists(closed_xpath) == False:
                return True
            else:
                print('This is a closed account.')
                return False
        else:
            print("Wrong link, or account doesn't exist.")
            return False

    def parse_posts_by_account(self, account_url):
        browser = self.browser

        if self.account_checker(account_url) == True:
            print('Account is OK.')
        else:
            return

        try:
            browser.get(f'{account_url}')
            time.sleep(5)

            posts_count = int(browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span').text)
            loops_count = int(posts_count / 12)

            posts_urls = []
            for i in range(1, loops_count):
                print(f'Collecting urls, loop #{i}.')
                hrefs = browser.find_elements_by_tag_name('a')
                for item in hrefs:
                    href = item.get_attribute('href')

                    if "/p/" in href:
                        posts_urls.append(href)

                browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(random.randrange(3, 7))

            account_name = str(account_url).split("/")[-2]
            print(f"Successfully parsed urls of {account_name}!")
            return posts_urls

        except Exception as ex:
            print(ex)
            browser.close()
            browser.quit()

    def exact_post_like(self, url):
        # made for liking one post from multiple accounts
        browser = self.browser
        browser.get(url)
        time.sleep(7)

        like = '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button'
        if self.xpath_exists(like) == True and self.wrong_post_checker() == True:
            like_button = browser.find_element_by_xpath(like).click()
            time.sleep(3)
            print(f'Post {url} liked!')

    def like_machine(self, posts_urls, max_rolls=60, subscribe=False, save_liked_posts=False, save_subs=False):

        browser = self.browser
        count = 0
        liked_urls = []
        subbed_urls = []

        for url in posts_urls:
            if count < max_rolls:
                try:
                    browser.get(url)
                    time.sleep(7)

                    like = '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button'
                    sub = '/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[2]/button'
                    if self.xpath_exists(like) is True and self.wrong_post_checker() is True:
                        like_button = browser.find_element_by_xpath(like).click()
                        print(f"Bot liked:  {url}")
                        time.sleep(10)
                        # time.sleep(random.randrange(80, 100))   # important timeout to not get banned
                        count += 1

                        if save_liked_posts is True:
                            liked_urls.append(url)

                        if subscribe is True:
                            try:
                                sub_button = browser.find_element_by_xpath(sub).click()
                                if save_subs is True:
                                    subbed_urls.append(url)
                            except Exception as ex:
                                print(f'Failed to subscribe. Problem: {ex}')
                    else:
                        print(f"Got a problem with {url}, skipping.")
                        pass

                except Exception as ex:
                    self.close_browser()
                    print(ex)


        if save_liked_posts is True:
            filename = str(f'{datetime.date.today()}_liked')
            try:
                self.save_urls_to_file(liked_urls, filename)
            except Exception as ex:
                print(f"Failed to save liked posts to a file. Problem: {ex}")

        if save_subs is True:
            filename = str(f'{datetime.date.today()}_subbed')
            try:
                self.save_urls_to_file(liked_urls, filename)
            except Exception as ex:
                print(f"Failed to save liked posts to a file. Problem: {ex}")

        print(f'Work is done!')
        print(f"Number of posts liked:  {count}")
        self.close_browser()


"""
Now it's time to make console menu for users to make bot usable.
From this place you can implement it's functions to your app.
 
"""

main_menu = """
    MAIN MENU

1. Like machine
2. Subscribe machine | not available
3. Downloader | not available
4. Unsubscriber | not available 
0. Exit
"""


def check_inp():
    inp = str(input())
    try:
        inp = int(inp)
        return inp
    except KeyError:
        return False


def check_yesno():
    inp = str(input()).upper()
    if inp == "Y":
        return True
    elif inp == "N":
        return False
    else:
        print('Wrong input!')
        return


def main():

    print(main_menu)
    inp = check_inp()
    if inp is False:
        return

    if inp == 1:
        print("""
1. Hashtag liker
2. User posts liker | not available
3. User subscribers liker | not available
    """)
        inp = check_inp()

        if inp == 1:
            print('Please, type hashtag which you want to use.')
            hashtag = str(input())
            print('Do you want to save liked posts urls? Y/N')
            save_liked_posts = check_yesno()
            maxrolls_input = int(input("Max rolls?   "))
            bot = InstagramBot(username, password)
            bot.login()
            bot.like_machine(
                posts_urls=bot.parse_posts_by_hashtag(hashtag),
                save_liked_posts=save_liked_posts,
                max_rolls=maxrolls_input)

        elif inp == 2:
            print("Will be available soon.")
            return

        elif inp == 3:
            print("Will be available soon.")
            return

    elif inp == 2:
        print("""
1. Use hashtag to find users. | not available
2. Use user's subscribers to find users. | not available
        """)
        inp = check_inp()

        return

    elif inp == 0:
        exit()


while True:
    main()
