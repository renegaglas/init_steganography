print("hide_me start")
from PIL import Image
from math import sqrt
import time

show_log = False

def get_key_dir(key_s):
    """return a directory with char bind to a tuple with unique value
    param key_s : string (alphabet use for the message)
    return : dictionary<char:(int, int)>"""
    key_s += ":0123456789"
    key_dir_tmp = {}
    key_dir = {}
    key_dir_len = 0
    for i in range (len(key_s)):# retrive first occurrance and assign it an id
        '''print("i",i)
        print("key_s",key_s)
        print("key_s[i]",key_s[i])'''
        if (key_dir_tmp.get(key_s[i]) == None):
            key_dir_tmp[key_s[i]] = key_dir_len
            key_dir_len += 1
    key_dir_len = int(sqrt(key_dir_len)) + 1 # matrice key_dir_len by key_dir_len
    for key, vlaue in key_dir_tmp.items():  #split the id so it can be put in a pixel
        key_dir[key] = (vlaue // key_dir_len, vlaue % key_dir_len)

    print(key_dir)
    print(key_dir_len)
    return key_dir, key_dir_len

def next_coord(x, y, width, height):
    print("before x =",x,"| y =",y)
    x += 1
    if (x >= width):
        x = 0
        y += 1
        if (y >= height):
            print("error image too small")
    print("after x =",x,"| y =",y)
    return (x ,y)

def LOG(function_name,msg, msg_pos, key_dir_len,key_dir):
    if (not show_log):
        return
    print("LOG : function_name",function_name)
    print("LOG : key_dir_len",key_dir_len)
    print("LOG : msg_pos",msg_pos)
    print("LOG : msg '" + msg + "'")
    print("LOG : msg[msg_pos] '" + msg[msg_pos] + "'")
    print("LOG : key_dir",key_dir)
    print("LOG : key_dir.get(" + msg[msg_pos] + ") : ",key_dir.get(msg[msg_pos]))

def hide_msg(msg, key_s, image):
    """hide msg in image using its pixel
    param msg : string (the message to hide)
    param image : string (relative path to the image)
    return : None"""
    print("LOG hide_msg : start")
    if (msg == None or key_s == None or image == None):
        print("error wrong input")
        return
    msg = str(len(msg)) + ":" + msg  #ex : "12:hello world!"
    key_dir, key_dir_len = get_key_dir(key_s)
    img = Image.open(image)
    width, height = img.size
    to_write = len(msg)
    msg_pos = 0

    #for debug purpose
    #key_dir_reverse = get_key_dir_recover(key_s)

    for y in range(height):
        for x in range(0,width,2): #loop through every pixels
            print("pixel coord = (",x,",",y,")")
            if (msg_pos >= to_write):
                print("LOG hide_msg : saving","tmp.png")
                img.save("tmp.png")
                return

            #encode 3 letter into 2 pixel
            (pixel00,pixel01,pixel02) = img.getpixel((x, y))
            LOG("hide_msg 1",msg, msg_pos, key_dir_len,key_dir)
            print("\nfirst pixel\npixel00",pixel00,"\npixel01",pixel01,"\npixel02",pixel02)
            #([pixel00],[pixel01],pixel02) ([pixel10],[pixel11],pixel12)
            pixel00 = pixel00 - pixel00 % key_dir_len + key_dir[msg[msg_pos]][0]
            pixel01 = pixel01 - pixel01 % key_dir_len + key_dir[msg[msg_pos]][1]
            msg_pos += 1
            if (msg_pos < to_write):
                #(pixel00,pixel01,[pixel02]) ([pixel10],pixel11,pixel12)
                LOG("hide_msg 2",msg, msg_pos, key_dir_len,key_dir)
                pixel02 = pixel02 - pixel02 % key_dir_len + key_dir[msg[msg_pos]][0]
                print("\npixel00",pixel00,"\npixel01",pixel01,"\npixel02",pixel02,"\n------------------")


                print("calling before x =",x,"| y =",y)
                (x2, y2) = next_coord(x, y, width, height)#override by the for loop
                print("calling after x =",x,"| y =",y)

                (pixel10,pixel11,pixel12) = img.getpixel((x2, y2))
                print("\nsecond pixel\npixel10",pixel10,"\npixel11",pixel11,"\npixel12",pixel12)
                pixel10 = pixel10 - pixel10 % key_dir_len + key_dir[msg[msg_pos]][1]
                msg_pos += 1

                if(msg_pos < to_write):
                    #(pixel00,pixel01,pixel02) pixel10,[pixel11],[pixel12])
                    LOG("hide_msg 3",msg, msg_pos, key_dir_len,key_dir)
                    pixel11 = pixel11 - pixel11 % key_dir_len + key_dir[msg[msg_pos]][0]
                    pixel12 = pixel12 - pixel12 % key_dir_len + key_dir[msg[msg_pos]][1]
                    #print("letter to encode :",msg[msg_pos])
                    #print("letter decoded   :",get_letter(pixel11, pixel12, key_dir_reverse, key_dir_len))
                    msg_pos += 1
                print("\nnpixel10",pixel10,"\npixel11",pixel11,"\npixel12",pixel12,"\n------------------")
                img.putpixel((x2, y2), (pixel10,pixel11,pixel12))#(pixel10,pixel11,pixel12))
            img.putpixel((x, y), (pixel00,pixel01,pixel02))#(pixel00,pixel01,pixel02)) # finish to write on the first pixel
    print("LOG hide_msg : saving","tmp.png")
    img.save("tmp.png")
    print("LOG hide_msg : end")

def get_key_dir_recover(key_s):
    """return a directory with char bind to a tuple with unique value
    param key_s : string (alphabet use for the message)
    return : dictionary<char:(int, int)>"""
    tmp, key_dir_len = get_key_dir(key_s)
    reversed_dict = {}
    for key, value in tmp.items():
        reversed_dict[value] = key
    return reversed_dict, key_dir_len

def LOG_recover(function_name,msg,key_dir):
    if (not show_log):
        return
    print("LOG recover : function_name",function_name)
    print("LOG recover : msg '" + msg + "'")
    print("LOG recover : key_dir",key_dir)

def get_letter(sub_pixel1, sub_pixel2, key_dir, key_tab_len, msg=""):
    if (show_log):
        LOG_recover("recover_msg",msg,key_dir)
        print("LOG: sub_pixel1 =",sub_pixel1)
        print("LOG: sub_pixel2 =",sub_pixel2)
        print("LOG: key_tab_len =",key_tab_len)
        print("LOG (coord1,coord2): (",sub_pixel1 % key_tab_len,",",sub_pixel2 % key_tab_len,")")
        print("return '" + key_dir[sub_pixel1 % key_tab_len, sub_pixel2 % key_tab_len] + "'")
    return key_dir[sub_pixel1 % key_tab_len, sub_pixel2 % key_tab_len]


def recover_msg(key_s, image, delim = ':'):
    """recover the msg from image using the provided key
    param key_s : string
    param image : string (relative path to the image)
    return : None"""
    print("LOG recover_msg : start")
    if (key_s == None or image == None):
        print("error wrong input")
        return
    msg = ""
    key_dir, key_dir_len = get_key_dir_recover(key_s)
    img = Image.open(image)
    width, height = img.size
    for y in range(height):# fixme
        for x in range(0,width,2): #loop through every pixels
            print("msg :",msg)
            #recover 3 letter into 2 pixel
            (pixel00,pixel01,pixel02) = img.getpixel((x, y)) # pixel = (x,y,z)
            #([pixel00],[pixel01],[pixel02]) pixel10,pixel11,pixel12)
            print("\nfirst pixel\npixel00",pixel00,"\npixel01",pixel01,"\npixel02",pixel02,"\n------------------")
            (x, y) = next_coord(x, y, width, height)
            (pixel10,pixel11,pixel12) = img.getpixel((x, y))
            print("\nsecond pixel\npixel10",pixel10,"\npixel11",pixel11,"\npixel12",pixel12,"\n------------------")
            tmp = get_letter(pixel00, pixel01, key_dir, key_dir_len, msg)
            if (tmp == delim):
                print("LOG recover_msg : job finish / msg =",msg)
                msg_start = get_letter(pixel02, pixel10,key_dir, key_dir_len)
                msg_start += get_letter(pixel11, pixel12,key_dir, key_dir_len)
                (x,y) = next_coord(x,y, width, height)
                return msg_start + recover_msg_aux(img,x,y,int(msg) - 2,key_dir,key_dir_len)
            msg += tmp
            if (x < width or y < height):
                #(x,y,[z]) ([x2],y2,z2)
                tmp = get_letter(pixel02, pixel10, key_dir, key_dir_len, msg)
                if (tmp == delim):
                    print("LOG recover_msg : job finish / msg =",msg)
                    msg_start = get_letter(pixel11, pixel12,key_dir, key_dir_len)
                    (x,y) = next_coord(x,y, width, height)
                    return msg_start + recover_msg_aux(img,x,y,int(msg) - 1,key_dir,key_dir_len)
                msg += tmp
                #(x,y,z ) (x2,[y2],[z2])
                tmp = get_letter(pixel11, pixel12, key_dir, key_dir_len, msg)
                if (tmp == delim):
                    print("LOG recover_msg : job finish / msg =",msg)
                    (x,y) = next_coord(x,y, width, height)
                    return recover_msg_aux(img,x,y,int(msg),key_dir,key_dir_len)
                msg += tmp

    print("LOG recover_msg : image finish / msg =",msg)
    return "error"


def recover_msg_aux(img, start_x, start_y, to_read, key_dir, key_dir_len):
    msg = ""
    print("LOG recover_msg_aux : start")
    print("LOG  start_x:",start_x)
    print("LOG  start_y:",start_y)
    print("LOG  to_read:",to_read)
    for y in range(start_y, height):
        for x in range(start_x,width,2):
            print("msg :",msg)
            #([pixel00],[pixel01],[pixel02]) (pixel10,pixel11,pixel12)
            (pixel00,pixel01,pixel02) = img.getpixel((x, y))
            tmp = get_letter(pixel00, pixel01, key_dir, key_dir_len, msg)
            if (to_read <= 0):
                print("LOG recover_msg_aux end 1 : job finish / msg =",msg)
                return msg
            msg += tmp
            to_read -= 1

            if (x < width or y < height):
                (x, y) = next_coord(x, y, width, height)

                #(pixel00,pixel01,pixel02) ([pixel10],[pixel11],[pixel12])
                (pixel10,pixel11,pixel12) = img.getpixel((x, y))
                tmp = get_letter(pixel02, pixel10, key_dir, key_dir_len, msg)
                if (to_read <= 0):
                    print("LOG recover_msg_aux end  2: job finish / msg =",msg)
                    return msg
                msg += tmp
                to_read -= 1

                tmp = get_letter(pixel11, pixel12, key_dir, key_dir_len, msg)
                if (to_read <= 0):
                    print("LOG recover_msg_aux end 3 : job finish / msg =",msg)
                    return msg
                msg += tmp
                to_read -= 1

    print("LOG recover_msg_aux end : image finish / msg =",msg)
    return "error"
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
msg = "hello world"

black = "black.png"
tmp = Image.open("tmp.png")
height,width = tmp.size
for y in range(height):
    for x in range(width): #loop through every pixels
        tmp.putpixel((x,y),(0,0,0))
tmp.save(black)

hide_msg(msg, key, file)
tmp = recover_msg(key, "tmp.png")
print("msg =",tmp)
print("hide_me end")
