import time
import urllib
from urllib.parse import urlparse
from bs4 import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re


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

            WebDriverWait(self.driv, 10).until(EC.url_contains("moodle"))

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
        qa_pairs = self.extract_qa_pairs(qa_text)
        qtext_divs = self.driv.find_elements(By.CLASS_NAME, 'qtext')
        for i, qtext_div in enumerate(qtext_divs):
            question = self.get_question_text(qtext_div)
            answer = self.find_corresponding_answer(question, qa_pairs)
            if answer:
                search_query = self.create_search_query(question)
                self.perform_google_search(search_query)
                time.sleep(3)
                search_results = self.get_search_results()
                result_titles, result_urls = self.extract_search_result_info(search_results)
                search_results_text = self.format_search_results(result_titles, result_urls)
                self.insert_search_results(search_results_text, qtext_div)

    def extract_qa_pairs(self, qa_text: str):
        qa_pairs = re.findall(r"(?ms)(Question:.*?(?:Answer:|Answers:).*?)(?=Question:|$)", qa_text)
        return qa_pairs

    def get_question_text(self, qtext_div):
        question = qtext_div.get_attribute('textContent').strip()
        return question

    def find_corresponding_answer(self, question, qa_pairs):
        answer = None
        for qa_pair in qa_pairs:
            if question in qa_pair:
                answer = re.split("Answer:|Answers:", qa_pair, 1)[1].strip()
                break
        return answer

    def create_search_query(self, question):
        search_query = f"{question} site:google.com"
        return search_query

    def perform_google_search(self, search_query):
        search_input = self.driv.find_element(By.NAME, 'q')
        search_input.clear()
        search_input.send_keys(search_query)
        search_input.submit()

    def get_search_results(self):
        search_results = self.driv.find_elements(By.CSS_SELECTOR, 'div.g')
        return search_results

    def extract_search_result_info(self, search_results):
        result_titles = []
        result_urls = []
        for result in search_results:
            title_element = result.find_element(By.CSS_SELECTOR, 'h3')
            url_element = result.find_element(By.CSS_SELECTOR, 'a')

            title = title_element.get_attribute('textContent')
            url = url_element.get_attribute('href')

            result_titles.append(title)
            result_urls.append(url)
        return result_titles, result_urls

    def format_search_results(self, result_titles, result_urls):
        search_results_text = ''
        for title, url in zip(result_titles, result_urls):
            search_results_text += f"<a href='{url}' target='_blank'>{title}</a><br>"
        return search_results_text

    def insert_search_results(self, search_results_text, qtext_div):
        script = """
            var div = document.createElement('div');
            div.innerHTML = arguments[0];
            arguments[1].insertAdjacentElement('afterend', div);
        """
        self.driv.execute_script(script, search_results_text, qtext_div)
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
