from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
# from django.conf import settings
from .validators import validate_zip_extension, validate_image_extension


class Album(models.Model):
    title = models.CharField(max_length=140)
    body = models.TextField(max_length=250, verbose_name='Description')
    date = models.DateTimeField(auto_now=True, auto_now_add=False)
    # file will be uploaded to MEDIA_ROOT/uploads

    archive = models.FileField(upload_to='albums/',
                               validators=[validate_zip_extension],
                               verbose_name='Zip file archive'
                               )
    cover = models.FileField(upload_to='albums/covers', blank=True, null=True, validators=[validate_image_extension])
    user = models.ForeignKey(User, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('photos:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
