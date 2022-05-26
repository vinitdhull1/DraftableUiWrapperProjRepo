from django import forms
from .models import UserFiles

class UploadFilesForm(forms.ModelForm):
    class Meta:
        model = UserFiles
        fields = ('left_file', 'right_file', )