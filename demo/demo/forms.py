from django import forms
from models import DropZoneModel

class UploadFileForm(forms.Form):
    #title = forms.CharField(max_length=50)
    file = forms.FileField()

class DropZoneForm(forms.ModelForm):
    class Meta:
        model = DropZoneModel
        fields = '__all__'
