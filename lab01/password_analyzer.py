import re

def analyze_password(password, name, birth_date):
    score = 0
    problems = []
    recommendations = []

    name_lower = name.lower()
    password_lower = password.lower()

    if name_lower and name_lower in password_lower:
        problems.append("Пароль містить ім'я користувача")
        recommendations.append("Не використовуйте ім'я у паролі")
    else:
        score += 1

    date_parts = birth_date.split(".")

    if len(date_parts) == 3:
        day, month, year = date_parts

        if year in password:
            problems.append("Пароль містить рік народження")
            recommendations.append("Не використовуйте рік народження у паролі")
        else:
            score += 1

        if day in password:
            problems.append("Пароль містить день народження")
            recommendations.append("Не використовуйте день народження у паролі")
        else:
            score += 1

        if month in password:
            problems.append("Пароль містить місяць народження")
            recommendations.append("Не використовуйте місяць народження у паролі")
        else:
            score += 1

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
        problems.append("Пароль має середню довжину")
        recommendations.append("Бажано використовувати пароль довжиною не менше 12 символів")
    else:
        problems.append("Пароль занадто короткий")
        recommendations.append("Збільшіть довжину пароля щонайменше до 12 символів")

    has_lowercase = bool(re.search(r"[a-zа-яіїєґ]", password))
    has_uppercase = bool(re.search(r"[A-ZА-ЯІЇЄҐ]", password))
    has_digit = bool(re.search(r"\d", password))
    has_special = bool(re.search(r"[^a-zA-Zа-яА-ЯіїєґІЇЄҐ0-9]", password))

    if has_lowercase:
        score += 1
    else:
        problems.append("Відсутні маленькі літери")
        recommendations.append("Додайте маленькі літери")

    if has_uppercase:
        score += 1
    else:
        problems.append("Відсутні великі літери")
        recommendations.append("Додайте великі літери")

    if has_digit:
        score += 1
    else:
        problems.append("Відсутні цифри")
        recommendations.append("Додайте цифри")

    if has_special:
        score += 1
    else:
        problems.append("Відсутні спеціальні символи")
        recommendations.append("Додайте спеціальні символи")

    common_words = [
        "password",
        "qwerty",
        "admin",
        "welcome",
        "password123",
        "qwerty123",
        "admin123"
    ]

    found_word = None

    for word in common_words:
        if word.lower() in password_lower:
            found_word = word
            break

    if found_word:
        problems.append(f"Пароль містить поширене слово: {found_word}")
        recommendations.append("Не використовуйте поширені слова")
    else:
        score += 1

    if score > 10:
        score = 10

    if score <= 3:
        level = "Низький"
    elif score <= 6:
        level = "Середній"
    elif score <= 8:
        level = "Хороший"
    else:
        level = "Високий"

    return score, level, problems, recommendations


def main():
    print("\n                 АНАЛІЗАТОР БЕЗПЕКИ ПАРОЛЯ")
    print("-" * 60)

    print("Введіть персональні дані для аналізу")

    name = input("Ім'я: ")
    birth_date = input("Дата народження: ")

    password = input("Тестовий пароль: ")

    score, level, problems, recommendations = analyze_password(
        password,
        name,
        birth_date
    )

    print("-" * 60)
    print("                  РЕЗУЛЬТАТ АНАЛІЗУ")

    print(f"Пароль: {'*' * len(password)}")
    print(f"Оцінка безпеки: {score}/10")
    print(f"Рівень безпеки: {level}")

    print("\n        Аналіз персональних даних")

    personal_data_found = False

    if name.lower() in password.lower():
        print("-Виявлено ім'я у паролі")
        personal_data_found = True

    date_parts = birth_date.split(".")

    if len(date_parts) == 3:
        day, month, year = date_parts

        if year in password:
            print("-Виявлено рік народження")
            personal_data_found = True

        if day in password:
            print("-Виявлено день народження")
            personal_data_found = True

        if month in password:
            print("-Виявлено місяць народження")
            personal_data_found = True

    if not personal_data_found:
        print("Зв'язок з персональними даними не виявлено")

    print("\n        Проблеми")

    if problems:
        for problem in problems:
            print("!" + problem)
    else:
        print("Критичних проблем не виявлено")

    print("\n        Рекомендації")

    if recommendations:
        unique_recommendations = list(dict.fromkeys(recommendations))

        for recommendation in unique_recommendations:
            print("+" + recommendation)
    else:
        print("Пароль відповідає основним вимогам безпеки")


if __name__ == "__main__":
    main()
