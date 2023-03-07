from django.urls import path
from . import views

app_name = 'skydive'
urlpatterns = [
    path("", views.index, name="index"),
    path('skydive/login', views.login, name='login'),
    path('skydive/register', views.register, name='register'),
    path('skydive/logout', views.logout, name='logout'),
]
