from selenium import webdriver
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from model.Follower import Follower
from model.Following import Following

url = 'https://www.instagram.com/'
browser = webdriver.Chrome()
actions = ActionChains(browser)
wait = 5

followers = []
following = []
no_follow = []
user = '' # type here instagram user
password = '' # type here instagram password


def open_browser():
    browser.get(url)


def login():
    time.sleep(wait)
    input_user = browser.find_element_by_name('username')
    input_pass = browser.find_element_by_name('password')
    input_user.send_keys(user)
    input_pass.send_keys(password)
    login_button = browser.find_element_by_css_selector('.sqdOP.L3NKy.y3zKF')
    login_button.click()


def close_pop_up():
    time.sleep(wait)
    close = browser.find_element_by_css_selector('.aOOlW.HoLwm')
    close.click()


def open_profile():
    time.sleep(wait)
    profile = browser.find_element_by_css_selector('.RR-M-._2NjG_')
    profile.click()


def open_followers():
    time.sleep(wait)
    links = browser.find_elements_by_css_selector('.-nal3')
    for link in links:
        if link.get_attribute('href') == 'https://www.instagram.com/' + user + '/followers/':
            link.click()


def save_followers():
    time.sleep(wait)
    final = False
    last = ''
    while final is False:
        time.sleep(2)
        usernames = browser.find_elements_by_css_selector('.FPmhX.notranslate._0imsa')
        if usernames[usernames.__len__() - 1] != last:
            for username in usernames:
                last = username
                if check_exists_follower(username.get_attribute('title')):
                    followers.append(Follower(username.get_attribute('title')))
            browser.execute_script("arguments[0].scrollIntoView();", last)
        else:
            final = True
    close_list()


def check_exists_follower(username):
    for us in followers:
        if us.nick == username:
            return False
    return True


def check_exists_following(username):
    for us in following:
        if us.nick == username:
            return False
    return True


def close_list():
    svgs = browser.find_elements_by_tag_name('svg')
    for svg in svgs:
        if svg.get_attribute('aria-Label') == 'Cerrar':
            svg.click()


def open_following():
    time.sleep(wait)
    links = browser.find_elements_by_css_selector('.-nal3')
    for link in links:
        if link.get_attribute('href') == 'https://www.instagram.com/' + user + '/following/':
            link.click()


def save_following():
    time.sleep(wait)
    final = False
    last = ''
    while final is False:
        time.sleep(2)
        usernames = browser.find_elements_by_css_selector('.FPmhX.notranslate._0imsa')
        if usernames[usernames.__len__() - 1] != last:
            for username in usernames:
                last = username
                if check_exists_following(username.get_attribute('title')):
                    following.append(Following(username.get_attribute('title')))
            browser.execute_script("arguments[0].scrollIntoView();", last)
        else:
            final = True
    close_list()


def check_who_no_follow():
    for follow in following:
        if check_exists_follower(follow.nick):
            no_follow.append(follow)


def show_no_follow():
    print('Dont follow you back this people: ')
    for no in no_follow:
        print(no.nick)


def check_if_code():
    time.sleep(wait)
    try:
        code = browser.find_element_by_css_selector('._2hvTZ.pexuQ.zyHYP')
        code.send_keys(str(input()))
        button = browser.find_element_by_css_selector('.sqdOP.L3NKy.y3zKF')
        button.click()
    except NoSuchElementException:
        print('Without verification code')


if __name__ == "__main__":
    open_browser()
    login()
    check_if_code()
    close_pop_up()
    open_profile()
    open_followers()
    save_followers()
    open_following()
    save_following()
    check_who_no_follow()
    show_no_follow()
