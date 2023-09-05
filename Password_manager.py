from cryptography.fernet import Fernet
import os

class PasswordManager:
    def __init__(self, key_file):
        self.key_file = key_file
        self.key = self.load_or_generate_key()

    def load_or_generate_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as file:
                return file.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as file:
                file.write(key)
            return key

    def encrypt_password(self, password):
        cipher_suite = Fernet(self.key)
        encrypted_password = cipher_suite.encrypt(password.encode())
        return encrypted_password

    def decrypt_password(self, encrypted_password):
        cipher_suite = Fernet(self.key)
        decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
        return decrypted_password

def main():
    key_file = 'encryption_key.key'
    manager = PasswordManager(key_file)

    while True:
        print("1. Store Password")
        print("2. Retrieve Password")
        print("3. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            website = input("Enter website or app name: ")
            username = input("Enter username: ")
            password = input("Enter password: ")

            encrypted_password = manager.encrypt_password(password)
            with open(f"{website}.pwd", 'wb') as file:
                file.write(encrypted_password)

            print("Password stored successfully!")

        elif choice == '2':
            website = input("Enter website or app name: ")

            try:
                with open(f"{website}.pwd", 'rb') as file:
                    encrypted_password = file.read()
                    decrypted_password = manager.decrypt_password(encrypted_password)
                    print(f"Password for {website}: {decrypted_password}")
            except FileNotFoundError:
                print("Password not found!")

        elif choice == '3':
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
