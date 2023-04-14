from django.shortcuts import render, redirect
from django.http import FileResponse, JsonResponse, HttpResponse
from django.urls import reverse
import os
from . import functions as fc
import hashlib
import json

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


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
    try:
        os.remove('magazine_archive/static/magazine/temp/magazines.zip')
    except:
        pass
    downloadArr = request.POST['downloadArr']
    downloadArr = downloadArr.split(',')
    fc.createZip(downloadArr)
    response = FileResponse(open('magazine_archive/static/magazine/temp/magazines.zip', 'rb'), as_attachment=True)
    return response


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
            fc.read_pdf_individual(volume, number)
            tableData = fc.getInfo()
        else:
            pass
    return render(request, 'magazine/admin.html', {'results': tableData['result']})


def m_login(request):
    '''
    runs when url is '/magazine/login'

    uses form POST data to authenticate users
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

    uses form POST data to get list of records
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


def m_downloadTranslated(request):
    '''
    runs when url is '/magazine/downloadTranslated'

    downloads translated version of document as plaintext
    '''
    try:
        os.remove('magazine_archive/static/magazine/temp/temp_file/translated_text.txt')
    except:
        pass

    language = request.POST['language']
    volume = request.POST['volume']
    number = request.POST['number']

    translated_text = fc.read_pdf_individual_translate(volume, number, language)
    
    with open('magazine_archive/static/magazine/temp/temp_file/translated_text.txt', 'w') as temp_file:
        temp_file.write(translated_text)
    
    return FileResponse(open('magazine_archive/static/magazine/temp/temp_file/translated_text.txt', 'rb'), as_attachment=True)


def m_forgot_password(request):
    '''
    runs when url is '/magazine/forgot-password'

    uses a form to get email address and then send 'reset-password' email if email address is in admin table
    '''
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            reset_password_link = request.build_absolute_uri(f'/magazine/reset-password/{user.id}:{token}/')
            send_mail(
                'Reset your password',
                f'Click on the following link to reset your password: {reset_password_link}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'An email has been sent to your address with instructions to reset your password.')
        else:
            messages.error(request, 'The email address you entered is not registered.')
    return render(request, 'magazine/forgot_password.html')


def m_reset_password(request, uid, uidb64, token):
    '''
    runs when url is '/magazine/reset-password/<token>

    allows user to reset password if token is still valid
    '''
    print(uid, uidb64, token)
    try:
        user = User.objects.filter(id=int(uid)).first()
    except Exception as e:
        print(e)
        user = None

    token_generator = PasswordResetTokenGenerator()
    if user and token_generator.check_token(user, f'{uidb64}-{token}'):
        if request.method == 'POST':
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            if password == confirm_password:
                password = hashlib.sha512(password.encode()).hexdigest()
                print(password)
                fc.set_password(user.email, password)
                user.set_password(password)
                user.save()
                messages.success(request, 'Your password has been reset successfully. You can now login with your new password.')
                return redirect('m_login')
            else:
                messages.error(request, 'The passwords you entered do not match.')
        return render(request, 'magazine/reset_password.html', {'token': token, 'uid': uid, 'uidb64': uidb64})
    else:
        messages.error(request, 'The reset password link is invalid or has expired.')
        return redirect('m_forgot_password')