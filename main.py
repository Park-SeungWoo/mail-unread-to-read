from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import pickle

import time
import warnings

warnings.filterwarnings('ignore')


def paging(unread_to_read):
    def wrapper(*args, **kwargs):
        driver = args[0]
        while True:
            try:
                unread_to_read(*args, **kwargs)
                next_btn_elem = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.ID, 'next-page')))
                if next_btn_elem.get_attribute('disabled'):
                    print('done!')
                    break
                else:
                    next_btn_elem.click()
            # except NoSuchElementException:  # selenium.common.exceptions  (if no elements => last page)
            #     print('paging process is done')
            #     break
            except BaseException as e:  # other exceptions
                print("something's wrong in paging decorator")
                print(e)
                break

    return wrapper


def login(driver):  # save cookies or load already saved cookies.
    try:
        ck = pickle.load(open('./cookies/naver_login.pkl', 'rb'))
    except FileNotFoundError:  # no pickle files
        print('login in 150sec!!!!!!!!!')
        time.sleep(150)
        print('save cookies')
        ck = driver.get_cookies()
        pickle.dump(ck, open('./cookies/naver_login.pkl', 'wb'))
    finally:
        for cookie in ck:
            driver.add_cookie(cookie)
        driver.get('https://mail.naver.com')
        time.sleep(3)

@paging
def unread_to_read(driver):
    WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, '/html/body/div[3]/div/div/div/div/div[4]/div/ul/li')))
    driver.find_element_by_class_name('button_checkbox_wrap').click()
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, 'button_checkbox_wrap'))).click()

    # delay until selected
    not_selected = True
    while not_selected:
        mail_elem = driver.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[4]/div/ul/li[1]')
        if mail_elem.get_attribute('class').split(' ')[1] == 'selected':
            not_selected = False

    read_unread_elem = driver.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[3]/div[2]/div[1]/div[3]/button')
    if read_unread_elem.get_attribute('class').split(' ')[1] == 'svg_read':
        read_unread_elem.click()
    else:
        pass


options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {'intl.accept_languages': 'ko'})

driver = webdriver.Chrome(executable_path='./Chrome_driver/chromedriver', chrome_options=options)
driver.get('https://www.naver.com')
login(driver)

unread_to_read(driver)

driver.close()
driver.quit()