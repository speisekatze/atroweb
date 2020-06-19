from django.urls import path, re_path

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('impressum', views.ImpressumView.as_view(), name='impressum'),
    path('datenschutz', views.DatenschutzView.as_view(), name='datenschutz'),
    path('faq', views.FaqView.as_view(), name='faq'),
    re_path(r'^.*/$', views.go_fuck_yourself, name='fuck')
]
