import json
from modules.chatGPT import CHAT as ai
from modules.WillisConnections.WILLHANDLE import WILLHANDLE
from modules.users import user_handeling as user


def user_creation(path_to_data):
    """
    Create a data file with Willis College user credentials.
    """
    if not user.data_detection(path_to_data):
        accounts = {}

        # Add Willis College account
        willis_username = input("Enter your Willis email (e.g., 'bob.ross@students.williscollege.com'): ")
        willis_password = input("Enter your Willis email password: ")
        willis_account = {
            'username': willis_username,
            'password': willis_password,
        }
        accounts['Willis'] = willis_account

        # Add OpenAI account
        openai_username = input("Enter your OpenAI email (e.g., 'bob.ross@gmail.com'): ")
        openai_password = input("Enter your OpenAI email password: ")
        openai_type_of_connection = input("Which way do you login (google, Microsoft, Apple, OpenAI): ")
        openai_account = {
            'username': openai_username,
            'password': openai_password,
        }
        accounts['OpenAI'] = openai_account

        filePassword = input("Enter the file password: ")

        # Create the data file
        with open(path_to_data, 'w') as f:
            json.dump(accounts, f)
            f.flush()

        base_key, base_salt = user.generate_base_key_and_salt()
        user.save_key_and_salt_to_file(base_key, base_salt, 'decryption.txt')
        user.encrypt_file(path_to_data, filePassword, base_key, base_salt)



#TESTING THE CHAT AUTO LOG

def main():
    questions_dict = {
        'question1': {
            'question_text': "How many syslog severity levels are there?",
            'answers': ['a. 0', 'b. 1', 'c. 2', 'd. 3', 'e. 4', 'f. 5', 'g. 6', 'h. 7', 'i. 8']
        },
        'question2': {
            'question_text': "Which of the following can be included as part of the event message when using the logger tool?",
            'answers': ['a. timestamp', 'b. user', 'c. host', 'd. message', 'e. service', 'f. target']
        },
        'question3': {
            'question_text': "True or False: The systemd.journald service doesn't use logging to store messages.",
            'answers': ['True', 'False']
        },
        'question4': {
            'question_text': "Which of the following packet information can be reviewed by a firewall?",
            'answers': ['a. Source IP address', 'b. Destination IP address', 'c. Protocol', 'd. Ingress port',
                        'e. Egress port', 'f. None of the above', 'g. Only A and B', 'h. Only D and E']
        },
        'question5': {
            'question_text': "True or False: The only actions that can be associated with a received packet are Accept, Reject and Block.",
            'answers': ['True', 'False']
        }
    }
    chat_user = ''
    chat_passwrd = ''
    bot = ai.CHAT_AI()
    answ = bot.answer_handler(questions_dict, chat_user, chat_passwrd, 'google')
    input('over')
'''
def main():
    """
    Main control function to handle the program flow.
    """
    path = 'data.json'
    user_creation(path)
    password = input("Enter the file password: ")
    key, salt = user.load_key_and_salt_from_file('decryption.txt')

    with open(path, 'rb') as file:
        file_data = file.read()  # Read data from the file
        decrypted_data = user.decrypt_data(file_data, password, key, salt)
        decrypted_data_str = decrypted_data.decode('utf-8')  # Convert bytes to string
        account = json.loads(decrypted_data_str)  # Load JSON from string

    willis_handle = WILLHANDLE()  # Create the object that interacts with Willis College and Moodle
    bot = ai.CHAT_AI()  # Create the object that interacts with Chat GPT

    questions_dict = willis_handle.get_quiz(
        account['Willis']['username'],
        account['Willis']['password']
    )  # Retrieve the quiz questions from Moodle

    qa_text = bot.answer_handler(questions_dict,
                                 account['OpenAI']['username'],
                                 account['OpenAI']['password'])  # Get the QA text from the bot

    willis_handle.write_underneath_qtext(qa_text)  # Write the answers underneath each question

    input("Press Enter to end")

'''
if __name__ == '__main__':
    main()


