from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import re



QUIZ_DETECTION_REGEX : str = '^(.*?)Quiz(.*)'
WILLIS_WEB_SITE = "https://willisonline.ca/login"



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



def search_for_quiz(driver):
    # Get a list of all window handles
    all_tabs = driver.window_handles

    # Iterate over all tabs
    for tab in all_tabs:
        # Switch to the current tab
        driver.switch_to.window(tab)

        # Check for "Quiz" in the title
        title = driver.title
        if re.search(QUIZ_DETECTION_REGEX, title):
            print('Quiz page found:', driver.current_url)
            return driver.current_url  # return the URL of the quiz page

    # No quiz page found
    return None







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
    willis_college_connection(driver, username, password)
    willis_to_moodle(driver)
    new_url = open_links_in_new_tabs(driver)
    quiz_url = search_for_quiz(driver)
    if quiz_url is not None:
        print('Quiz page URL:', quiz_url)
        # Now you are on the quiz page and can perform operations on it.
    else:
        print("No quiz found.")

    input('press enter to quit the browser')
    driver.quit()








def create_driver():
    return webdriver.Chrome()






