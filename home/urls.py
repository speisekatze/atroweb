from django.urls import path

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('impressum', views.ImpressumView.as_view(), name='impressum'),
    path('datenschutz', views.DatenschutzView.as_view(), name='datenschutz'),
]
