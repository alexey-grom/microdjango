#!/usr/bin/env python

from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.views.generic import ListView, CreateView

from microdjango import MicroDjango


app = MicroDjango(
    INSTALLED_APPS=(
        'django.contrib.staticfiles',
        'debug_toolbar',
        'django_extensions',
    ),
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'example.sqlite3',
        },
    },
    STATIC_URL='/static/',
)


class Item(models.Model):
    title = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True)


class Other(models.Model):
    value = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)


class ItemListView(ListView):
    model = Item
    template_name = 'list.html'


class ItemCreateView(CreateView):
    model = Item
    template_name = 'create.html'
    fields = 'title',
    success_url = reverse_lazy('list')


app.urlpatterns.extend([
    url(r'^$', ItemListView.as_view(), name='list'),
    url(r'^create/$', ItemCreateView.as_view(), name='create'),
])


if __name__ == '__main__':
    app.syncdb()
    app.run()
