import re
import urllib
from urllib.parse import urlparse
from bs4 import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WILLHANDLE:
    def __init__(self, WILLIS_WEB_SITE=None, QUIZ_DETECTION_REGEX=None):
        self.QUIZ_DETECTION_REGEX = QUIZ_DETECTION_REGEX if QUIZ_DETECTION_REGEX else r'^https:\/\/students\.willisonline\.ca\/mod\/quiz\/.*$'
        self.WILLIS_WEB_SITE = WILLIS_WEB_SITE if WILLIS_WEB_SITE else "https://willisonline.ca/login"
        self.driv = webdriver.Chrome()

    # region connect to the website
    def __microsoft_connection(self, username: str, password: str) -> None:
        try:
            WebDriverWait(self.driv, 10).until(EC.presence_of_element_located((By.NAME, 'loginfmt')))
            input_field = self.driv.find_element(By.NAME, 'loginfmt')
            input_field.send_keys(username)
            input_field.send_keys(Keys.ENTER)

            WebDriverWait(self.driv, 15).until(EC.visibility_of_element_located((By.NAME, 'passwd')))
            input_field = self.driv.find_element(By.NAME, 'passwd')
            input_field.send_keys(password)

            click_specific_btn(self.driv, 'id="idSIButton9"', 'input')

            WebDriverWait(self.driv, 15).until(EC.element_to_be_clickable((By.ID, 'idBtn_Back')))
            self.driv.find_element(By.ID, 'idBtn_Back').click()

        except Exception as e:
            print("An error occurred: ", e)

    def __willis_college_connection(self, willis_username: str, willis_password: str) -> None:
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
        try:
            WebDriverWait(self.driv, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Moodle')))
            self.driv.find_element(By.LINK_TEXT, 'Moodle').click()

            self.driv.switch_to.window(self.driv.window_handles[-1])

            return self.driv.current_url
        except Exception as e:
            print("An error occurred: ", e)

    def __get_timeline_urls(self) -> list[str]:
        try:
            divs = self.driv.find_elements(By.XPATH, '//div[@class="list-group-item timeline-event-list-item flex-column pt-2 pb-0 border-0 px-2" and @data-region="event-list-item"]')
            return [div.find_element(By.TAG_NAME, 'a').get_attribute('href') for div in divs]
        except:
            return None
    # endregion

    # region get quiz data
    def get_question_dict(self) -> dict:
        soup = BeautifulSoup(self.driv.page_source, 'html.parser')
        question_divs = soup.find_all('div', class_='que')
        questions_dict = {}
        for question_div in question_divs:
            question_id = question_div['id']
            question_text = question_div.find('div', class_='qtext').text.strip()

            answer_divs = question_div.find_all('div', class_='answer')
            answer_text = []
            for answer_div in answer_divs:
                answer_text.append(answer_div.get_text())

            questions_dict[question_id] = {
                'question_text': question_text,
                'answers': answer_text if answer_text else None
            }
        return questions_dict

    def get_quiz(self, username, password) -> dict:
        self.__willis_college_connection(username, password)
        self.__willis_to_moodle()
        urls = self.__get_timeline_urls()
        for url in urls:
            if re.fullmatch(self.QUIZ_DETECTION_REGEX, url):
                self.driv.get(url)
                break

        click_specific_btn(self.driv, 'class="btn btn-primary"', 'button')

        self.driv.switch_to.window(self.driv.window_handles[-1])

        WebDriverWait(self.driv, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'que')))

        return self.get_question_dict()
    # endregion

    # region apply webpage data
    def write_underneath_qtext(self, qa_text: str):
        """
        Writes answers from the provided string underneath each 'qtext' div on the current webpage.
        The text of the 'qtext' div is used as a key to get the corresponding answer from the string.
        :param qa_text: A string containing questions and answers in the format "Question: ... Answer: ..."
        """
        # Split the text into question-answer pairs
        qa_pairs = re.findall(r"(?ms)(Question:.*?(?:Answer:|Answers:).*?)(?=Question:|$)", qa_text)

        # Find all 'qtext' divs on the page
        qtext_divs = self.driv.find_elements(By.CLASS_NAME, 'qtext')

        # For each 'qtext' div
        for i, qtext_div in enumerate(qtext_divs):
            # Get the question text
            question = qtext_div.get_attribute('textContent').strip()

            # Find the corresponding answer in the QA pairs
            answer = None
            for qa_pair in qa_pairs:
                if question in qa_pair:
                    answer = re.split("Answer:|Answers:", qa_pair, 1)[1].strip()
                    break

            # If an answer was found, write it directly under the 'qtext' div
            if answer:
                # Create a link to Google search with the question
                search_query = urllib.parse.quote(question)
                google_search_link = f"https://www.google.com/search?q={search_query}"
                answer_with_link = f"{answer} <a href='{google_search_link}' target='_blank'>[Search on Google]</a>"

                script = """
                    var p = document.createElement('p');
                    p.innerHTML = arguments[0];
                    p.style.color = 'green';
                    arguments[1].parentNode.insertBefore(p, arguments[1].nextSibling);
                """
                self.driv.execute_script(script, answer_with_link, qtext_div)
    # endregion

def display(questions_dict):
    for question_id, question_data in questions_dict.items():
        print(f"Question ID: {question_id}")
        print(f"Question Text: {question_data['question_text']}")
        if question_data['answers']:
            print("Answers:")
            for answer in question_data['answers']:
                print(answer)

def click_specific_btn(driv, attr_btn: str, tag_btn: str):
    try:
        button = WebDriverWait(driv, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"{tag_btn}[{attr_btn}]")))
        button.click()
    except:
        print("Button not found.")
