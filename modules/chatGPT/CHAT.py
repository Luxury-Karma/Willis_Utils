import time
import random
from telnetlib import EC
from typing import overload
from bs4 import *
import undetected_chromedriver as webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from modules.WillisConnections.WILLHANDLE import click_specific_btn


class CHAT_AI:
    def __init__(self, loginUrl=None, prompt=None, wait_time=None, minimal_wait_time=None):
        self.__driver = webdriver.Chrome()
        self.loginUrl = loginUrl or 'https://chat.openai.com/auth/login'
        self.prompt = prompt or 'Please provide the answer in the following format - Question: [question data], Answer: [your response]. Ensure that you strictly adhere to the given format and maintain accurate capitalization and punctuation. Reminder that when I give you somthing with options to answer look the one that answer the question'
        self.wait_time = wait_time or 10
        self.minimal_wait_time = minimal_wait_time or 2
    #region login

    #region logOptions
    def __log_chat_account(self,username:str, passwrd: str):
        self._connection_by_other_mean(username, 'email')
        self._connection_by_other_mean(passwrd,'password')

    def __other_login(self, username: str, password: str, search_word: str):
        # Wait for the buttons to load
        WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button')))
        time.sleep(self.minimal_wait_time)

        # Find all buttons
        buttons = self.__driver.find_elements(By.CSS_SELECTOR,'button')

        # Loop over the buttons and click on the one that contains the search word
        for button in buttons:
            if search_word.lower() in button.text.lower():
                button.click()
                break
        self._connection_by_other_mean(username, 'email')
        self._connection_by_other_mean(password, 'password')

    def _connection_by_other_mean(self, input_field: str,type_searched: str):
        WebDriverWait(self.__driver, self.wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))
        time.sleep(self.minimal_wait_time)
        # Find the email input field
        email_input = self.__driver.find_element(By.CSS_SELECTOR, f'input[type="{type_searched}"]')

        # Send keys to the email input field
        time.sleep(random.randint(1, 5))
        email_input.send_keys(input_field)
        email_input.send_keys(Keys.ENTER)

    #endregion
    def __log_chat_Microsoft(self,username:str,passwrd:str):
        pass

    def __log_chat_apple(self,username:str, passwrd:str):
        pass


    def __open_chat_tab(self, username: str, passwrd: str,account_type: str) -> None:
        """
        Connection with Open AI account
        :param username: Open AI linked email
        :param passwrd: Open AI password
        :return: None
        """

        self.__driver.get(self.loginUrl)
        WebDriverWait(self.__driver, self.wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#__next > div.flex.h-full.w-full.flex-col.items-center.justify-center.bg-gray-50.dark\:bg-gray-800 > div.w-96.flex.flex-col.flex-auto.justify-center.items-center > div.flex.flex-row.gap-3 > button:nth-child(1)')))
        click_specific_btn(self.__driver, 'class="btn relative btn-primary"', 'button')
        if account_type.lower() == 'account':
            self.__log_chat_account(username, passwrd)
        else:
            self.__other_login(username, passwrd, account_type)






    @staticmethod
    def waiting_for_connection():
        input("Tell me when your Chat GPT is connected and loaded by pressing Enter.")

    # endregion

    #region ChatInput
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
        WebDriverWait(self.__driver, 20).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        time.sleep(self.minimal_wait_time)

        #region Kill the shit box
        try:
            WebDriverWait(self.__driver, self.wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.absolute.inset-0')))
            self.__driver.execute_script(
                "var elem = document.querySelector('.absolute.inset-0'); elem.parentNode.removeChild(elem);")
        except Exception as e:
            print(f'The page was probably not there {e}')

        #endregion

        WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.ID, 'prompt-textarea')))
        input_field = self.__driver.find_element(By.ID, 'prompt-textarea')
        input_field.send_keys(question)
        #self.__driver.find_element(By.CSS_SELECTOR, '#__next > div.overflow-hidden.w-full.h-full.relative.flex.z-0 > div.relative.flex.h-full.max-w-full.flex-1.overflow-hidden > div > main > div.absolute.bottom-0.left-0.w-full.border-t.md\:border-t-0.dark\:border-white\/20.md\:border-transparent.md\:dark\:border-transparent.md\:bg-vert-light-gradient.bg-white.dark\:bg-gray-800.md\:\!bg-transparent.dark\:md\:bg-vert-dark-gradient.pt-2 > form > div > div > button').click()
        input_field.send_keys(Keys.TAB)
        input_field.send_keys(Keys.ENTER)  # Should allways select the send key and press enter to send the question


    def __get_answer(self):
        answer_element = self.__driver.find_element(By.CSS_SELECTOR,
                                                    "div.markdown.prose.w-full.break-words.dark\:prose-invert.light")
        paragraphs = answer_element.find_elements(By.TAG_NAME, "p")
        answer = " ".join([paragraph.text for paragraph in paragraphs])
        print(f'The answer of Chat GPT is: {answer}')
        return answer
    #endregion
    def answer_handler(self, question: dict, usrname: str, passwrd: str, type_of_account: str):
        self.__open_chat_tab(usrname, passwrd, type_of_account)
        ask = self.__creating_question_formula(question)
        #self.waiting_for_connection()
        self.__pasting_question(ask.replace('\n', ''))
        input('Press Enter when the answer is over.')
        input('Are you sure?')
        return self.__get_answer()
