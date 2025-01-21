from .views import ListView
from django.urls import path
urlpatterns=[
    path('list/',ListView.as_view(),name='list'),
]