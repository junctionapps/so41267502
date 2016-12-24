from django.conf.urls import url, include

from viewer import views
# namespaced as viewer

urlpatterns = [

    url(r'^album/(?P<album_id>[0-9]+)/', views.album, name='album'),
    url(r'^$', views.home, name='home'),

]
