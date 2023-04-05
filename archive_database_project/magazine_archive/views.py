from django.shortcuts import render, redirect
from django.http import FileResponse, JsonResponse
from django.urls import reverse
import os
from . import functions as fc
import hashlib

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage


def m_index(request, pdf=None):
    '''
    runs when  url is '/magazine/<pdf>'

    function that gets the database information and renders
    the main page

    if a record has been selected from the table, this will
    render that record aswell
    '''
    tableData = fc.getInfo()

    return render(request, 'magazine/index.html', {
        'pdf': pdf,
        'results': tableData['result'],
        'years': tableData['years'],
        'months': tableData['months'],
        'days': tableData['days'],
        'volumes': tableData['volumes'],
        'numbers': tableData['numbers']
    })


def m_download(request, pdf):
    '''
    runs when url is '/magazine/download/<pdf>'

    opens a new tab and downloads the record <pdf> to the end-user's system
    '''
    return FileResponse(open(f'magazine_archive/static/magazine/temp/{pdf}.pdf', 'rb'), as_attachment=True)


def m_downloadArr(request):
    '''
    runs when url is '/magazine/downloadArr'

    uses form POST data to get list of records to download
    '''
    downloadArr = request.POST['downloadArr']
    downloadArr = downloadArr.split(',')
    fc.createZip(downloadArr)
    f = open(f'magazine_archive/static/magazine/temp/magazines.zip', 'rb')
    return FileResponse(f, as_attachment=True)


@login_required(redirect_field_name='')
def m_admin(request):
    '''
    runs when url is '/magazine/admin'

    only accessible if logged in
    allows select users to add to the database easily
    '''
    tableData = fc.getInfo()
    if request.method == 'POST':
        if request.POST['type'] == 'file':
            date = request.POST['date']
            volume = request.POST['volume']
            number = request.POST['number']
            data = request.FILES['file']
            if not data.name.endswith('.pdf'):
                messages.error(request, 'Only PDF files are allowed')
                return render(request, 'magazine/admin.html', {'results': tableData['result']})
            fs = FileSystemStorage(location='magazine_archive/static/magazine/temp/temp_file/')
            fs.save(f'{volume}-{number}.pdf', data)
            fc.insertBLOB(date, volume, number)
            fc.exportBLOB(volume, number, 'magazine_archive/static/magazine/temp/')
            os.remove(f'magazine_archive/static/magazine/temp/temp_file/{volume}-{number}.pdf')
            fc.read_pdf_individual(volume, number)
        else:
            pass
    return render(request, 'magazine/admin.html', {'results': tableData['result']})


def m_login(request):
    '''
    runs when url is '/magazine/login'

    uses form POST data to 
    '''
    if request.method == 'POST':
        email = request.POST['email']
        password = hashlib.sha512(request.POST['password'].encode()).hexdigest()
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('m_admin')

        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'magazine/login.html')

def m_getkeywords(request):
    '''
    runs when url is '/magazine/keywords'

    uses form POST data to get list of keywords
    '''
    keywordArr = request.POST['keywordArr']
    if ',' not in keywordArr:
        keywordArr = [keywordArr]
    else:
        keywordArr = keywordArr.split(',')
    pdfArr = request.POST['pdfArr']
    try:
        current = request.POST['current'].split('-')
    except:
        pass

    result = fc.getKeywords(keywordArr)
    return JsonResponse({'result': result})
    