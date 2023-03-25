from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

from .views import ResetPasswordView

app_name = 'skydive'
urlpatterns = [
    path("", views.index, name="index"),
    path('skydive/login', views.login, name='login'),
    path('skydive/register', views.register, name='register'),
    path('skydive/logout', views.logout, name='logout'),
    path('skydive/reset', ResetPasswordView.as_view(), name='reset'),
    path('skydive/password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='skydive/password_reset_confirm.html',
                                                     success_url=reverse_lazy('skydive:password_reset_complete')),
         name='password_reset_confirm'),
    path('skydive/password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='skydive/password_reset_complete.html'),
         name='password_reset_complete'),
    path('skydive/search', views.search, name='search'),
    path('skydive/search/<str:destination>', views.search_loc, name='search_loc'),
    path('skydive/search/<str:skydive_type>/<int:desc_id>', views.type_skydive, name='type_skydive'),
]
