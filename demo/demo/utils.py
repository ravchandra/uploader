import datetime

def handle_uploaded_file(f):
    with open('/root/uploaded_files/uploaded_'+datetime.datetime.now().strftime("%d%m%y_%H%M%S")+'.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
