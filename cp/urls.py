from django.urls import path

from . import views

app_name = 'cp'
urlpatterns = [
    path('', views.LoginFormView.as_view(), name='login'),
    path('pwlost', views.PwResetFormView.as_view(), name='login'),
    path('signup', views.RegisterFormView.as_view(), name='login'),
    path('signin', views.LoginFormView.as_view(), name='login'),
]
