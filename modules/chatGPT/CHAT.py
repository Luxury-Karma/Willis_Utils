
from telnetlib import EC
import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait



class CHAT_AI:

    def __init__(self, loginUrl = None, prompt = None):
        """
        In normal use you should not change them
        :param loginUrl: on which website i am suppose to be log to
        :param prompt: what am i saying in aditional of the question and answer of chat gpt
        """
        self.__driver = webdriver.Chrome()
        self.loginUrl: str = loginUrl if loginUrl else 'https://chat.openai.com/auth/login'  # send to the loggin page of OPENAI
        # PROMPT WILL NEED TO BE OPTIMISE AF
        self.prompt: str = prompt if prompt else 'You will allways give an answer. If I gave you options then it is a mutiple choice.' \
                                                 'tell me wich one you choose only and no explenation of why.' \
                                                 'if it is not a multiple choice write Short answer : Question :  question text under write the answer. Keep in mind you NEED to give me an answer' \
                                                 'For the multiple choice you will give me only the ones you selected and nothing else. In this way : Question number, Question and under the answer.' \
                                                 'If in any question there is more than one answer you will NOT put the word answer more than once.' \
                                                 'FINALY remember to NEVER only answer give me allways the question before'

    def __open_chat_tab(self) -> None:
        """
        Open the tabs of Chat GPT
        :return: None
        """
        self.__driver.get(self.loginUrl)  # oppen OPENAI connection



    def __creating_question_formula(self, question_information: dict) -> str:
        """
        Create the prompt to ask the tabs in chat GPT with the persona
        :return: string
        """
        question = ''
        question = question + self.prompt + '. '
        for _, question_data in question_information.items():
            question = question + f"Question Text: {question_data['question_text']}"
            if question_data['answers']:
                question = question + "Answers:"
                for answer in question_data['answers']:
                    question = question + ' ' + answer + ', '
        print(f'The question will be : {question}')
        return question

    def __pasting_question(self, question: str) -> None :
        """
        Send the question to the correct emplacement in the chat GPT tabs
        :return: None
        """
        WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.ID, 'prompt-textarea')))
        self.__driver.find_element(By.ID, 'prompt-textarea').send_keys(question)  # Write the question
        self.__driver.find_element(By.CSS_SELECTOR, '#__next > div.overflow-hidden.w-full.h-full.relative.flex.z-0 > div.relative.flex.h-full.max-w-full.flex-1.overflow-hidden > div > main > div.absolute.bottom-0.left-0.w-full.border-t.md\:border-t-0.dark\:border-white\/20.md\:border-transparent.md\:dark\:border-transparent.md\:bg-vert-light-gradient.bg-white.dark\:bg-gray-800.md\:\!bg-transparent.dark\:md\:bg-vert-dark-gradient.pt-2 > form > div > div.flex.flex-col.w-full.py-2.flex-grow.md\:py-3.md\:pl-4.relative.border.border-black\/10.bg-white.dark\:border-gray-900\/50.dark\:text-white.dark\:bg-gray-700.rounded-md.shadow-\[0_0_10px_rgba\(0\,0\,0\,0\.10\)\].dark\:shadow-\[0_0_15px_rgba\(0\,0\,0\,0\.10\)\] > button').click()  # Ensure that the question is send

    def __get_answer(self) -> str:
        """
        Get the answer of CHAT GPT
        :return: answer
        """

        # TAKING THE ANSWER
        answer_element = self.__driver.find_element(By.CSS_SELECTOR,
                                                    "div.markdown.prose.w-full.break-words.dark\:prose-invert.light")
        paragraphs = answer_element.find_elements(By.TAG_NAME, "p")

        answer = " ".join([paragraph.text for paragraph in paragraphs])

        print(f'The answer of chat GPT is: {answer}')
        return answer

    def answer_handler(self, question: dict) -> str:
        """
        Get a question and will return the answer for you !
        :return: None
        """
        self.__open_chat_tab()  # open the driver
        ask = self.__creating_question_formula(question)  # create the prompt for chat GPT
        waiting_for_connection()  # whait for the connection
        self.__pasting_question(ask.replace('\n', ''))  # past the question inside the prompt and send it
        input('press enter when the answer is over')
        input('are you sur?')
        return self.__get_answer()  # get the answer


def waiting_for_connection():
    """
    Wait for the user to connect when the user is connected when connected press enter and continue the script
    :return: None
    """
    input('Tell me when you\' chat GTP is connected and loaded by pressing enter')




