import os
import zipfile as zf
import cv2 as cv
import pytesseract
from pdf2image import convert_from_path
import re
# re library from here:
# https://www.w3schools.com/python/python_regex.asp

import os
from django.conf import settings
from django.db import connections

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'archive_database.settings')

from google.cloud import translate_v2 as translate


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


def export_all():
    '''
    used when PDFs are being exported from the database to file form
    when the application is first run
    '''
    with connections['default'].cursor() as cursor:
        sql = 'SELECT volume, number, data FROM magazines'
        cursor.execute(sql)
        result = cursor.fetchall()
        connections['default'].commit()
        for record in result:
            convertToFileData(record[0], record[1], record[2], 'magazine_archive/static/magazine/temp/')


def create_zip(pdfArr):
    '''
    used when downloading multiple records
    '''
    # Original code that I modified:
    # https://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory
    root = 'magazine_archive/static/magazine/temp/'
    
    with zf.ZipFile(f'{root}magazines.zip', 'w', zf.ZIP_DEFLATED) as zfile:
        
        for file in os.listdir(root):
            if file[:-4] in pdfArr:
                zfile.write(os.path.join(root, file), file)


def get_info():
    '''
    gets information from the magazines table that is used to help build
    the table in the base and admin routes.
    '''
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
        # easier on the template if i have all the fields as seperate variables
        return result


def get_login(email):
    with connections['default'].cursor() as cursor:
        sql = f"SELECT * FROM admin WHERE email = '{email}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        return result


# def create_login(firstname, lastname, email, password):
#     with connections['default'].cursor() as cursor:
#         password = hashlib.sha512(password.encode()).hexdigest()
#         sql = f"INSERT INTO admin (firstname,lastname,email,password) VALUES ('{firstname}', '{lastname}', '{email}', '{password}')"
#         cursor.execute(sql)
#         connections['default'].commit()


def check_record(volume, number):
    with connections['default'].cursor() as cursor:
        sql = f'SELECT EXISTS(SELECT 1 FROM magazines WHERE volume = {volume} AND number = {number})'
        cursor.execute(sql)
        result = cursor.fetchone()[0]
        return (result == 1)


def check_email(email):
    with connections['default'].cursor() as cursor:
        # learnt about the EXISTS statement from here:
        # https://www.w3schools.com/sql/sql_exists.asp
        sql = f"SELECT EXISTS(SELECT 1 FROM admin WHERE email = '{email}')"
        cursor.execute(sql)
        result = cursor.fetchone()[0]
        return (result == 1)


def read_pdf_all():
    for pdf in os.listdir('magazine_archive/static/magazine/temp/'):
        if not pdf.endswith('.pdf'): continue
        pages = convert_from_path(f'magazine_archive/static/magazine/temp/{pdf}', 300)
        key = pdf[:-4].split('-')

        for i, page in enumerate(pages):
            page.save(f'magazine_archive/static/magazine/temp/temp_img/{i}.jpg', 'JPEG')
            img = cv.imread(f'magazine_archive/static/magazine/temp/temp_img/{i}.jpg')
            img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            text = pytesseract.image_to_string(img_gray)
            text = re.sub(r'[^\w\s\n]', '', text)
            text = re.split(r'\s+|\n+', text)
            for word in text:
                with connections['default'].cursor() as cursor:
                    sql = f'SELECT recordID FROM magazines WHERE volume = {key[0]} AND number = {key[1]}'
                    cursor.execute(sql)
                    record = cursor.fetchone()[0]

                with connections['default'].cursor() as cursor:
                    sql = f'INSERT INTO keywords (recordID, page, word) VALUES ("{record}", "{i+1}", "{word}")'
                    try:
                        cursor.execute(sql)
                        connections['default'].commit()
                    except Exception as e:
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
        text = re.sub(r'[^\w\s\n]', '', text)
        text = re.split(r'\s+|\n+', text)
        for word in text:
            with connections['default'].cursor() as cursor:
                sql = f'SELECT recordID FROM magazines WHERE volume = {volume} AND number = {number}'
                cursor.execute(sql)
                record = cursor.fetchone()[0]

            with connections['default'].cursor() as cursor:
                sql = f'INSERT INTO keywords (recordID, page, word) VALUES ("{record}", "{i+1}", "{word}")'
                try:
                    cursor.execute(sql)
                    connections['default'].commit()
                except Exception as e:
                    print(e)

        os.remove(f'magazine_archive/static/magazine/temp/temp_img/{i}.jpg')

def read_pdf_individual_translate(volume, number, endLang, ogLang='en'):
    pdf = f'{volume}-{number}.pdf'
    pages = convert_from_path(f'magazine_archive/static/magazine/temp/{pdf}', 300)

    translatedText = ''

    for i, page in enumerate(pages):
        page.save(f'magazine_archive/static/magazine/temp/temp_img/{i}.jpg', 'JPEG')
        img = cv.imread(f'magazine_archive/static/magazine/temp/temp_img/{i}.jpg')
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        text = pytesseract.image_to_string(img_gray)

        client = translate.Client()

        result = client.translate(text, source_language=ogLang, target_language=endLang)
        translatedText += result['translatedText']

        os.remove(f'magazine_archive/static/magazine/temp/temp_img/{i}.jpg')
    return translatedText


def get_keywords(keywordArr):
    with connections['default'].cursor() as cursor:
        query = f'''
            SELECT magazines.volume, magazines.number, keywords.page
            FROM keywords
            JOIN magazines ON keywords.recordID = magazines.recordID
            WHERE keywords.word IN ({', '.join(['%s'] * len(keywordArr))})
            GROUP BY magazines.volume, magazines.number, keywords.page
            HAVING COUNT(DISTINCT keywords.word) = {len(keywordArr)}
        '''
        # GROUP BY, HAVING COUNT and DISTINCT statemets from:
        # https://www.w3schools.com/sql/sql_groupby.asp
        # https://www.w3schools.com/sql/sql_having.asp
        # https://www.w3schools.com/sql/sql_distinct.asp

        cursor.execute(query, keywordArr)
        results = cursor.fetchall()
        
        return results
    
def set_password(email, password):
    with connections['default'].cursor() as cursor:
        sql = f'''
            UPDATE admin
            SET password = '{password}'
            WHERE email = '{email}'
        '''
        try:
            cursor.execute(sql)
            connections['default'].commit()
            return True
        except Exception as e:
            print(e)
            return False

    