from django.urls import path

from . import views

app_name = 'cp'
urlpatterns = [
    path('', views.LoginFormView.as_view(), name='index'),
    path('pwlost', views.PwResetFormView.as_view(), name='pwlost'),
    path('pwsent', views.PwSentView.as_view(), name='pwsent'),
    path('signup', views.RegisterFormView.as_view(), name='register'),
    path('signin', views.LoginFormView.as_view(), name='signin'),
    path('register', views.RegisterResultView.as_view(), name='register_result'),
    path('verify/<str:token>/', views.VerifyView.as_view(), name='verify'),
    path('reset/<str:token>/', views.NewPasswdView.as_view(), name='newpw_token'),
    path('reset/', views.NewPasswdView.as_view(), name='newpw'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
