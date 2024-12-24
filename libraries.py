from stegano import lsb as steganoLSB
from pystegano import lsb as pysteganoLSB
import stepic
from PIL import Image
import numpy as np


def stegano_lib(file , message, output):
    secret = steganoLSB.hide(file, message)
    secret.save(output)
    clear_message = steganoLSB.reveal(output)
    print(f"Сообщение: {clear_message}")

def stepic_lib(file , message, output):
    image = Image.open(file)
    encoded_image = stepic.encode(image, message.encode())
    encoded_image.save(output)
    output_image = Image.open(output)
    clear_message = stepic.decode(output_image)
    print(f"Сообщение: {clear_message}")

def pystegano_lib(file, message, output):
    image = Image.open(file)
    image_np = np.array(image)
    encoded_image_np = pysteganoLSB.encode(image_np, message)
    encoded_image = Image.fromarray(encoded_image_np)
    encoded_image.save(output)
    output_image = Image.open(output)
    clear_message = pysteganoLSB.decode(np.array(output_image))
    print(f"Сообщение: {clear_message}")

stegano_lib('house.png', 'thats a message for stegano', 'house_encoded1.png')
stepic_lib('house.png', 'thats a message for stepic', 'house_encoded2.png')
pystegano_lib("house.png", "thats a message for pystegano", 'house_encoded3.png')