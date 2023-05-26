from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
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

        # Store the original window handles
        original_windows = driver.window_handles

        # Open each URL in a new tab
        for url in urls:
            driver.execute_script(f"window.open('{url}', '_blank');")
            time.sleep(1)  # add a delay to allow each tab to load

        # Return only the new window handles
        new_windows = [window for window in driver.window_handles if window not in original_windows]

        return new_windows

    except Exception as e:
        print("An error occurred: ", e)


def download_links_from_tabs(driver, div_class, new_tabs):
    for tab in new_tabs:
        # Switch to each tab
        driver.switch_to.window(tab)

        # Give the page some time to load
        time.sleep(1)

        # Find the 'a' elements in the specific div and get the href attribute
        links = driver.find_elements_by_css_selector(f'div.{div_class} a')

        # Download href content from these links
        for link in links:
            href = link.get_attribute('href')

            # Send a GET request to the href URL
            response = requests.get(href, stream=True)

            # Check if the request is successful
            if response.status_code == 200:
                # Get the file name from the href, you might want to customize this
                file_name = href.split('/')[-1]

                # Write the response content to a file
                with open(file_name, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)

                print(f'Downloaded: {file_name}')

def total_connection(username, password):
    driver = create_driver()
    willis_college_connection(driver,username,password)
    willis_to_moodle(driver)
    open_links_in_new_tabs(driver)
    download_links_from_tabs(driver, 'fileuploadsubmission', open_links_in_new_tabs(driver))




def create_driver():
    return webdriver.Chrome()






