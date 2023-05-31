import os
import json
from cryptography.fernet import Fernet
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os
import warnings
import base64


def data_detection(path_to_create):
    """
    Ensure that the file with the user data exists
    :return: if the file exists
    """
    return os.path.isfile(path_to_create)


def add_data_for_willis_connection(username: str, password: str):
    return {'wUsername': username, 'wPassword': password}


def willis_account_creation(username: str, password: str):
    return {'Willis_College_user': {'username': username, 'password': password}}


def create_data_file(path_to_data, username: str, password: str, filePassword: str):
    data = willis_account_creation(username, password)
    # Create the file initially
    with open(path_to_data, 'w') as f:
        json.dump(data, f)
        f.flush()
    base_key, base_salt = generate_base_key_and_salt()
    save_key_and_salt_to_file(base_key, base_salt, '../../decryption.txt')
    encrypt_file(path_to_data, filePassword, base_key, base_salt)


def generate_base_key_and_salt():
    base_key = Fernet.generate_key()
    base_salt = os.urandom(16)
    return base_key, base_salt


import base64

def derive_key(base_key, base_salt, password, iterations=100000):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=base_salt,
        iterations=iterations,
        backend=default_backend()
    )
    derived_key = kdf.derive(b''.join([base_key, bytes(password.encode('UTF-8'))]))
    derived_key_base64 = base64.urlsafe_b64encode(derived_key)
    return derived_key_base64





def save_key_and_salt_to_file(key, salt, filename):
    key_encoded = base64.urlsafe_b64encode(key).decode('utf-8')
    salt_encoded = base64.urlsafe_b64encode(salt).decode('utf-8')
    with open(filename, 'w') as file:
        file.write(key_encoded)
        file.write('\n')  # Add a newline to separate key and salt
        file.write(salt_encoded)


def load_key_and_salt_from_file(filename):
    with open(filename, 'r') as file:
        key_encoded = file.readline().strip()
        salt_encoded = file.readline().strip()
    key = base64.urlsafe_b64decode(key_encoded)
    salt = base64.urlsafe_b64decode(salt_encoded)
    return key, salt


def encrypt_file(filename, password, base_key, base_salt):
    cipher = Fernet(derive_key(base_key, base_salt, password))

    with open(filename, 'rb') as file:
        file_data = file.read()

    encrypted_data = cipher.encrypt(file_data)

    with open(filename, 'wb') as encrypted_file:
        encrypted_file.write(base_salt + encrypted_data)

    print(f"File '{filename}' encrypted successfully. Encrypted file: '{filename}'")


def decrypt_data(encrypted_data, password, base_key, base_salt):
    cipher = Fernet(derive_key(base_key, base_salt, password))

    encrypted_data = encrypted_data[16:]  # Extract the encrypted data from the file

    decrypted_data = cipher.decrypt(encrypted_data)

    return decrypted_data

