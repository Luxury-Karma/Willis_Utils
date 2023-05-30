from urllib.parse import urlparse,parse_qs

from bs4 import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re


class WILLHANDLE:


    def __init__(self,WILLIS_WEB_SITE=None, QUIZ_DETECTION_REGEX=None):
        """
        You do not have to change anything in normal condition use
        :param WILLIS_WEB_SITE: URL of the website
        :param QUIZ_DETECTION_REGEX: Regex to detect a specific URL
        """
        self.QUIZ_DETECTION_REGEX = QUIZ_DETECTION_REGEX if QUIZ_DETECTION_REGEX else \
            r'^https:\/\/students\.willisonline\.ca\/mod\/quiz\/.*$'
        self.WILLIS_WEB_SITE = WILLIS_WEB_SITE if WILLIS_WEB_SITE else "https://willisonline.ca/login"
        self.driv = webdriver.Chrome()

    def __microsoft_connection(self, username: str, password: str) -> None:
        """
        Connection by the microsoft token oauth2 authentification
        :param username: the username to connect with (full)
        :param password: the password link to that account
        :return: None
        """
        try:
            WebDriverWait(self.driv, 10).until(EC.presence_of_element_located((By.NAME, 'loginfmt')))
            input_field = self.driv.find_element(By.NAME, 'loginfmt')
            input_field.send_keys(username)

            # Press Enter to submit the username field
            input_field.send_keys(Keys.ENTER)

            WebDriverWait(self.driv, 10).until(EC.visibility_of_element_located((By.NAME, 'passwd')))
            input_field = self.driv.find_element(By.NAME, 'passwd')
            input_field.send_keys(password)

            # Click the Next button
            click_specific_btn(self.driv, 'id="idSIButton9"', 'input')

            # Wait for the Back button to be clickable
            WebDriverWait(self.driv, 10).until(EC.element_to_be_clickable((By.ID, 'idBtn_Back')))
            self.driv.find_element(By.ID, 'idBtn_Back').click()

        except Exception as e:
            print("An error occurred: ", e)

    def __willis_college_connection(self, willis_username: str, willis_password: str) -> None:
        """
        Full connection from willis college
        :param willis_username: willis college username
        :param willis_password: willis college password
        :return: None
        """
        self.driv.get(self.WILLIS_WEB_SITE)

        try:
            WebDriverWait(self.driv, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'img[alt="Sign in with Microsoft"]'))
            )
        except Exception as e:
            print("An error occurred: ", e)
        else:
            link = WebDriverWait(self.driv, 10).until(
                EC.presence_of_element_located((By.XPATH, '//img[@alt="Sign in with Microsoft"]/..'))
            )
            link.click()
            self.__microsoft_connection(willis_username, willis_password)

    def __willis_to_moodle(self) -> str:
        """
        Open moodle from willis college website
        :return: URL to open for the willis's moodle
        """
        try:
            WebDriverWait(self.driv, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Moodle')))
            self.driv.find_element(By.LINK_TEXT, 'Moodle').click()

            # Switch to the new tab
            self.driv.switch_to.window(self.driv.window_handles[-1])

            # Wait for the new tab to load
            WebDriverWait(self.driv, 10).until(EC.url_contains("moodle"))

            return self.driv.current_url
        except Exception as e:
            print("An error occurred: ", e)

    def __get_timeline_urls(self) -> list[str]:
        """
        Get the day of work
        :return: all the urls of the day
        """
        try:
            # Find all divs with the specified class
            divs = self.driv.find_elements(By.XPATH, '//div[@class="list-group-item timeline-event-list-item flex-column pt-2 pb-0 border-0 px-2" and @data-region="event-list-item"]')

            # For each div, find the 'a' tag and extract the href attribute (URL)
            return [div.find_element(By.TAG_NAME, 'a').get_attribute('href') for div in divs]

        except:
            return None

    def get_question_dict(self) -> dict:
        """
        In one page of a quiz get all the question and answer
        :return: dictionary of all the question and choice of answer
        """
        # Create BeautifulSoup object
        soup = BeautifulSoup(self.driv.page_source, 'html.parser')

        # Find all question divs
        question_divs = soup.find_all('div', class_='que')

        # Initialize dictionary to store questions and answers
        questions_dict = {}

        # Iterate over question divs
        for question_div in question_divs:
            # Extract question details
            question_id = question_div['id']
            question_text = question_div.find('div', class_='qtext').text.strip()

            # Extract answer options if available
            answer_divs = question_div.find_all('div', class_='answer')
            answer_text = []
            # Now, you can loop through these elements and extract the answer text
            for answer_div in answer_divs:
                answer_text.append(answer_div.get_text())

            # Store question details and answers in dictionary
            questions_dict[question_id] = {
                'question_text': question_text,
                'answers': answer_text if answer_text else None
            }
        return questions_dict

    def get_quiz(self, username, password) -> dict:
        """
        :param username: Username to connect at willis college's moodle
        :param password: Password to connect at willis college's moodle
        :return: dictionary with the question and answer of the quiz
        """
        self.__willis_college_connection(username, password)  # Connect to the willis website
        self.__willis_to_moodle()  # connect to moodle
        urls = self.__get_timeline_urls() # Find all the url for the task of the day
        for url in urls:  # if there is a match for a quiz it will open it
            # Switch to the current tab
            if re.fullmatch(self.QUIZ_DETECTION_REGEX, url):
                self.driv.get(url)  # open the quiz URL
                break

        click_specific_btn(self.driv, 'class="btn btn-primary"', 'button')  # Open the Quiz

        # NEED TO FIND A SOLUTION FOR THIS SHIT :
        self.driv.switch_to.window(self.driv.window_handles[-1])  # Switch to the newest tab (the quiz)

        WebDriverWait(self.driv, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'que')))  # whait for the quiz to be loaded

        return self.get_question_dict()  # FIND all the question and proposal answer



    # EXPERIMENT

    def write_underneath_qtext(self, qa_text: str):
        """
        Writes answers from the provided string underneath each 'qtext' div on the current webpage.
        The text of the 'qtext' div is used as a key to get the corresponding answer from the string.
        :param qa_text: A string containing questions and answers in the format "Question: ... Answer: ..."
        """
        # Split the text into question-answer pairs
        qa_pairs = re.findall(r"(?ms)(Question:.*?(?:Answer:|Answers:).*?)(?=Question:|$)", qa_text)

        # Convert the QA pairs into a dict
        qa_dict = {}
        for qa_pair in qa_pairs:
            # Split the QA pair into question and answer
            splitted = re.split("Answer:|Answers:", qa_pair, 1)
            if len(splitted) == 2:
                question, answer = splitted
                question = question.replace('Question:', '').strip()  # Clean up the question
                answer = answer.strip()  # Clean up the answer
                qa_dict[question] = answer

        # Find all 'qtext' divs on the page
        qtext_divs = self.driv.find_elements(By.CLASS_NAME, 'qtext')

        # For each 'qtext' div
        for qtext_div in qtext_divs:
            # Get the question text
            question = qtext_div.get_attribute('textContent').strip()

            # Find the corresponding answer in the dict
            answer = qa_dict.get(question, "")

            # If an answer was found, write it directly under the HTML page
            if answer:
                self.driv.execute_script("""
                    var p = document.createElement('p');
                    p.textContent = arguments[0];
                    p.style.color = 'green';
                    document.body.appendChild(p);
                """, answer)


def display(questions_dict):
        # Print the resulting dictionary
    for question_id, question_data in questions_dict.items():
        print(f"Question ID: {question_id}")
        print(f"Question Text: {question_data['question_text']}")
        if question_data['answers']:
            print("Answers:")
            for answer in question_data['answers']:
                print(answer)

def click_specific_btn(driv, attr_btn: str, tag_btn: str):
    try:
        # Wait for the button to be clickable
        button = WebDriverWait(driv, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f"{tag_btn}[{attr_btn}]")))
        # Click the button
        button.click()
    except:
        print("Button not found.")