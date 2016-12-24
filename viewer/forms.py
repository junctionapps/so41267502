import zipfile

from django import forms
from django.forms import ModelForm, Form

from viewer.models import Album


class AlbumUploadForm(ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'body', 'archive']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Enter a title'}),
            'body': forms.Textarea(attrs={'placeholder': 'Enter a description',
                                          'class': 'form-control bound-data-field',
                                          'rows': 2, }),
            #'archive': forms.FileField(),
        }


class CoverForm(Form):
    def __init__(self, *args, **kwargs):

        album = kwargs.pop('album', None)

        with zipfile.ZipFile(album.archive, 'r') as z:
            choices = [(f,f) for f in z.namelist()]

        super(CoverForm, self).__init__(*args, **kwargs)

        self.fields['cover'] = forms.CharField(
            label='Select a cover',
            widget=forms.Select(attrs={'class': 'form-control', },
                                choices=choices),
        )

