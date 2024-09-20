from PIL import Image
import numpy as np
import time
import os
import sys

file_path = os.path.join(os.getcwd(), 'chapter1.jpg')

#Chapter 1:
current_time = int(time.time())
generated_number = (current_time % 100) + 50
if generated_number % 2 == 0:
    generated_number += 10
print(generated_number)
Input_image = Image.open(file_path)
total_r = 0
def increase_rgb(image, adjustment_value):
    red_channel, green_channel, blue_channel = image.split()
    
    red_channel = red_channel.point(lambda p: min(p + adjustment_value, 255))
    green_channel = green_channel.point(lambda p: min(p + adjustment_value, 255))
    blue_channel = blue_channel.point(lambda p: min(p + adjustment_value, 255))
    return Image.merge("RGB", (red_channel, green_channel, blue_channel))



modified_image = increase_rgb(Input_image, generated_number)
output_path = os.path.join(os.getcwd(), 'chapter1out.jpg')
modified_image.save(output_path)
image_width, image_height = modified_image.size
red_pixels_sum = 0

for y in range(image_height):
    for x in range(image_width):
        red_value, _, _ = modified_image.getpixel((x, y))
        red_pixels_sum += red_value

print("Sum of Red pixels Values:", red_pixels_sum)

# Question 2 Chapter 2

s = '56aAww1984sktr235270aYmn145ss785fsq31D0'


numbers = ""
letters = ""
ASCII_number = []
ASCII_letter = []

# split characters and numbers
for char in s:
    if char.isalpha():
        letters += char
    else:
        numbers += char

# ASCII values of the uppercase letters
for char in letters:
    if char.isupper(): # only appending uppercase letters
        ASCII_letter.append(ord(char))

#ASCII values of the even numbers
for char in numbers:
    if int(char) % 2 == 0: # only appening even numbers
        ASCII_number.append(ord(char))
print("ASCII values of uppercase letters:", ASCII_letter)
print("ASCII values of even digits:", ASCII_number)
