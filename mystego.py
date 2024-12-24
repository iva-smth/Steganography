from PIL import Image
import numpy as np
import argparse

def hide_message_in_image(cover_image_path, secret_message, output_image_path):
    cover_image = Image.open(cover_image_path)
    width, height = cover_image.size

    # Кодируем сообщение в UTF-8 и преобразуем в двоичный формат
    binary_secret_message = ''.join(format(byte, '08b') for byte in secret_message.encode('utf-8')) + '00000000'

    if len(binary_secret_message) > width * height * 3:
        raise ValueError("Секретное сообщение слишком длинное для изображения.")

    cover_image_array = np.array(cover_image)

    index = 0
    for row in range(height):
        for col in range(width):
            for color_channel in range(3):
                if index < len(binary_secret_message):
                    bit = int(binary_secret_message[index])
                    if (cover_image_array[row][col][color_channel] % 2) != bit:
                        if bit == 1:
                            cover_image_array[row][col][color_channel] = min(cover_image_array[row][col][color_channel] + 1, 255)
                        else:
                            cover_image_array[row][col][color_channel] = max(cover_image_array[row][col][color_channel] - 1, 0)
                    index += 1
                else:
                    break

    output_image = Image.fromarray(cover_image_array)
    output_image.save(output_image_path)
    print(f"Сообщение скрыто в изображении: {output_image_path}")

def extract_message_from_image(stego_image_path):
    stego_image = Image.open(stego_image_path)
    width, height = stego_image.size
    stego_image_array = np.array(stego_image)

    binary_secret_message = ''
    for row in range(height):
        for col in range(width):
            for color_channel in range(3):
                binary_secret_message += str(stego_image_array[row][col][color_channel] % 2)

    secret_message = ''
    for i in range(0, len(binary_secret_message), 8):
        byte = binary_secret_message[i:i + 8]
        if byte == '00000000':
            break
        secret_message += chr(int(byte, 2))

    # Декодируем извлеченное сообщение из UTF-8
    return secret_message.encode('latin1').decode('utf-8')

def read_message_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скрытие и извлечение сообщений в изображениях с использованием стеганографии LSB.")
    
    subparsers = parser.add_subparsers(dest='command')

    # Подкоманда для скрытия сообщения
    hide_parser = subparsers.add_parser('hide', help='Скрыть сообщение в изображении.')
    hide_parser.add_argument('cover_image', help='Путь к изображению-носителю.')
    hide_parser.add_argument('secret_message', help='Секретное сообщение для скрытия или путь к текстовому файлу.')
    hide_parser.add_argument('output_image', help='Путь для сохранения выходного изображения.')

    # Подкоманда для извлечения сообщения
    extract_parser = subparsers.add_parser('extract', help='Извлечь сообщение из стеганографического изображения.')
    extract_parser.add_argument('stego_image', help='Путь к стеганографическому изображению.')

    args = parser.parse_args()

    if args.command == 'hide':
        # Проверка, является ли аргумент путем к файлу
        try:
            with open(args.secret_message, 'r', encoding='utf-8') as file:
                secret_message = file.read()
        except FileNotFoundError:
            secret_message = args.secret_message  # Если файл не найден, используем как текстовое сообщение

        hide_message_in_image(args.cover_image, secret_message, args.output_image)
        
    elif args.command == 'extract':
        extracted_message = extract_message_from_image(args.stego_image)
        print("Извлеченное секретное сообщение:", extracted_message)
