import os
import zipfile as zf
import hashlib

import cv2 as cv
import pytesseract
from pdf2image import convert_from_path

import os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'archive_database.settings')

from django.db import connections


def convertToBinaryData(volume, number, path):
    with open(f'{path}{volume}-{number}.pdf', 'rb') as file:
        binaryData = file.read()
    return binaryData


def convertToFileData(volume, number, data, path):
    with open(f'{path}{volume}-{number}.pdf', 'wb') as file:
        file.write(data)


def insertBLOB(date, volume, number):
    path = 'magazine_archive/static/magazine/temp/temp_file/'
    data = convertToBinaryData(volume, number, path)
    with connections['default'].cursor() as cursor:
        sql = 'INSERT INTO magazines (date, volume, number, data) VALUES (%s, %s, %s, %s)'
        cursor.execute(sql, (date, volume, number, data))
        connections['default'].commit()
    for file in os.listdir(path):
        os.remove(os.path.join(path, file))


def exportBLOB(volume, number, path):
    with connections['default'].cursor() as cursor:
        sql = 'SELECT data FROM magazines WHERE volume = (%s) AND number = (%s)'
        cursor.execute(sql, (volume, number))
        result = cursor.fetchone()
        connections['default'].commit()
        convertToFileData(volume, number, result[0], path)


def exportAll():
    with connections['default'].cursor() as cursor:
        sql = 'SELECT volume, number, data FROM magazines'
        cursor.execute(sql)
        result = cursor.fetchall()
        connections['default'].commit()
        for record in result:
            convertToFileData(record[0], record[1], record[2], 'magazine_archive/static/magazine/temp/')


def createZip(pdfArr):
    root = 'magazine_archive/static/magazine/temp/'
    
    with zf.ZipFile(f'{root}magazines.zip', 'w', zf.ZIP_DEFLATED) as zfile:
        
        for file in os.listdir(root):
            if file[:-4] in pdfArr:
                zfile.write(os.path.join(root, file), file)


def getInfo():
    with connections['default'].cursor() as cursor:
        sql = 'SELECT date, volume, number FROM magazines'
        cursor.execute(sql)
        result = cursor.fetchall()
        connections['default'].commit()

        years = []
        months = []
        days = []
        volumes = []
        numbers = []
        for line in result:

            tmp = line[0].year
            if tmp not in years:
                years.append(tmp)

            tmp = line[0].month
            if tmp not in months:
                months.append(tmp)

            tmp = line[0].day
            if tmp not in days:
                days.append(tmp)

            tmp = line[1]
            if tmp not in volumes:
                volumes.append(tmp)

            tmp = line[2]
            if tmp not in numbers:
                numbers.append(tmp)

        years.sort()
        months.sort()
        days.sort()
        volumes.sort()
        numbers.sort()


        result = {
            'result': result,
            'years': years,
            'months': months,
            'days': days,
            'volumes': volumes,
            'numbers': numbers
        }
        return result


# def get_login(email, password):
#     with connections['default'].cursor() as cursor:
#         sql = 'SELECT email, password FROM admin'
#         cursor.execute(sql)
#         result = cursor.fetchall()
#         return (email, password) in result


def create_login(firstname, lastname, email, password):
    with connections['default'].cursor() as cursor:
        password = hashlib.sha512(password.encode()).hexdigest()
        sql = f"INSERT INTO admin (id,firstname,lastname,email,password) VALUES (NULL, '{firstname}', '{lastname}', '{email}', '{password}')"
        cursor.execute(sql)
        connections['default'].commit()

def read_pdf():
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
                    if letter in [',','.',';',':',')','(','"','\n','”','“','\\']:
                        word = word.replace(letter, '')

                with connections['default'].cursor() as cursor:
                    sql = f'INSERT INTO keywords (volume, number, page, word) VALUES ("{key[0]}", "{key[1]}", "{i+1}", "{word}")'
                    try:
                        cursor.execute(sql)
                        connections['default'].commit()

                    except Exception as e:
                        print(sql)
                        print(word)
                        print(e)

            os.remove(f'magazine_archive/static/magazine/temp/temp_img/{i}.jpg')

def read_pdf_individual(volume, number):
    pdf = f'{volume}-{number}.pdf'
    pages = convert_from_path(f'magazine_archive/static/magazine/temp/{pdf}', 300)

    for i, page in enumerate(pages):
        page.save(f'magazine_archive/static/magazine/temp/temp_img/{i}.jpg', 'JPEG')
        img = cv.imread(f'magazine_archive/static/magazine/temp/temp_img/{i}.jpg')
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        text = pytesseract.image_to_string(img_gray)
        text = text.split(' ')
        for word in text:
            for letter in word:
                if letter in [',','.',';',':',')','(','"','\n','”','“','\\']:
                    word = word.replace(letter, '')

            with connections['default'].cursor() as cursor:
                sql = f'INSERT INTO keywords (volume, number, page, word) VALUES ("{volume}", "{number}", "{i+1}", "{word}")'
                try:
                    cursor.execute(sql)
                    connections['default'].commit()

                except Exception as e:
                    print(sql)
                    print(word)
                    print(e)

            os.remove(f'magazine_archive/static/magazine/temp/temp_img/{i}.jpg')

def getKeywords(keywordArr):
    with connections['default'].cursor() as cursor:

        placeholders = ', '.join(['%s'] * len(keywordArr))

        # format the query
        query = f'''
            SELECT volume, number, page
            FROM keywords
            WHERE word IN ({placeholders})
            GROUP BY volume, number, page
            HAVING COUNT(DISTINCT word) = {len(keywordArr)}
        '''
        # fetch the results
        cursor.execute(query, keywordArr)
        results = cursor.fetchall()
        
        return results

