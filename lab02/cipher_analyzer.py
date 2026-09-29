ENGLISH_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def caesar_key_from_birth_date(birth_date):
    digits = [int(char) for char in birth_date if char.isdigit()]
    return sum(digits)

def caesar_encrypt(text, shift):
    result = ""

    for char in text.upper():
        if char in ENGLISH_ALPHABET:
            index = ENGLISH_ALPHABET.index(char)
            new_index = (index + shift) % len(ENGLISH_ALPHABET)
            result += ENGLISH_ALPHABET[new_index]
        else:
            result += char

    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

def prepare_vigenere_key(key):
    key = key.upper()

    clean_key = ""

    for char in key:
        if char in ENGLISH_ALPHABET:
            clean_key += char

    return clean_key

def vigenere_encrypt(text, key):
    key = prepare_vigenere_key(key)

    if not key:
        return text

    result = ""
    key_index = 0

    for char in text.upper():

        if char in ENGLISH_ALPHABET:

            text_index = ENGLISH_ALPHABET.index(char)

            key_char = key[key_index % len(key)]
            key_shift = ENGLISH_ALPHABET.index(key_char)

            new_index = (text_index + key_shift) % len(ENGLISH_ALPHABET)

            result += ENGLISH_ALPHABET[new_index]

            key_index += 1

        else:
            result += char

    return result

def vigenere_decrypt(text, key):
    key = prepare_vigenere_key(key)

    if not key:
        return text

    result = ""
    key_index = 0

    for char in text.upper():

        if char in ENGLISH_ALPHABET:

            text_index = ENGLISH_ALPHABET.index(char)

            key_char = key[key_index % len(key)]
            key_shift = ENGLISH_ALPHABET.index(key_char)

            new_index = (text_index - key_shift) % len(ENGLISH_ALPHABET)

            result += ENGLISH_ALPHABET[new_index]

            key_index += 1

        else:
            result += char

    return result

def compare_algorithms(
        original_text,
        caesar_encrypted,
        vigenere_encrypted,
        caesar_key,
        vigenere_key
):
    print("\n" + "-" * 65)
    print("           Порівняльний аналіз")
    print(f"Довжина початкового тексту: {len(original_text)} символів")

    print("Шифр Цезаря:")
    print(f"  Ключ: {caesar_key}")
    print(f"  Довжина зашифрованого тексту: {len(caesar_encrypted)} символів")
    print("  Тип ключа: числовий зсув")

    print("Шифр Віженера:")
    print(f"  Ключ: {vigenere_key}")
    print(f"  Довжина зашифрованого тексту: {len(vigenere_encrypted)} символів")
    print("  Тип ключа: текстовий багатосимвольний ключ")

    print("\nВисновок:")
    print("  Шифр Цезаря простий у реалізації та використанні,")
    print("  але має невелику кількість можливих ключів.")

    print("  Шифр Віженера використовує послідовність символів ключа,")
    print("  тому є складнішим за шифр Цезаря.")

def main():
    print("            Програма порівняння класичних шифрів")
    print("У програмі використовуються:")
    print("1. Шифр Цезаря")
    print("2. Шифр Віженера")

    print("-" * 65)
    surname = input("Введіть прізвище: ")
    birth_date = input("Введіть дату народження: ")
    text = input("Введіть текст для шифрування: ")

    caesar_key = caesar_key_from_birth_date(birth_date)
    vigenere_key = prepare_vigenere_key(surname)

    if not vigenere_key:
        print("\nПрізвище повинно містити англійські літери!")
        return

    caesar_encrypted = caesar_encrypt(text, caesar_key)
    vigenere_encrypted = vigenere_encrypt(text, vigenere_key)

    caesar_decrypted = caesar_decrypt(
        caesar_encrypted,
        caesar_key
    )

    vigenere_decrypted = vigenere_decrypt(
        vigenere_encrypted,
        vigenere_key
    )

    print("\n" + "-" * 65)
    print("             Результати шифрування")
    print("Початковий текст:")
    print(text)

    print("\n           Шифр Цезаря")
    print(f"Ключ: {caesar_key}")
    print("Зашифрований текст:")
    print(caesar_encrypted)
    print("Розшифрований текст:")
    print(caesar_decrypted)

    print("\n           Шифр Віженера")
    print(f"Ключ: {vigenere_key}")
    print("Зашифрований текст:")
    print(vigenere_encrypted)
    print("Розшифрований текст:")
    print(vigenere_decrypted)

    print("\n" + "-" * 65)
    print("             Перевірка розшифрування")
    if caesar_decrypted == text.upper():
        print("+Шифр Цезаря - розшифрування виконано правильно")
    else:
        print("Шифр Цезаря - помилка розшифрування!")

    if vigenere_decrypted == text.upper():
        print("+Шифр Віженера - розшифрування виконано правильно")
    else:
        print("Шифр Віженера - помилка розшифрування!")

    compare_algorithms(
        text,
        caesar_encrypted,
        vigenere_encrypted,
        caesar_key,
        vigenere_key
    )

if __name__ == "__main__":
    main()
