from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    #sign in page
    url(r'^signin$', views.signin),
    url(r'^register$', views.register),
    url(r'^user/new$', views.create_user),
    url(r'^users/new/$', views.add_user),
    url(r'^users/edit/$', views.edit_profile),
    url(r'^users/show/(?P<id>[0-9]+)$', views.show_user),
    url(r'^users/edit/(?P<id>[0-9]+)$', views.edit_user),
    url(r'^users/update/(?P<id>[0-9]+)$', views.update_user),
    url(r'^users/delete/(?P<id>[0-9]+)$', views.delete_user),

    # new message route
    url(r'^messages/new$', views.new_message),

    # comment routes
    url(r'^comments/new$', views.new_comment),

    #log in route
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.home),
]
