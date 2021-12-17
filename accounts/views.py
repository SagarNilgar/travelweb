from django.shortcuts import render ,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import pyttsx3
import datetime
import sys
import pyaudio

# Create your views here.

def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        
        user =auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request,user)
            
            return redirect("/")
        
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
            
        
    else:
    
        return render(request,'login.html')
        

def register(request):
    
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        
        if password1==password2:
            if User.objects.filter(username=username).exists():
                
                messages.info(request,'Username is already registered')
                return redirect('register')
                
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Id is already registered')
                return redirect('register')
                 
            else:
                user =User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save();
        
                messages.info(request,'Registration is completed successfully')
                return redirect('login')
        else: 
            messages.info(request,'Password is not matching...')
        
            return redirect('register')
        
    else:
    
        return render(request,'register.html')
    

def logout(request):

    mail_content = '''Hello,
    This is a test mail.
    In this mail we are sending some attachments.
    The mail is sent using Python SMTP library.
    Thank You
    '''
    #The mail addresses and password
    sender_address = 'testsagar7@gmail.com'
    sender_pass = 'Sagar@123'
    receiver_address = 'sagarnilgar251@gmail.com'
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'A test mail sent by Python. It has an attachment.'
    #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    attach_file_name = 'C:\\Djangoprojects\\env\mysite\\accounts\\UnkownPerson\\Unkown_211217_125044\\1.png'
    attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
    payload = MIMEBase('application', 'octate-stream')
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload) #encode the attachment
    #add payload header with filename
    payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
    message.attach(payload)
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')
    auth.logout(request)
    return redirect('/')


def speak(request) :
    engine = pyttsx3.init()
    engine.say('Good morning.')
  
    engine.say('Nice to meet you')
    engine.runAndWait()
    return redirect('/')


  

   