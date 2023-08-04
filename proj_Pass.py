from cryptography.fernet import Fernet
import os

def generate_key():
    return Fernet.generate_key()

def write_key(key):
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    if os.path.exists("key.key"):
        with open("key.key", "rb") as key_file:
            return key_file.read()
    else:
        return generate_key()

def encrypt_password(password, key):
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password, key):
    cipher_suite = Fernet(key)
    decrypted_password = cipher_suite.decrypt(encrypted_password)
    return decrypted_password.decode()

def view_passwords(key):
    try:
        with open('passwords.txt', 'r') as f:
            for line in f:
                data = line.strip()
                user, passw = data.split("|")
                decrypted_passw = decrypt_password(passw.encode(), key)
                print(f"User: {user} | Password: {decrypted_passw}")
    except FileNotFoundError:
        print("Passwords file not found. Please add passwords first.")

def add_password(name, pwd, key):
    encrypted_passw = encrypt_password(pwd, key)
    with open('passwords.txt', 'a') as f:
        f.write(f"{name}|{encrypted_passw.decode()}\n")

def main():
    key = load_key()
    write_key(key)

    while True:
        mode = input(
            "Would you like to add a new password or view existing ones (view, add), press q to quit? ").lower()

        if mode == "q":
            break
        elif mode == "view":
            view_passwords(key)
        elif mode == "add":
            name = input('Account Name: ')
            pwd = input("Password: ")
            add_password(name, pwd, key)
        else:
            print("Invalid mode. Please try again.")

if __name__ == "__main__":
    main()