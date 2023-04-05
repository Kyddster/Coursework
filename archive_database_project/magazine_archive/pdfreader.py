import cv2 as cv
import imutils
from pdf2image import convert_from_path
import os
import numpy as np
from scipy.spatial.distance import hamming
import pickle

import pytesseract

def read_pdf():
    keywords = []
    '''
    - read file
    - save pages to images
    - go through each image
    - scan letters
    - scan words
    - find letters in words
    - save words
    - convert words to text
    - save text with reference to page and document, with (x,y,w,h) on page
    - after all pages gone through, delete images of pages
    '''
    test_dict_old = {'a': [],
                 'b': [],
                 'c': [],
                 'd': [],
                 'e': [],
                 'f': [],
                 'g': [],
                 'h': [],
                 'i': [],
                 'j': [],
                 'k': [],
                 'l': [],
                 'm': [],
                 'n': [],
                 'o': [],
                 'p': [],
                 'q': [],
                 'r': [],
                 's': [],
                 't': [],
                 'u': [],
                 'v': [],
                 'w': [],
                 'x': [],
                 'y': [],
                 'z': [],
                 '0': [],
                 '1': [],
                 '2': [],
                 '3': [],
                 '4': [],
                 '5': [],
                 '6': [],
                 '7': [],
                 '8': [],
                 '9': [],
                }
    test_dict = pickle_load()
    print(test_dict)

    for pdf in os.listdir('magazine_archive/static/magazine/temp/'):
        if not pdf.endswith('.pdf'): continue
        pages = convert_from_path(f'magazine_archive/static/magazine/temp/{pdf}', 300)
        key = pdf[:-4].split('-')

        for i, page in enumerate(pages):
            page.save(f'magazine_archive/static/magazine/temp/temp_img/{i}.jpg', 'JPEG')
            img = cv.imread(f'magazine_archive/static/magazine/temp/temp_img/{i}.jpg')
            img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


            # words
            retW, thresh2W = cv.threshold(img_gray, 253, 255, cv.THRESH_BINARY_INV)
            kernelW = cv.getStructuringElement(cv.MORPH_RECT, (1,1))
            maskW = cv.morphologyEx(thresh2W, cv.MORPH_DILATE, kernelW)
            bboxesW = []
            # bboxes_img = img.copy()
            contoursW = cv.findContours(maskW, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            contoursW = imutils.grab_contours(contoursW)
            for cntr in contoursW:
                x,y,w,h = cv.boundingRect(cntr)
                if w < 10 or h < 10: continue
                # cv.rectangle(bboxes_img, (x, y), (x+w, y+h), (0,0,255), 1)
                bboxesW.append((x,y,w,h))

            # letters
            retL, thresh2L = cv.threshold(img_gray, 125, 255, cv.THRESH_BINARY_INV)
            kernelL = cv.getStructuringElement(cv.MORPH_RECT, (1,1))
            maskL = cv.morphologyEx(thresh2L, cv.MORPH_DILATE, kernelL)
            bboxesL = []
            # bboxes_img = img.copy()
            contoursL = cv.findContours(maskL, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            contoursL = imutils.grab_contours(contoursL)
            for cntr in contoursL:
                x,y,w,h = cv.boundingRect(cntr)
                if w < 10 or h < 10:
                    continue
                # cv.rectangle(bboxes_img, (x, y), (x+w, y+h), (0,0,255), 1)
                bboxesL.append((x,y,w,h))

            # connecting letters into words
            large_boxes = bboxesW
            small_boxes = bboxesL
            threshold = 0.7
            for large_box in large_boxes:
                word = ''
                contained_boxes = []
                crop_img = img[large_box[1]:large_box[1]+large_box[3], large_box[0]:large_box[0]+large_box[2]]
                # cv.imshow('cropped', crop_img)
                # cv.waitKey(0)
                for box in small_boxes:
                    x_overlap = max(0, min(box[0] + box[2], large_box[0] + large_box[2]) - max(box[0], large_box[0]))
                    y_overlap = max(0, min(box[1] + box[3], large_box[1] + large_box[3]) - max(box[1], large_box[1]))
                    overlap_area = x_overlap * y_overlap
                    small_box_area = box[2] * box[3]
                    containment_ratio = overlap_area / small_box_area
                    if containment_ratio >= threshold:
                        contained_boxes.append(box)
                contained_boxes = sorted(contained_boxes, key=lambda x: x[0])

                # convert letters into bitmaps
                for box in contained_boxes:
                    crop_img = img[box[1]:box[1]+box[3], box[0]:box[0]+box[2]]
                    crop_gray = cv.cvtColor(crop_img, cv.COLOR_BGR2GRAY)
                    ret, crop_thresh = cv.threshold(crop_gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
                    crop_inv = cv.bitwise_not(crop_thresh)
                    crop_array = np.int8(crop_inv / 255)
                    # print(crop_array)

                    # do OCR here

                    letterArr = []
                    valueArr = []
                    sizeArr = []
                    size1Arr = []
                    total = []
                    for letter in test_dict:
                        if test_dict[letter] != []:
                            for array in test_dict[letter]:
                                try:
                                    tempArr = crop_array[::]
                                    if array.shape[0] > tempArr.shape[0]:
                                        array = array[:tempArr.shape[0]]
                                    if array.shape[0] < tempArr.shape[0]:
                                        tempArr = tempArr[:array.shape[0]]
                                    if array.shape[1] > tempArr.shape[1]:
                                        array = array[:,:tempArr.shape[1]]
                                    if array.shape[1] < tempArr.shape[1]:
                                        tempArr = tempArr[:,:array.shape[1]]
                                    
                                    size1Temp = crop_array.shape[1] / tempArr.shape[1]
                                    letterArr.append(letter)
                                    hammingTemp = hamming(tempArr.flatten(), array.flatten())
                                    sizeTemp = (tempArr.size / crop_array.size)
                                    totalTemp = (hammingTemp + (1-sizeTemp)) / 2



                                    # if letter in 'mniu':
                                    #     print(letter, hammingTemp, sizeTemp, size1Temp, totalTemp)
                                    #     print()

                                    valueArr.append(hammingTemp)
                                    sizeArr.append(sizeTemp)
                                    size1Arr.append(size1Temp)
                                    total.append(totalTemp)



                                except Exception as e:
                                    pass
                                    # print(e)

                    try:
                        minLetter = letterArr[valueArr.index(min(valueArr))]
                        min1Letter = letterArr[total.index(min(total))]
                        minSize = letterArr[sizeArr.index(min(sizeArr))]
                        # print(minLetter, min(valueArr))
                        # print(min1Letter, min(total))
                        word += minLetter
                    except Exception as e:#
                        pass
                        # print(e)
                    

                    # test_letter = input('letter: ')
                    # if test_letter == '':
                    #     continue
                    # elif test_letter == 'exit':
                    #     exit()
                    # elif test_letter == 'print':
                    #     print(test_dict)
                    # elif test_letter == 'save':
                    #     pickle_dump(test_dict)
                    #     exit()
                    
                    # test_dict[test_letter].append(crop_array)

                
                print(word)
                keywords.append((key[0], key[1], i+1, word))

            for file in os.listdir('magazine_archive/static/magazine/temp/temp_img'):
                os.remove(f'magazine_archive/static/magazine/temp/temp_img/{file}')
            print(keywords)



def pickle_dump(dictionary):
    with open('magazine_archive/static/magazine/temp/training_data/data.pickle', 'wb') as f:
        pickle.dump(dictionary, f)


def pickle_load():
    with open('magazine_archive/static/magazine/temp/training_data/data.pickle', 'rb') as file:
        return pickle.load(file)

def read_pdf1():
    keywords = []

    for pdf in os.listdir('magazine_archive/static/magazine/temp/'):
        if not pdf.endswith('.pdf'): continue
        pages = convert_from_path(f'magazine_archive/static/magazine/temp/{pdf}', 300)
        key = pdf[:-4].split('-')

        for i, page in enumerate(pages):
            page.save(f'magazine_archive/static/magazine/temp/temp_img/{i}.jpg', 'JPEG')
            img = cv.imread(f'magazine_archive/static/magazine/temp/temp_img/{i}.jpg')
            img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            text = pytesseract.image_to_string(img_gray)
            text = text.split(' ')
            for word in text:
                for letter in word:
                    if letter in [',','.',';',':',')','(','"','\n']:
                        word = word.replace(letter, '')
                keywords.append((key[0],key[1],i+1,word))
            os.remove(f'magazine_archive/static/magazine/temp/temp_img/{i}.jpg')
    return keywords


print(read_pdf1())