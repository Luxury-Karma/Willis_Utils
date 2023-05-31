import time
import random
from telnetlib import EC
import undetected_chromedriver as webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from modules.WillisConnections.WILLHANDLE import click_specific_btn


class CHAT_AI:
    def __init__(self, loginUrl=None, prompt=None):
        self.__driver = webdriver.Chrome()
        self.loginUrl = loginUrl or 'https://chat.openai.com/auth/login'
        self.prompt = prompt or 'Please provide the answer in the following format - Question: [question data], Answer: [your response]. Ensure that you strictly adhere to the given format and maintain accurate capitalization and punctuation. Reminder that when I give you somthing with options to answer look the one that answer the question'

    def __open_chat_tab(self, username: str, passwrd: str):
        self.__driver.get(self.loginUrl)
        WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#__next > div.flex.h-full.w-full.flex-col.items-center.justify-center.bg-gray-50.dark\:bg-gray-800 > div.w-96.flex.flex-col.flex-auto.justify-center.items-center > div.flex.flex-row.gap-3 > button:nth-child(1)')))
        click_specific_btn(self.__driver, 'class="btn relative btn-primary"', 'button')

        CSS_Selector = '#username'
        WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, CSS_Selector)))
        input_field = self.__driver.find_element(By.CSS_SELECTOR, CSS_Selector)
        time.sleep(random.randint(1, 3))
        input_field.send_keys(username)
        time.sleep(random.randint(1, 5))
        input_field.send_keys(Keys.ENTER)

        CSS_Selector = '#password'
        WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, CSS_Selector)))
        input_field = self.__driver.find_element(By.CSS_SELECTOR, CSS_Selector)
        time.sleep(random.randint(1, 3))
        input_field.send_keys(passwrd)
        time.sleep(random.randint(1, 5))
        input_field.send_keys(Keys.ENTER)


        input('Remove the anoying page ')


    @staticmethod
    def waiting_for_connection():
        input("Tell me when your Chat GPT is connected and loaded by pressing Enter.")

    def __creating_question_formula(self, question_information):
        question = self.prompt + '. '
        for _, question_data in question_information.items():
            question += f"Question Text: {question_data['question_text']}"
            if question_data['answers']:
                question += "Answers:"
                for answer in question_data['answers']:
                    question += ' ' + answer + ', '
        print(f'The question will be: {question}')
        return question

    def __pasting_question(self, question):
        WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.ID, 'prompt-textarea')))
        self.__driver.find_element(By.ID, 'prompt-textarea').send_keys(question)
        self.__driver.find_element(By.CSS_SELECTOR, '#__next > div.overflow-hidden.w-full.h-full.relative.flex.z-0 > div.relative.flex.h-full.max-w-full.flex-1.overflow-hidden > div > main > div.absolute.bottom-0.left-0.w-full.border-t.md\:border-t-0.dark\:border-white\/20.md\:border-transparent.md\:dark\:border-transparent.md\:bg-vert-light-gradient.bg-white.dark\:bg-gray-800.md\:\!bg-transparent.dark\:md\:bg-vert-dark-gradient.pt-2 > form > div > div > button').click()

    def __get_answer(self):
        answer_element = self.__driver.find_element(By.CSS_SELECTOR,
                                                    "div.markdown.prose.w-full.break-words.dark\:prose-invert.light")
        paragraphs = answer_element.find_elements(By.TAG_NAME, "p")
        answer = " ".join([paragraph.text for paragraph in paragraphs])
        print(f'The answer of Chat GPT is: {answer}')
        return answer

    def answer_handler(self, question: dict, usrname: str, passwrd: str):
        self.__open_chat_tab(usrname, passwrd)
        ask = self.__creating_question_formula(question)
        #self.waiting_for_connection()
        self.__pasting_question(ask.replace('\n', ''))
        input('Press Enter when the answer is over.')
        input('Are you sure?')
        return self.__get_answer()
