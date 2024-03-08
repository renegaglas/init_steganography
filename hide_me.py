from PIL import Image
from math import sqrt
import time

def get_key_dir(key_s, key_dir_len):
    """return a directory with char bind to a tuple with unique value
    param key_s : string (alphabet use for the message)
    return : dictionary<char:(int, int)>"""
    key_dir = {}
    for i in range (len(key_s)):
        key_dir[key_s[i]] = (i // key_dir_len, i % key_dir_len)
    return key_dir

def next_coord(x, y, width, height):
    x += 1
    if (x > width):
        x = 0
        y += 1
        if (y > height):
            print("error image too small")

def hide_msg(msg, key_s, image):
    """hide msg in image using its pixel
    param msg : string (the message to hide)
    param image : string (relative path to the image)
    return : None"""
    print("LOG hide_msg : start")
    if (msg == None or key_s == None or image == None):
        print("error wrong input")
        return

    key_dir_len = int(sqrt(len(key_s)) + 1)
    key_dir = get_key_dir(key_s, key_dir_len)
    img = Image.open(image)
    width, height = img.size
    to_write = len(msg)
    msg_pos = 0

    for y in range(height):
        for x in range(width): #loop through every pixels
            if (to_write <= 0):
                print("LOG hide_msg : end (to_write <= 0)")
                return #exit when finish to write msg

            #encode 3 letter into 2 pixel
            (pixel00,pixel01,pixel02) = img.getpixel((x, y)) # pixel = (x,y,z)
            #([x],[y],z) (x2,y2,z2)
            pixel00 = pixel00 - pixel00 % key_dir_len + key_dir[msg[msg_pos]][0]
            pixel01 = pixel01 - pixel01 % key_dir_len + key_dir[msg[msg_pos]][1]
            msg_pos += 1
            if (to_write >= 2):
                #(x,y,[z]) ([x2],y2,z2)
                pixel02 = pixel02 - pixel02 % key_dir_len + key_dir[msg[msg_pos]][0]
                next_coord(x, y, width, height)
                (pixel10,pixel11,pixel12) = img.getpixel((x, y))
                pixel10 = pixel10 - pixel10 % key_dir_len + key_dir[msg[msg_pos]][1]
                msg_pos += 1
                #(x,y,z) (x2,[y2],[z2])
                if(to_write >= 3):
                    pixel11 = pixel11 - pixel11 % key_dir_len + key_dir[msg[msg_pos]][0]
                    pixel12 = pixel12 - pixel12 % key_dir_len + key_dir[msg[msg_pos]][1]
                    msg_pos += 1
                    to_write -= 1
                to_write -= 1
                img.putpixel((x, y), (pixel10,pixel11,pixel12))
            img.putpixel((x, y), (pixel00,pixel01,pixel02))
            to_write -= 1
    print("LOG hide_msg : end")



def recover_msg(msg, key_s, image):
    print("to implement")
'''
img = Image.open(file)

width, height = img.size
if (width < height):
    height = width
else:
    width = height

for x in range(width):
    for y in range(height):
        pixel = img.getpixel((x, y))
        img.putpixel((y, x), pixel)


img.show()
'''


file = "test.png"#input("Entrez le nom de l\'image : ")
key = "abcdefghijklmnopqrstuvwxyz "
msg = "mathis le plus beau"

hide_msg(msg, key, file)

time.sleep(100)

while True:
    a = 2
