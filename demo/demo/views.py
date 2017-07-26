from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext

import datetime
import os
import pysftp
import stat
import settings

from config import SFTP_SERVER, SFTP_USERNAME, SFTP_PASSWORD, \
                    SFTP_DIR
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

def handle_uploaded_file_sftp(f):
    with open(os.path.join(settings.MEDIA_ROOT , f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        #os.chmod(os.path.join(FILE_DIR , f.name), 0666)

    with pysftp.Connection(SFTP_SERVER, username=SFTP_USERNAME, password=SFTP_PASSWORD) as sftp:
        sftp.chdir(SFTP_DIR)
        sftp.put(os.path.join(settings.MEDIA_ROOT, f.name))
        #pdb.set_trace()

@login_required
def dropzone_view(request):
    if request.method == 'POST':
        form = DropZoneForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = DropZoneModel(file = request.FILES['file'])
            new_file.save()
            #handle_uploaded_file_sftp(request.FILES['file'])

            return HttpResponseRedirect(reverse('dropzone'))
    else:
        form = DropZoneForm()

    data = {'form': form}
    return render(request, 'demo/dropzone.html', context=data)

