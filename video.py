import cv2
import numpy as np

WIDTH = 800
HEIGHT = 600
INTERN_WIDTH = WIDTH / 10
INTERN_HEIGHT = HEIGHT /10

def getBaseImages(qnt):
    images = []
    for i in range(qnt):
        image = cv2.imread('./assets/{}_base.png'.format(i + 1))
        resized = cv2.resize(image, (WIDTH, HEIGHT))
        images.append(resized)
    return images

def infiniteSlideShow(images):
    index = 0
    while True:
        cv2.imshow('image', images[index])
        k = cv2.waitKey(33)
        
        if k == 100:
            if index == len(images) - 1:
                index = 0
            else:
                index = index + 1
        elif k == 97:
            if index == 0:
                index = len(images) - 1
            else:
                index = index - 1
        if k == 27:
            break
        elif k == -1:
            continue
        else:
            print(k)


def _blendImage(im1, im2):
    
    i = 1
    blended = []
    original_im1 = im1
    original_im2 = im2

    FACTOR = 5
    while(((i * FACTOR) + INTERN_HEIGHT) <= HEIGHT):
        print('Iteração: {}'.format(i))

        new_intern_width = int(INTERN_WIDTH * i * FACTOR) 
        new_intern_height = int(INTERN_HEIGHT * i * FACTOR)
        
        extended_extern_width = int(WIDTH * i * FACTOR)
        extended_extern_height = int(HEIGHT * i * FACTOR )
        

        intern = cv2.resize(original_im2, (new_intern_width, new_intern_height))

        non_cropped_extern = cv2.resize(original_im1, (extended_extern_width, extended_extern_height))
        extern_height, extern_width, _ = non_cropped_extern.shape
        
        half_extended_height = int(extended_extern_height / 2)
        half_extended_width = int(extended_extern_width / 2)

        Y1 = half_extended_height - int(new_intern_height / 2)
        Y2 = half_extended_height + int(new_intern_height / 2)

        X1 = half_extended_width - int(new_intern_width / 2)
        X2 = half_extended_width + int(new_intern_width / 2)

        extern = non_cropped_extern[Y1:Y2, X1:X2]
        print('\n ---------------------- \n')
        print('Tamanho do externo croppado')
        print(extern.shape)
        print('Limites')
        print(X1,X2,Y1,Y2)
        print('\n ---------------------- \n')
        ## Colando imagem interna na externa

        new_extern_height, new_extern_width, _ = extern.shape 

        half_extern_width = int (new_extern_width / 2)
        half_extern_height = int (new_extern_height / 2)

        iX1 = int( half_extern_width - (new_intern_width / 2))
        iX2 = int( half_extern_width + (new_intern_width / 2))

        iY1 = int( half_extern_height - (new_intern_height / 2))
        iY2 = int( half_extern_height + (new_intern_height / 2))
        
        extern[iY1:iY2, iX1:iX2] = intern
        blended.append(extern)

        im1 = extern
        im2 = intern
        i = i + 1
    return blended

def blendImage(externImg, insideImage):
    try:
        blended = []
        blended = _blendImage(externImg, insideImage)

        return blended

    except Exception as e:
        print(e)
        return []

def generateAnimation(images):
    length = len(images)
    newImages = []
    for i in range(length):
        
        if i == length - 1:
            nextImage = images[0]
        else:
            nextImage = images [i + 1]

        currentImage = images[i]
        
        blended = blendImage(currentImage, nextImage)
        
        for b in blended:
            newImages.append(b)

    return newImages
        


images = getBaseImages(3)
animated =generateAnimation(images)

infiniteSlideShow(animated)