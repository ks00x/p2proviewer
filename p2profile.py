from PIL import Image
import numpy as np

''' references
https://www.eevblog.com/forum/thermal-imaging/infiray-and-their-p2-pro-discussion/200/

played around with the code given here: 
https://exiftool.org/forum/index.php?topic=11401.msg61816#msg61816

tested with pillow version 10.0.1
'''

def c_to_f(x):
    return x * 1.8 + 32


def p2pro_image(fileobj,fahrenheit=False):
    '''extracts the raw data from a p2pro file and returns a tuple with 
    the temperature map in Celsius (256x192 pixels) and the in camera processed image as numpy arrays'''
    im = Image.open(fileobj)
    a = im.applist[2][1]
    for i in range(3, 7):
        a += im.applist[i][1]
    # https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes    
    img = Image.frombytes('I;16N' , (256, 192), a[0xC000*2:])
    temps = np.array(img,dtype=np.int32)
    temps = np.rot90(temps,3)
    temps = (temps / 64) - 273.15
    if fahrenheit :        
        return c_to_f(temps) , im
    else :
        return temps, im


def main():
    import matplotlib.pyplot as plt
    temps,org = p2pro_image('test6.jpg')
    print(temps.min(),temps.max())
    plt.imshow(temps, cmap="inferno")
    plt.show()


if __name__ == '__main__':
    main()