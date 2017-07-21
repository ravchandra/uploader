from django import forms

class UploadFileForm(forms.Form):
    #title = forms.CharField(max_length=50)
    file = forms.FileField()

class DragUploadFileForm(forms.Form):
    #title = forms.CharField(max_length=50)
    file = forms.FileField()
