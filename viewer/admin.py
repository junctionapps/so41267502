from django.contrib import admin
from viewer.models import Album


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'date', 'user')

