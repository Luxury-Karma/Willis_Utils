import WillisConnections
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


def main():
    """
    Act as the main control of the user for the program.
    Handle the script and the user options
    :return:
    """
    path: str = 'data.json'
    willis_user_creation(path)
    password = input('password for filr')
    key, salt = user.load_key_and_salt_from_file()
    account = user.decrypt_file(path, password, )
    WillisConnections.total_connection()




if __name__ == '__main__':
    main()