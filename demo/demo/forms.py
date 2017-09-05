from django import forms
from models import DropZoneModel

class UploadFileForm(forms.Form):
    #title = forms.CharField(max_length=50)
    file = forms.FileField(allow_empty_file=True)

class DropZoneForm(forms.ModelForm):
    class Meta:
        model = DropZoneModel
        fields = ('file',)
