import os
import sys, getopt
from colorama import Fore, Back, init
from PIL import Image, ImageEnhance

init(convert=True)

def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile="])
    except getopt.GetoptError:
        print('picasso.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('picasso.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
    print(inputfile)
    print(render(inputfile))

def render(file):
    img = Image.open(file)
    width, height = img.size
    if width > os.get_terminal_size().lines:
        width = os.get_terminal_size().lines

    if height > os.get_terminal_size().lines:
        height = os.get_terminal_size().lines

    img = img.resize((width, height))

    img = convert_primary(img)

    string = ""

    pixels = list(img.getdata())
    width, height = img.size
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

    for i in pixels:
        for j in i:
            string += rgb_to_console_color(j) + "▓▓"
        string += "\n"
    return string


def color_subtract(a, b):
    return sum(tuple(map(lambda i, j: abs(i - j), a, b)))

def rgb_to_console_color(color):

    console_colors = {
        Fore.BLACK : (0, 0, 0),
        Fore.BLUE : (0, 0, 128),
        Fore.GREEN : (0, 128, 0),
        Fore.CYAN : (0, 128, 128),
        Fore.RED : (128, 0, 0),
        Fore.MAGENTA : (128, 0, 128),
        Fore.YELLOW : (128, 128, 0),
        Fore.WHITE : (192, 192, 192),
        Fore.LIGHTBLACK_EX : (128, 128, 128),
        Fore.LIGHTBLUE_EX : (0, 0, 255),
        Fore.LIGHTGREEN_EX : (0, 255, 0),
        Fore.LIGHTCYAN_EX : (0, 255, 255),
        Fore.LIGHTRED_EX : (255, 0, 0),
        Fore.LIGHTMAGENTA_EX : (255, 0, 255),
        Fore.LIGHTYELLOW_EX : (255, 255, 0),
        Fore.LIGHTWHITE_EX : (255, 255, 255)
    }

    closest = Fore.LIGHTWHITE_EX

    for i in console_colors:
        if color_subtract(console_colors[i], color) < color_subtract(console_colors[closest], color):
            closest = i

    return closest

def convert_primary(image):
  width, height = image.size

  pixels = image.load()

  for i in range(width):
    for j in range(height):
      pixel = image.getpixel((i, j))

      red =   pixel[0]
      green = pixel[1]
      blue =  pixel[2]

      if red > 127:
        red = 255
      else:
        red = 0
      if green > 127:
        green = 255
      else:
        green = 0
      if blue > 127:
        blue = 255
      else:
        blue = 0

      pixels[i, j] = (int(red), int(green), int(blue))

  return image

if __name__ == "__main__":
   main(sys.argv[1:])
