from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from .models import user
from django.contrib import messages
from django.contrib.sessions.models import Session
import MySQLdb as sql
from django.core.files.storage import FileSystemStorage
import os
from django.http import HttpResponse,StreamingHttpResponse
import csv
from login.poseest.run_video import pose
from statistics import mean


import threading
from imutils.video import VideoStream
import imutils
import time

import cv2
#import cv2
import shutil
from moviepy.editor import VideoFileClip
from datetime import datetime


@csrf_exempt
def login(request):
    request.session['is_logged']=False
    return render(request,'index.html')

def signout(request):
    request.session['is_logged'] = False
    del request.session['logged_user']
    return login(request)
    return httpResponse()

def checkuser(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        request.session['is_logged']=True
        request.session['logged_user']=username

        logged_user = request.session.get('logged_user')

        return dashboard(request)
        return HttpResponse()

def register(request):
        return render(request,'register.html')

def dbentry(request):
    if request.method == "POST":
        fname=request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        pwd = request.POST['pwd']
        conpwd = request.POST['conpwd']

        if pwd != conpwd:
            return render(request, 'register.html')

        usr = user(fname=fname,lname=lname,email=email,phone=phone,pwd=pwd)
        usr.save()

        directory = email

        # Parent Directory path
        parent_dir = "C:/Users/LENOVO IP 510/Desktop/BE_PROJECT/AAAK/PROJECT FILES/"

        # Path
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)



    return render(request, 'index.html')

def add_new_test(request):
    return render(request, 'add_new_test.html')

def add_video(request):
    if request.method == "POST":
        file=request.FILES['videofile']
        filename=request.POST['filename']
        fs=FileSystemStorage()
        filepath = "C:/Users/LENOVO IP 510/Desktop/BE_PROJECT/AAAK/PROJECT FILES/"
        logged_user = request.session.get('logged_user')
        filepath =filepath+logged_user+'/'+filename
        os.mkdir(filepath)
        vfilepath = filepath + '/'+filename+'.mp4'
        fs.save(vfilepath,file)

        dfilepath = filepath + '/'+filename+'.csv'
        with open(dfilepath, 'w', newline='') as file:
            writer = csv.writer(file)
        return dashboard(request)
        return HttpResponse()

def dashboard(request):
    logged_user = request.session.get('logged_user')
    path="C:/Users/LENOVO IP 510/Desktop/BE_PROJECT/AAAK/PROJECT FILES/"+logged_user
    dir_list=os.listdir(path)

    accuracies={}
    for dir in dir_list:
        filepath = "C:/Users/LENOVO IP 510/Desktop/BE_PROJECT/AAAK/PROJECT FILES/"
        filepath = filepath + logged_user + '/' + dir + '/' + dir + '.csv'

        report = {}
        i = 0
        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                report[i] = row
                i = i + 1

        total = i
        i = i - 1;
        accuracy = 0
        while i > -1:
            accuracy = accuracy + float(str(report[i][2]))
            i = i - 1

        if total == 0:
            accuracy = 0
        else:
            accuracy = accuracy / total

        accuracies[dir]=round(accuracy,2)


    return render(request, 'dashboard.html',{'dirs':dir_list,'accuracies':accuracies,'total':total})

def practice(request):
    if request.method=="POST":
        dirname=request.POST["dirname"]
        logged_user = request.session.get('logged_user')
        filepath = "C:/Users/LENOVO IP 510/Desktop/BE_PROJECT/AAAK/PROJECT FILES/"
        filepath = filepath + logged_user + '/' + dirname+'/'+dirname+'.csv'

        report={}
        i=0;
        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                report[i]=row
                i=i+1

        total=i
        i=i-1;
        accuracy=0
        while i>-1:
            accuracy=accuracy+float(report[i][2])
            i=i-1

        if total==0:
            accuracy=0
        else:
            accuracy=accuracy/total
        return render(request,"practice.html",{'report':report,'accuracy':round(accuracy,2),'dir':dirname})

def start(request):
    if request.method=="POST":
        dirname=request.POST["dirname"]
        logged_user = request.session.get('logged_user')
        filepath = "C:/Users/LENOVO IP 510/Desktop/BE_PROJECT/AAAK/PROJECT FILES/"
        filepath = filepath + logged_user + '/' + dirname+'/'+dirname+'.mp4'
        src=filepath
        dst="C:/Users/LENOVO IP 510/Desktop/BE_PROJECT/AAAK/login/static/inputvideo/input.mp4"
        shutil.copy(src, dst)
        clip = VideoFileClip(src)

        
        return render(request, "live_practice.html", {'dir':dirname,'duration':clip.duration})

def accuracy_save(request):
    if request.method=="POST":
        dirname=request.POST["dirname"]
        accuracy = request.POST["accuracy"]
        logged_user = request.session.get('logged_user')
        filepath = "C:/Users/LENOVO IP 510/Desktop/BE_PROJECT/AAAK/PROJECT FILES/"
        filepath = filepath + logged_user + '/' + dirname+'/'+dirname+'.csv'

        list=[]
        x = datetime.now()
        list.append(x.strftime("%x"))
        list.append(x.strftime("%X"))
        list.append(round(float(accuracy),2))

        with open(filepath, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = csv.writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(list)

        report = {}
        i = 0;
        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                report[i] = row
                i = i + 1

        total = i
        i = i - 1;
        accuracy = 0
        while i > -1:
            accuracy = accuracy + float(report[i][2])
            i = i - 1

        if total == 0:
            accuracy = 0
        else:
            accuracy = accuracy / total
        return render(request, "practice.html", {'report': report, 'accuracy':round(accuracy,2), 'dir': dirname})





#####################################################################################################################
def loading(request):
    if request.method == "GET":
        dirname = request.GET["dirname"]
        print("in loading")
        return render(request, "loading.html", {'dir': dirname})




def process(request):
    if request.method == "GET":
        dirname = request.GET["dirname"]
        logged_user = request.session.get('logged_user')
        filepath = "C:/Users/LENOVO IP 510/Desktop/BE_PROJECT/AAAK/PROJECT FILES/"
        filepath = filepath + logged_user + '/' + dirname + '/' + dirname + '.mp4'
        camera = "C:/Users/LENOVO IP 510/Desktop/BE_PROJECT/pose/login/poseest/INPUTS/input1.mp4"
        camera1 = "C:/Users/LENOVO IP 510/Desktop/BE_PROJECT/pose/login/poseest/INPUTS/half.mp4"
        path="C:/Users/LENOVO IP 510/Downloads/test.webm"


        accuracy=pose(camera,camera)
        values1={}
        values2={}
        values3={}
        values4={}
        i=1
        for items in accuracy:
            if(items<=25):
                values1[round(i*(24/60),2)] = round(items,2)

            if (items > 25 and items <= 50):
                values2[round(i*(24/60),2)] = round(items,2)

            if (items > 50 and items <= 75):
                values3[round(i*(24/60),2)] = round(items,2)

            if (items > 75 and items <= 100):
                values4[round(i*(24/60),2)] = round(items,2)
            i=i+1


        return render(request, "accuracy_save.html",{'accuracy':round(mean(accuracy),2),
                                        'first':values1,'second':values2,'third':values3,'fourth':values4,'dir':dirname})






