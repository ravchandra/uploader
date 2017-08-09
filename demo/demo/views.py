from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext

import datetime
import mimetypes
import os
import pysftp
import stat
import settings

from config import SFTP_SERVER, SFTP_USERNAME, SFTP_PASSWORD, \
                    SFTP_DIR, DOWNLOAD_DIR
from .forms import UploadFileForm, DropZoneForm
from .models import DropZoneModel

def home(request):
    if (request.user.is_authenticated()):
        return render(request, 'demo/home.html', \
          context={'current_time':datetime.datetime.utcnow()})
    return login(request, template_name='demo/home.html')

@login_required
def profile(request):
    return render(request, template_name='demo/profile.html')

@login_required
def upload_file_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                #handle_uploaded_file(request.FILES['file'])
                handle_uploaded_file_sftp(request.FILES['file'])
            except Exception as err:
                print err
            else:
                return HttpResponseRedirect(reverse('upload_success'))
    else:
        form = UploadFileForm()
    return render(request, 'demo/upload_file.html', {'form': form})

@login_required
def upload_success_view(request):
    return render(request, 'demo/upload_success.html', \
      {'sftp_dir':SFTP_DIR,'sftp_server':SFTP_SERVER})

def handle_uploaded_file(f):
    #with open('/root/uploaded_files/uploaded_'+datetime.datetime.now().strftime("%d%m%y_%H%M%S")+'.txt', 'wb+') as destination:
    with open(os.path.join(settings.MEDIA_ROOT, f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@login_required
def handle_uploaded_file_sftp(request,f):
    with pysftp.Connection(SFTP_SERVER, username=SFTP_USERNAME,\
    password=SFTP_PASSWORD) as sftp:
        sftp.chdir(SFTP_DIR)
        sftp.put(os.path.join(settings.MEDIA_ROOT, f.name))
        #pdb.set_trace()

@login_required
def dropzone_view(request):
    if request.method == 'POST':
        form = DropZoneForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = DropZoneModel(file = request.FILES['file'], user=request.user)
            new_file.save()
            handle_uploaded_file_sftp(request,new_file.file)

            return HttpResponseRedirect(reverse('dropzone'))
    else:
        form = DropZoneForm()

    data = {'form': form}
    return render(request, 'demo/dropzone.html', context=data)

def download_file_sftp(f):
    with pysftp.Connection(SFTP_SERVER, username=SFTP_USERNAME,\
    password=SFTP_PASSWORD) as sftp:
        sftp.chdir(SFTP_DIR)
        sftp.get(f,localpath=DOWNLOAD_DIR+f)

@login_required
def downloads_view(request):
    if (request.user.is_authenticated()):
        if not request.user.is_superuser and not request.user.is_staff:
            files = DropZoneModel.objects.filter(user = request.user)
        else:
            files = DropZoneModel.objects.all()
        names = [f.file for f in files]
        users = [f.user_id for f in files]
        data = zip(names,users)
        return render(request, 'demo/downloads.html', \
          context={'files':files,'data':data})
    return render(request, template_name='demo/downloads.html')

@login_required
def download_file_view(request):
    file_name = request.path.split("/download_file/")[1]
    download_file_sftp(file_name)
    mime_type = mimetypes.MimeTypes().guess_type(DOWNLOAD_DIR+file_name)[0] 
    with open(DOWNLOAD_DIR+file_name) as text_file:
        response = HttpResponse(text_file.read())
        response['content_type'] = mime_type
        response['Content-Disposition'] = 'attachment;filename='+file_name
        return response
