import json
#from modules.WillisConnections import WILLHANDLE
from Willis_Utils.modules.WillisConnections.WILLHANDLE import  WILLHANDLE
from Willis_Utils.modules.chatGPT import CHAT as ai
import user_handeling as user

def menu():
    """
    Show the user all the options he can choose of
    :return:
    """
    pass


def willis_user_creation(path_to_data):
    if not user.data_detection(path_to_data):
        username: str = input('Enter the willis email exemple : \'bob.ross@students.williscollege.com\': ')
        password: str = input('Enter you\'re willis email password: ')
        fPassword: str = input('Enter the file password')
        user.create_data_file(path_to_data, username, password, fPassword)



'''

def main():
    question_information = {
        '1': {
            'question_text': 'What is your favorite color?',
            'answers': ['Blue', 'Red', 'Green']
        },
        '2': {
            'question_text': 'How old are you?',
            'answers': []
        },
        '3': {
            'question_text': 'What is your favorite animal?',
            'answers': ['Dog', 'Cat', 'Elephant']
        }
    }

    bot = ai.CHAT_AI()
    print(bot.answer_handler(question_information))
'''

def main():
    """
    Act as the main control of the user for the program.
    Handle the script and the user options
    :return:
    """
    path: str = 'data.json'
    willis_user_creation(path)
    password = input('password for file')
    key, salt = user.load_key_and_salt_from_file('decryption.txt')

    account: dict
    with open(path, 'rb') as file:
        file_data = file.read()  # Read data from the file
        decrypted_data = user.decrypt_data(file_data, password, key, salt)
        decrypted_data_str = decrypted_data.decode('utf-8')  # Convert bytes to string
        account = json.loads(decrypted_data_str)  # Load JSON from string
    willis_handle = WILLHANDLE()
    willis_handle.get_quiz(account['Willis_College_user']['username'], account['Willis_College_user']['password'])  # Connect to willis college
    bot = ai.CHAT_AI()
    bot.answer_handler(willis_handle.get_question_dict())









if __name__ == '__main__':
    main()