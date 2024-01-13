from PIL import Image
import numpy as np


''' 
https://www.eevblog.com/forum/thermal-imaging/infiray-and-their-p2-pro-discussion/200/

'''

def p2pro_image(fileobj):
    'extracts the raw data from a p2pro file and returns the temperature map in Celsius'
    im = Image.open(fileobj)
    a = im.applist[2][1]
    for i in range(3, 7):
        a += im.applist[i][1]
    # https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes    
    img = Image.frombytes('I;16N' , (256, 192), a[0xC000*2:])
    temps = np.array(img,dtype=np.int32) 
    return (temps / 64) - 273.15


def main():
    import matplotlib.pyplot as plt
    temps = p2pro_image('test6.jpg')
    print(temps.min(),temps.max())
    plt.imshow(temps, cmap="inferno")
    plt.show()


if __name__ == '__main__':
    main()