from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import draftable
from django.contrib.auth.models import User
import requests
from draftable.endpoints import exceptions
from datetime import timedelta
from .models import UserFiles
from .forms import UploadFilesForm
from django.conf import settings

# Create your views here.


@login_required(login_url='login')
def index(request):
    if request.method == "POST" and request.FILES:
        left_file = request.FILES["left_file"]
        right_file = request.FILES["right_file"]
        print("Profile:-", request.user.profile.token)
        token = request.user.profile.token
        # user_files = UserFiles(left_file=left_file, right_file=right_file)
        # user_files.save()
        form = UploadFilesForm(request.POST, request.FILES)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.save()

            print("----LEFT FILE--->", form_obj.left_file.name)
            print("----RIGHT FILE--->", form_obj.right_file.name)
            LEFT_FILE_NAME = form_obj.left_file.name
            RIGHT_FILE_NAME = form_obj.right_file.name
            try:
                reqUrl = "https://43.204.76.144/api/v1/comparisons"

                headers = {
                    #'Authorization': 'Token fc0870520b1d705a1718f0462aca3457',
                    'Authorization': 'Token ' + token
                }

                files = {
                    'left.file_type': (None, 'pdf'),
                    'left.display_name': (None, left_file.name),
                    'left.file':
                    open(r"" + settings.MEDIA_ROOT + "/" + LEFT_FILE_NAME,
                         "rb"),
                    'right.file_type': (None, 'pdf'),
                    'right.display_name': (None, right_file.name),
                    'right.file':
                    open(r"" + settings.MEDIA_ROOT + "/" + RIGHT_FILE_NAME,
                         "rb"),
                    'public': (None, 'true'),
                }

                response = requests.post(
                    'https://43.204.76.144/api/v1/comparisons',
                    headers=headers,
                    files=files,
                    verify=False)
                res = response.json()
                print("Response-->", res)

                resURL = reqUrl + "/viewer/" + "zGBXUJ/" + res["identifier"]

                messages.success(request, "PROCESS STATUS: SUCCESS")
                return render(request, 'index.html', context={"url": resURL})
            except Exception as error:
                messages.error(
                    request, "PROCESS STATUS: FAILED --> Error:" + str(error))
                print("----ERROR---->", error)
                return render(request, 'index.html', context={})
        else:
            messages.error(request, form.errors)
            print("----ERROR---->", form.errors)
            return render(request, 'index.html', context={})

    return render(request, 'index.html', context={})


def log_in(request):
    if request.user.is_authenticated:
        return redirect(index)
    else:
        context = {}
        if request.method == "POST":
            username = request.POST['userName']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                # return render(request, 'index.html')
                return redirect(index)
            else:
                messages.error(request, 'please enter correct credentials!')
                return render(request, 'login.html', context)
        else:
            return render(request, 'login.html')


@login_required(login_url='logout')
def log_out(request):
    auth.logout(request)
    return render(request, 'login.html')
