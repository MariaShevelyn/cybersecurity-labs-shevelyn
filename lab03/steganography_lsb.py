
from PIL import Image, ImageChops
from pathlib import Path
import os

END_MARKER = "###END###"

def text_to_bits(text):
    data = text.encode("utf-8")
    return "".join(f"{byte:08b}" for byte in data)


def bits_to_text(bits):
    bits = bits[:len(bits) // 8 * 8]
    data = bytes(
        int(bits[i:i + 8], 2)
        for i in range(0, len(bits), 8)
    )
    return data.decode("utf-8", errors="replace")


def hide_message(input_image, output_image, message):
    with Image.open(input_image) as source:
        image = source.convert("RGB")

    data = (message + END_MARKER).encode("utf-8")

    # спочатку 32 біти
    header = f"{len(data):032b}"
    # на біти
    payload = text_to_bits(message + END_MARKER)
    all_bits = header + payload

    capacity = image.width * image.height * 3

    if len(all_bits) > capacity:
        raise ValueError(
            "Повідомлення завелике для цього зображення"
        )

    pixels = list(image.getdata())
    new_pixels = []
    bit_index = 0

    for pixel in pixels:
        rgb = list(pixel)

        for channel in range(3):
            if bit_index < len(all_bits):
                bit = int(all_bits[bit_index])

                # молодший біт
                rgb[channel] = (rgb[channel] & 254) | bit
                bit_index += 1

        new_pixels.append(tuple(rgb))

    result = Image.new("RGB", image.size)
    result.putdata(new_pixels)

    result.save(output_image, format="PNG")

    return len(all_bits)


def extract_message(encoded_image):
    with Image.open(encoded_image) as source:
        image = source.convert("RGB")

    pixels = list(image.getdata())
    bits = []

    # зчитуємо молодші біти каналів
    for pixel in pixels:
        for channel_value in pixel:
            bits.append(str(channel_value & 1))

    if len(bits) < 32:
        raise ValueError("Зображення замале")

    message_length = int("".join(bits[:32]), 2)
    required_length = 32 + message_length * 8

    if required_length > len(bits):
        raise ValueError(
            "Некоректна довжина даних"
            "Можливо, зображення не містить повідомлення"
        )

    # витягуємо біти
    message_bits = "".join(bits[32:required_length])
    message_bytes = bytes(
        int(message_bits[i:i + 8], 2)
        for i in range(0, len(message_bits), 8)
    )

    decoded = message_bytes.decode("utf-8", errors="replace")

    if not decoded.endswith(END_MARKER):
        raise ValueError(
            "Маркер кінця не знайдено"
            "Можливо, зображення пошкоджене"
        )

    return decoded[:-len(END_MARKER)]


def analyze_images(original_path, encoded_path):
    with Image.open(original_path) as source:
        original = source.convert("RGB")

    with Image.open(encoded_path) as source:
        encoded = source.convert("RGB")

    if original.size != encoded.size:
        raise ValueError("Розміри зображень не збігаються")

    difference = ImageChops.difference(original, encoded)
    diff_pixels = list(difference.getdata())

    total_pixels = original.width * original.height

    changed_pixels = sum(
        1 for pixel in diff_pixels
        if pixel != (0, 0, 0)
    )

    changed_channels = sum(
        1
        for pixel in diff_pixels
        for value in pixel
        if value != 0
    )

    max_difference = max(
        (max(pixel) for pixel in diff_pixels),
        default=0
    )

    original_size = os.path.getsize(original_path)
    encoded_size = os.path.getsize(encoded_path)

    changed_percent = (
        changed_pixels / total_pixels * 100
        if total_pixels else 0
    )

    print("\n" + "-" * 45)
    print("         Аналіз змін у зображенні")

    print(f"Роздільна здатність: {original.width} × {original.height}")
    print(f"Загальна кількість пікселів: {total_pixels}")
    print(
        f"Змінених пікселів: {changed_pixels} "
        f"({changed_percent:.4f}%)"
    )
    print(f"Змінених кольорових каналів: {changed_channels}")
    print(f"Максимальна різниця значення каналу: {max_difference}")
    print(f"Розмір оригіналу: {original_size} байт")
    print(f"Розмір нового PNG: {encoded_size} байт")
    print(
        f"Різниця розмірів файлів: "
        f"{encoded_size - original_size:+} байт"
    )

def main():
    print("\n           Стенографія - приховування тексту в зображенні")
    print("-" * 60)

    image_path = input(
        "Введіть шлях до зображення: "
    ).strip().strip('"')

    if not image_path or not Path(image_path).is_file():
        print("Помилка! Файл зображення не знайдено")
        return

    personal_data = input(
        "Введіть ім'я: "
    ).strip()

    text = input("Введіть текст: ").strip()

    if not text:
        print("Помилка! Повідомлення не може бути порожнім")
        return

    # Використовуємо введені персональні дані у повідомленні.
    if personal_data:
        message = f"Автор: {personal_data}. Повідомлення: {text}"
    else:
        message = text

    output_path = str(
        Path(image_path).with_name("encoded_image.png")
    )

    try:
        print("\n" + "-" * 45)
        print("           1. Перетворення тексту на біти")
        print(f"Текст: {message}")

        first_character = message[0]
        print(
            f"Перший символ {first_character!r} у UTF-8: "
            f"{first_character.encode('utf-8').hex(' ')}"
        )
        print(
            "Його двійковий код: "
            + " ".join(
                f"{byte:08b}"
                for byte in first_character.encode("utf-8")
            )
        )

        print("\n" + "-" * 45)
        print("           2. Приховування повідомлення")

        bits_written = hide_message(
            image_path, output_path, message
        )

        print("Повідомлення успішно приховано")
        print(f"Файл результату: {output_path}")
        print(f"Записано бітів разом із заголовком: {bits_written}")

        print("\n" + "-" * 45)
        print("             3. Витягування повідомлення")

        extracted = extract_message(output_path)
        print(f"Витягнутий текст: {extracted}")

        if extracted == message:
            print("Повідомлення збігається")
        else:
            print("Помилка! Текст не збігається")

        print("\n" + "-" * 45)
        print("             4. Аналіз зображення")
        analyze_images(image_path, output_path)


    except (OSError, ValueError) as error:
        print(f"\nПомилка: {error}")


if __name__ == "__main__":
    main()
