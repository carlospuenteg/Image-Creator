import cv2  
import numpy as np
import random

from functools import reduce

fibSeq = lambda n : [reduce(lambda x,_ : [x[1], x[0]+x[1]], range(num), [0,1] )[0] for num in range(n+1)]
fibVal = lambda n : reduce(lambda x,_ : [x[1], x[0]+x[1]], range(n), [0,1])[0]

#-----------------------------------------------------------------------------------------------------------------------

def random_colored(img_width, img_height, img_file):
    img =  np.zeros([img_height, img_width, 3], dtype = np.uint8)

    for line in img:
        for pixel in line:
            pixel[0] = random.randint(0, 255)
            pixel[1] = random.randint(0, 255)
            pixel[2] = random.randint(0, 255)

    cv2.imwrite(img_file, img)

#-----------------------------------------------------------------------------------------------------------------------

def random_bw(img_width, img_height, img_file):
    img =  np.zeros([img_height, img_width, 3], dtype = np.uint8)

    for line in img:
        for pixel in line:
            pixel[:] = [0,0,0] if random.getrandbits(1) == 1 else [255,255,255]

    cv2.imwrite(img_file, img)

#-----------------------------------------------------------------------------------------------------------------------

def linear_gradient_toWhite(img_width, img_height, img_file, color):
    img =  np.zeros([img_height, img_width, 3], dtype = np.uint8)

    colors = []
    for c in color[::-1]:
        colors.append({
            "val": c,
            "step": img_height // (255 - c) if c != 255 else 0,
            "mod": img_height % (255 - c) if c != 255 else 0
        })

    for i in range(img_height):
        for c in colors:
            if c['step'] != 0 and i % c["step"] + int(i < c["mod"]) == 0:
                c["val"] += 1

        img[i] = [colors[0]['val'], colors[1]['val'], colors[2]['val']]

    cv2.imwrite(img_file, img)

#-----------------------------------------------------------------------------------------------------------------------

def textured_color(img_width, img_height, img_file, color, maxChange=30, chance=0.2):
    img =  np.zeros([img_height, img_width, 3], dtype = np.uint8)

    color = color[::-1]

    for line in img:
        for pixel in line:
            rand = [random.randint(0, maxChange) if random.random() < chance/3 else 0 for i in range(3)]
            pixel[:] = [color[i] + rand[i] if color[i] + rand[i] < 255 else color[i] - rand[i] for i in range(3)]

    cv2.imwrite(img_file, img)

#-----------------------------------------------------------------------------------------------------------------------

def texture_from_bin(img_width, img_height, img_file, bin):
    img =  np.zeros([img_height, img_width, 3], dtype = np.uint8)

    for i, line in enumerate(img):
        for j, pixel in enumerate(line):
            location = i*img_width + j
            pixel[:] = (255,255,255) if bin[location % len(bin)] == '1' else (0,0,0)

    cv2.imwrite(img_file, img)

def binary_fibonacci(n):
    return '0'.join([bin(x)[2:] for x in fibSeq(n)])

    
#-----------------------------------------------------------------------------------------------------------------------

def fibonacci_texture(img_width, img_height, img_file):
    img =  np.zeros([img_height, img_width, 3], dtype = np.uint8)

    fib = fibSeq(300)

    index = 0
    for i, line in enumerate(img):
        for j, pixel in enumerate(line):
            location = i*img_width + j
            if fib[index] <= location:
                index += 1
            
            print(location)
            img[i][j][:] = (255,255,255) if index%2 == 1 else (0,0,0)
            
    cv2.imwrite(img_file, img)

#-----------------------------------------------------------------------------------------------------------------------

# random_colored(100, 100, "random_colored.png")
# random_bw(1024, 720, "random_bw.png")
# linear_gradient_toWhite(1024, 720, "linear_gradient_toWhite.png", [255,100,0])
# textured_color(1024, 720, "textured_color.png", [92, 64, 51], 40, 0.5)
# texture_from_bin(2000, 2000, "texture_from_bin.png", binary_fibonacci(100))
# fibonacci_texture(2000, 2000, "fibonacci_texture.png")