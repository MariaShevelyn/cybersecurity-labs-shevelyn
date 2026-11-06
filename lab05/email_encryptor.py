import base64
import os
import smtplib

from email.message import EmailMessage
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# ключ
def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000
    )

    key = base64.urlsafe_b64encode(
        kdf.derive(password.encode("utf-8"))
    )

    return key

# шифрування
def encrypt_message(message, password):
    salt = os.urandom(16)

    key = generate_key(password, salt)

    cipher = Fernet(key)
    encrypted = cipher.encrypt(message.encode("utf-8"))

    result = (
        base64.urlsafe_b64encode(salt).decode("utf-8")
        + ":"
        + encrypted.decode("utf-8")
    )

    return result

# розшифрування
def decrypt_message(encrypted_message, password):
    salt_text, encrypted_text = encrypted_message.strip().split(":", 1)

    salt = base64.urlsafe_b64decode(salt_text)

    key = generate_key(password, salt)

    cipher = Fernet(key)

    decrypted = cipher.decrypt(encrypted_text.encode("utf-8"))

    return decrypted.decode("utf-8")

def send_email(sender, app_password, receiver, encrypted_message):
    email = EmailMessage()

    email["Subject"] = "Зашифроване повідомлення"
    email["From"] = sender
    email["To"] = receiver

    email.set_content(
        "Вам надійшло зашифроване повідомлення:\n"
        + encrypted_message
        + "\n\n"
        "Для розшифрування використовуйте спільне секретне слово."
    )

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
        server.set_debuglevel(0)

        server.starttls()

        server.login(sender, app_password)

        server.send_message(email)

def send_message():
    print("\n           --Надсилання повідомлення--")

    sender = input("Ваша Gmail-адреса: ").strip()

    app_password = input("Пароль додатка Gmail: ").replace(" ", "")

    receiver = input("Gmail-адреса отримувача: ").strip()

    password = input("Спільне секретне слово: ")

    message = input("\nВведіть текст повідомлення: ")

    if not sender or not receiver or not password or not message.strip():
        print("\nПомилка. Заповніть усі поля!")
        return

    encrypted = encrypt_message(message, password)

    print("Повідомлення успішно зашифровано!")

    print("\nЗашифрований текст:")
    print(encrypted)

    try:
        send_email(sender, app_password, receiver, encrypted)

        print("\nЛист надіслано отримувачу!")

    except smtplib.SMTPAuthenticationError:
        print("\nПомилка авторизації Gmail!")

    except Exception as error:
        print("\nНе вдалося надіслати повідомлення")
        print("Причина помилки:", error)


# розшифрування
def receive_message():
    print("\n           --Отримання повідомлення--")

    encrypted = input("Вставте зашифроване повідомлення: ")

    password = input("Введіть спільне секретне слово: ")

    if not encrypted.strip() or not password:
        print("\nПомилкая Заповніть усі поля!")
        return

    try:
        decrypted = decrypt_message(encrypted, password)

        print("\nПовідомлення успішно розшифровано!")
        print(decrypted)

    except (InvalidToken, ValueError):
        print("\nПомилка! Неправильне секретне слово")

def main():
    while True:
        print("\n           --EMAIL-ШИФРАТОР--")
        print("1. Зашифрувати та надіслати повідомлення")
        print("2. Розшифрувати отримане повідомлення")
        print("0. Вихід")

        choice = input("\nОберіть дію: ")

        if choice == "1":
            send_message()

        elif choice == "2":
            receive_message()

        elif choice == "0":
            print("\nРоботу програми завершено")
            break

        else:
            print("\nНеправильний вибір")

if __name__ == "__main__":
    main()
