from __future__ import unicode_literals 
from django.shortcuts import render
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .forms import UploadFileForm
import datetime
#from .utils handle_uploaded_file

def home(request):
    if (request.user.is_authenticated()):
        return render(request, 'demo/home.html')
    return login(request, template_name='demo/home.html')

@login_required
def profile(request):
    return render(request, template_name='demo/profile.html')

@login_required
def upload_file_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect(reverse('upload_success'))
    else:
        form = UploadFileForm()
    return render(request, 'demo/upload_file.html', {'form': form})

@login_required
def upload_success_view(request):
    return render(request, 'demo/upload_success.html')

def handle_uploaded_file(f):
    #with open('/root/uploaded_files/uploaded_'+datetime.datetime.now().strftime("%d%m%y_%H%M%S")+'.txt', 'wb+') as destination:
    with open('/root/uploaded_files/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
