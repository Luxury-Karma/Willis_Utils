import random
import time
from telnetlib import EC

import openai
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

openai.api_key = "YOUR_API_KEY"  # Replace with your OpenAI API key
def chat(question):

    # Call the OpenAI API to generate a response
    response = openai.Completion.create(
        engine='davinci',
        prompt=question,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    )

    return response.choices[0].text.strip()  # Extract the generated reply

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


from selenium.webdriver.support import expected_conditions as EC

# Initialize the WebDriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(executable_path=,options=options)

driver.set_window_size(1366, 768)  # Set a custom viewport size


# Navigate to the URL
url = "https://auth0.openai.com/u/login/password?state=hKFo2SB0ck1DVHVmNG1lNGxjaG4tTVVONmM5S2VDaGk3VjFBcKFur3VuaXZlcnNhbC1sb2dpbqN0aWTZIGN3Rmx3UDNWWVFXMVhHU3ZxMW5fclFYWDhXeDBxeGVMo2NpZNkgVGRKSWNiZTE2V29USHROOTVueXl3aDVFNHlPbzZJdEc"
driver.get(url)

import modules.WillisConnections.WILLHANDLE as w
time.sleep(random.randrange(1,4))
w.click_specific_btn(driver, 'class="btn relative btn-primary"', 'button')

time.sleep(random.randrange(1,4))
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
input_field = driver.find_element(By.ID, 'username')
input_field.send_keys('natheypi@gmail.com')
input_field.send_keys(Keys.ENTER)
time.sleep(random.randrange(1,4))
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
input_field = driver.find_element(By.ID, 'password')
input_field.send_keys('hSkV6K%~:49$a^>')
input_field.send_keys(Keys.ENTER)




