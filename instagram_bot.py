from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from auth_data import username, password
import time
import random

"""

INSTAGRAM BOT

Important! Please, don't forget to add user login data to 'auth_data.py'.
After logging in is done, you can work with a program.

"""

# Telling user what's happening
print('Getting username and password and logging in Instagram.')
time.sleep(1)
print("Please, don't close Chrome window! It will proceed by itself.")
time.sleep(1)
print("Open this console after logging in is done!")
time.sleep(3)
browser = webdriver.Chrome('./chromedriver')


def exit_from_browser():
    global browser
    browser.close()
    browser.quit()
    # this func closes the browser


def login(username, password):
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
        print('''
        //////////////////////////////////////////////////
        Check if you are logged in before choosing options.
        //////////////////////////////////////////////////
        ''')
        time.sleep(7)

    except Exception as ex:
        print(f'Something went wrong: {ex}')
        browser.close()
        browser.quit()


def like_machine(posts_urls):
    # you'd better not like more that 60 posts a day, in case of getting banned for suspicious activity
    count = 0
    for url in posts_urls:
        if 0 < count < 60:
            try:
                browser.get(url)
                time.sleep(5)
                like_button = browser.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
                time.sleep(random.randrange(80, 100))
                count += 1

            except Exception as ex:
                exit_from_browser()
                print(ex)
        else:
            pass

        print("bot liked:   ", url)
    print(f"Number of posts liked:  {count}")


def hashtag_search(hashtag, exit_check,rolls=5):
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

        like_machine(posts_urls)

        if exit_check == "Y":
            browser.close()
            browser.quit()
            return False
        elif exit_check == "N":
            pass
        else:
            print('Something went wrong:  exit_check is incorrect.')
        # browser.close()
        # browser.quit()
    except Exception as ex:
        print(ex)
        browser.close()
        browser.quit()


def main():
    login(username, password)
    while True:
        print("""
    Please, choose option from the list: 
    
1. Hashtag liker
2. *** / work in progress
3. *** / work in progress
4. *** / work in progress
0. Exit
        """)
        try:
            inp = int(input())
        except Exception as ex:
            print('Wrong input, please try again.')
            break
        if inp == 1:
            hashtag = str(input('Please, enter hash tag you want to try:  '))
            print("Do you want to close browser after everything is done? Y/N")
            exit_check = str(input()).upper()
            if exit_check == 'Y' or exit_check == 'N':
                print(f'OK, posting likes on #{hashtag}, please do not stop the program.')
                time.sleep(3)  # small pause so user can read what you wrote in console
                hashtag_search(hashtag, exit_check, rolls=1)
            else:
                print('Incorrect inputs, please try again.')
        elif inp == 2:
            print('Not available now.')
            pass
        elif inp == 3:
            print('Not available now.')
            pass
        elif inp == 4:
            print('Not available now.')
            pass
        elif inp == 0:
            browser.close()
            browser.quit()
            print('App is shutting down.')
            return False


main()
