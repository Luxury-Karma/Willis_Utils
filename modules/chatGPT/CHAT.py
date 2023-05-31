from telnetlib import EC
import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class CHAT_AI:
    def __init__(self, loginUrl=None, prompt=None):
        self.__driver = webdriver.Chrome()
        self.loginUrl = loginUrl or 'https://chat.openai.com/auth/login'
        self.prompt = prompt or 'Please provide the answer in the following format - Question: [question data], Answer: [your response]. Ensure that you strictly adhere to the given format and maintain accurate capitalization and punctuation.'

    def __open_chat_tab(self):
        self.__driver.get(self.loginUrl)

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
        self.__driver.find_element(By.CSS_SELECTOR, '#__next > div.overflow-hidden.w-full.h-full.relative.flex.z-0 > div.relative.flex.h-full.max-w-full.flex-1.overflow-hidden > div > main > div.absolute.bottom-0.left-0.w-full.border-t.md\:border-t-0.dark\:border-white\/20.md\:border-transparent.md\:dark\:border-transparent.md\:bg-vert-light-gradient.bg-white.dark\:bg-gray-800.md\:\!bg-transparent.dark\:md\:bg-vert-dark-gradient.pt-2 > form > div > div.flex.flex-col.w-full.py-2.flex-grow.md\:py-3.md\:pl-4.relative.border.border-black\/10.bg-white.dark\:border-gray-900\/50.dark\:text-white.dark\:bg-gray-700.rounded-md.shadow-\[0_0_10px_rgba\(0\,0\,0\,0\.10\)\].dark\:shadow-\[0_0_15px_rgba\(0\,0\,0\,0\.10\)\] > button').click()

    def __get_answer(self):
        answer_element = self.__driver.find_element(By.CSS_SELECTOR,
                                                    "div.markdown.prose.w-full.break-words.dark\:prose-invert.light")
        paragraphs = answer_element.find_elements(By.TAG_NAME, "p")
        answer = " ".join([paragraph.text for paragraph in paragraphs])
        print(f'The answer of Chat GPT is: {answer}')
        return answer

    def answer_handler(self, question):
        self.__open_chat_tab()
        ask = self.__creating_question_formula(question)
        self.waiting_for_connection()
        self.__pasting_question(ask.replace('\n', ''))
        input('Press Enter when the answer is over.')
        input('Are you sure?')
        return self.__get_answer()
