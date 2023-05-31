import json
from modules.chatGPT import CHAT as ai
from modules.WillisConnections.WILLHANDLE import WILLHANDLE
import user_handling as user

def willis_user_creation(path_to_data):
    """
    Create a data file with Willis College user credentials.
    """
    if not user.data_detection(path_to_data):
        username = input("Enter your Willis email (e.g., 'bob.ross@students.williscollege.com'): ")
        password = input("Enter your Willis email password: ")
        file_password = input("Enter the file password: ")
        user.create_data_file(path_to_data, username, password, file_password)


def main():
    """
    Main control function to handle the program flow.
    """
    path = 'data.json'
    willis_user_creation(path)
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
        account['Willis_College_user']['username'],
        account['Willis_College_user']['password']
    )  # Retrieve the quiz questions from Moodle

    qa_text = bot.answer_handler(questions_dict)  # Get the QA text from the bot

    willis_handle.write_underneath_qtext(qa_text)  # Write the answers underneath each question

    input("Press Enter to end")


if __name__ == '__main__':
    main()
