import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import bs4 as BeautifulSoup
import time



def willis_college_connection(driver, willis_username: str, willis_password: str):
    url = "https://willisonline.ca/login"
    driver.get(url)

    try:
        img = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'img[alt="Sign in with Microsoft"]'))
        )
    except Exception as e:
        print("An error occurred: ", e)
    else:
        link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//img[@alt="Sign in with Microsoft"]/..'))
        )
        link.click()
        microsoft_connection(willis_username,willis_password, driver)


def microsoft_connection(username: str, password: str, driver):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'loginfmt')))
        input_field = driver.find_element(By.NAME, 'loginfmt')
        input_field.send_keys(username)
        button_input = driver.find_element(By.ID, 'idSIButton9')
        button_input.click()

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'passwd')))
        input_field = driver.find_element(By.NAME, 'passwd')
        input_field.send_keys(password)
        button_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'idSIButton9')))
        button_input.click()

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'idBtn_Back')))
        button_input = driver.find_element(By.ID, 'idBtn_Back')
        button_input.click()
    except Exception as e:
        print("An error occurred: ", e)


def willis_to_moodle(driver) -> str:
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT,'Moodle')))
        driver.find_element(By.LINK_TEXT, 'Moodle').click()
        time.sleep(5)  # wait for new tab to open
        driver.switch_to.window(driver.window_handles[-1])  # switch to the new tab (it should be the last one in the list of window handles)
        # Get the new URL
        new_url = driver.current_url
        return new_url
    except Exception as e:
        print("An error occurred ", e)






def open_links_in_new_tabs(driver):
    try:
        # Find all divs with the specified class
        divs = driver.find_elements(By.XPATH, '//div[@class="list-group-item timeline-event-list-item flex-column pt-2 pb-0 border-0 px-2" and @data-region="event-list-item"]')

        # For each div, find the 'a' tag and extract the href attribute (URL)
        urls = [div.find_element(By.TAG_NAME, 'a').get_attribute('href') for div in divs]

        # Open each URL in a new tab
        for url in urls:
            driver.execute_script(f"window.open('{url}', '_blank');")
            time.sleep(1)  # add a delay to allow each tab to load

    except Exception as e:
        print("An error occurred: ", e)



def main():
    driver = webdriver.Chrome()  # Initialize the driver here
    username = ''
    password = ''

    willis_college_connection(driver, username, password)
    willis_to_moodle(driver)

    open_links_in_new_tabs(driver)

    while True:
        pass


if __name__ == '__main__':
    main()
