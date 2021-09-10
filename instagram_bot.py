from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from auth_data import username, password
import time
import random

browser = webdriver.Chrome('./chromedriver')


def exit_from_browser():
    global browser
    browser.close()
    browser.quit()
    # this func closes the browser


def login(username, password):
    global browser  # no need to define it each time
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
        time.sleep(10)
        # now we logged in
        # browser.close()
        # browser.quit()
    except Exception as ex:
        print(ex)
        browser.close()
        browser.quit()


def hashtag_search(hashtag, rolls=5):
    global browser
    try:
        browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(5)

        for i in range(1, rolls, 1):
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight;')
            time.sleep(random.randrange(3, 7))
            # here we scroll to get as much urls as possible

        hrefs = browser.find_elements_by_tag_name('a')

        posts_urls = []
        for item in hrefs:
            href = item.get_attribute('href')

            if "/p/" in href:
                posts_urls.append(href)

        print(f'successfully parced urls for #{hashtag} hashtag, now bot will like posts')
        for url in posts_urls:
            try:
                browser.get(url)
                time.sleep(5)
                like_button = browser.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
                time.sleep(random.randrange(80, 100))
            except Exception as ex:
                print(ex)
                exit_from_browser()

            print("bot liked:   ", url)

        # browser.close()
        # browser.quit()
    except Exception as ex:
        print(ex)
        browser.close()
        browser.quit()


login(username, password)


hashtag_search(str(input('Please, enter hash tag you want to try:  ')), rolls=1)

browser.close()
browser.quit()
