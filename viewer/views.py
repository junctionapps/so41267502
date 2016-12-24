import os
import zipfile
import base64

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from viewer.forms import AlbumUploadForm, CoverForm
from viewer.models import Album


def _set_cover(album, cover_file=None):
    """ Sets the cover, picks the first one in the list if not specified"""
    save_path = '{}/{}/{}/{}'.format(settings.MEDIA_ROOT, 'albums', 'covers', album.id)
    relative_path = '{}/{}/{}'.format('albums', 'covers', album.id)
    with zipfile.ZipFile(album.archive, 'r') as z:
        if not cover_file:
            cover_file = z.namelist()[0]
        z.extract(cover_file, save_path)

    # delete cover if already there
    try:
        os.remove('{}/{}'.format(save_path, 'cover'))
    except OSError:
        pass

    # save cover as 'cover' (only one file in each album folder)
    os.rename('{}/{}'.format(save_path, cover_file),
              '{}/{}'.format(save_path, 'cover'))

    album.cover = '{}/{}'.format(relative_path, 'cover')
    album.save()


def home(request, album_id=None):
    """ Show the landing page with form for uploading a new zip archive of photos"""
    context = dict()
    instance = Album.objects.get(pk=album_id) if album_id else None

    if request.method == "POST":
        form = AlbumUploadForm(request.POST, request.FILES, instance=instance)
        print('here')
        if form.is_valid():
            obj = form.save(commit=False)
            if request.user.is_authenticated():
                obj.user = request.user
            obj.save()
            _set_cover(obj)
            return HttpResponseRedirect(reverse('viewer:home'))
    else:
        form = AlbumUploadForm(instance=instance)

    albums = Album.objects.order_by('-date')[:15]
    context.update({'albums': albums,
                    'form': form, })
    return render(request, 'viewer/home.html', context)


def album(request, album_id):
    """ Get the images from an archive, and shows them"""
    album = get_object_or_404(Album, pk=album_id)

    if request.method == "POST":
        # set the cover
        form = CoverForm(request.POST, album=album)
        if form.is_valid():
            _set_cover(album,form.cleaned_data['cover'])
    context = dict()
    images = dict()

    # probably should do some logic on the name and file type
    # or be very aware of what is in the zip file
    with zipfile.ZipFile(album.archive, 'r') as z:
        for f in z.namelist():
            images.update({f: base64.b64encode(z.read(f)),})

    form = CoverForm(album=album)
    context.update({'album': album,
                    'images': images,
                    'form': form})

    return render(request, 'viewer/album.html', context)
