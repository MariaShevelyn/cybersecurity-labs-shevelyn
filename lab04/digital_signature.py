import hashlib
from pathlib import Path

MOD = 1000007
MULTIPLIER = 7

def compute_hash(data_bytes, algorithm="sha256"):
    if algorithm == "sha512":
        return hashlib.sha512(data_bytes).hexdigest()
    elif algorithm == "blake2b":
        return hashlib.blake2b(data_bytes).hexdigest()
    return hashlib.sha256(data_bytes).hexdigest()

def generate_key_pair(surname, birth_date, secret_word, algorithm="sha256"):
    personal_string = f"{surname}{birth_date}{secret_word}"
    raw_hash = compute_hash(personal_string.encode("utf-8"), algorithm)

    private_key = int(raw_hash[:12], 16) % MOD

    public_key = (private_key * MULTIPLIER) % MOD

    return raw_hash, private_key, public_key

def get_document_hash(file_path, algorithm="sha256"):
    content = Path(file_path).read_bytes()
    hex_hash = compute_hash(content, algorithm)
    numeric_hash = int(hex_hash[:12], 16)
    return hex_hash, numeric_hash

def create_signature(file_path, private_key, algorithm="sha256"):
    _, doc_hash = get_document_hash(file_path, algorithm)
    signature = doc_hash ^ private_key
    return signature

def verify_signature(file_path, signature, public_key, algorithm="sha256"):
    _, current_doc_hash = get_document_hash(file_path, algorithm)

    inverse_multiplier = pow(MULTIPLIER, -1, MOD)
    recovered_key = (public_key * inverse_multiplier) % MOD

    decrypted_signature = signature ^ recovered_key

    is_valid = (decrypted_signature == current_doc_hash)
    status = "Підпис ДІЙСНИЙ" if is_valid else "Підпис ПІДРОБЛЕНИЙ"

    return is_valid, status, decrypted_signature, current_doc_hash


def prepare_demo_document(file_path, surname):
    content = (
        f"Власник документа: {surname}\n"
        f"Спеціальність: 122 Комп'ютерні науки\n"
        f"Навички: Python, SQL, C++, C#\n"
    )
    Path(file_path).write_text(content, encoding="utf-8")

def main():
    print("\n          Система особистих цифрових підписів")
    print("-" * 58)

    surname = input("Введіть прізвище: ").strip()
    birth_date = input("Введіть дату народження: ").strip()
    secret_word = input("Введіть секретне слово: ").strip()

    if not surname or not birth_date or not secret_word:
        print("Персональні дані не можуть бути порожніми")
        return

    print("\nДоступні алгоритми хешування: 1 - SHA-256, 2 - SHA-512, 3 - BLAKE2b")
    algo_choice = input("Оберіть алгоритм (1/2/3): ").strip()
    algo_map = {"1": "sha256", "2": "sha512", "3": "blake2b"}
    algorithm = algo_map.get(algo_choice, "sha256")

    default_doc = f"резюме_{surname}.txt"
    doc_input = input(
        f"Введіть назву файлу документа (Enter для '{default_doc}'): "
    ).strip()
    doc_path = doc_input if doc_input else default_doc

    prepare_demo_document(doc_path, surname)

    # генерація пари ключів
    print("\n" + "-" * 58)
    print("             Генерація пари ключів")
    raw_key_hash, private_key, public_key = generate_key_pair(
        surname, birth_date, secret_word, algorithm
    )
    print(f"Алгоритм хешування: {algorithm.upper()}")
    print(f"Вхідні дані ключа:  \"{surname}\" + \"{birth_date}\" + \"{secret_word}\"")
    print(f"Хеш персональних даних: {raw_key_hash[:32]}")
    print(f"Приватний ключ:     {private_key}")
    print(f"Публічний ключ:     {public_key}")

    Path("private_key.txt").write_text(str(private_key), encoding="utf-8")
    Path("public_key.txt").write_text(str(public_key), encoding="utf-8")

    # підписання документа
    print("\n" + "-" * 58)
    print("             Створення цифрового підпису")
    doc_hex_hash, doc_num_hash = get_document_hash(doc_path, algorithm)
    signature = create_signature(doc_path, private_key, algorithm)
    Path("signature.sig").write_text(str(signature), encoding="utf-8")

    print(f"Документ:           {doc_path}")
    print(f"Хеш документа ({algorithm.upper()}): {doc_hex_hash[:32]}")
    print(f"Числове значення хешу: {doc_num_hash}")
    print(f"Цифровий підпис (XOR): {signature}")

    # перевірка підпису
    print("\n" + "-" * 58)
    print("             Перевірка цифрового підпису")
    _, status, dec_sig, curr_hash = verify_signature(
        doc_path, signature, public_key, algorithm
    )
    print(f"Розшифрований підпис:   {dec_sig}")
    print(f"Хеш поточного документа: {curr_hash}")
    print(f"Перевірка рівності:     {dec_sig == curr_hash}")
    print(f"Результат: {status}")

    # демонстрація змін
    print("\n" + "-" * 58)
    print("       Демонстрація виявлення підробок та змін")
    # несанкціонована зміна тексту
    print("Спроба модифікації підписаного документа:")
    original_bytes = Path(doc_path).read_bytes()
    Path(doc_path).write_bytes(original_bytes + b"\nDodatkovi falshyvni dani")

    _, mod_status, mod_dec_sig, mod_curr_hash = verify_signature(
        doc_path, signature, public_key, algorithm
    )
    print(f"Розшифрований підпис:    {mod_dec_sig}")
    print(f"Хеш зміненого документа: {mod_curr_hash}")
    print(f"Результат: {mod_status} (виявлено зміну вмісту документа!)")

    Path(doc_path).write_bytes(original_bytes)

    # спроба підписати фальшивимключем
    print("\nСпроба підробки підпису без знання приватного ключа:")
    fake_private_key = (private_key + 12345) % MOD
    fake_signature = create_signature(doc_path, fake_private_key, algorithm)
    print(f"Фальшивий підпис зловмисника: {fake_signature}")

    _, fake_status, fake_dec_sig, orig_curr_hash = verify_signature(
        doc_path, fake_signature, public_key, algorithm
    )
    print(f"Розшифрований фейк-підпис: {fake_dec_sig}")
    print(f"Хеш поточного документа:   {orig_curr_hash}")
    print(f"Результат: {fake_status} (ключ підпису не відповідає публічному ключу!)")

if __name__ == "__main__":
    main()
