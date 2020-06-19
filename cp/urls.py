from django.urls import path

from . import views

app_name = 'cp'
urlpatterns = [
    path('', views.LoginFormView.as_view(), name='login'),
    path('pwlost', views.PwResetFormView.as_view(), name='reset'),
    path('signup', views.RegisterFormView.as_view(), name='register'),
    path('signin', views.LoginFormView.as_view(), name='login'),
    path('register', views.RegisterResultView.as_view(), name='register_result'),
    path('verify/<str:token>/', views.VerifyView.as_view(), name='verify')
]
