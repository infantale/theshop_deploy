from django.urls import path

from .views import *

app_name = 'core'
urlpatterns = [
    path('accounts/logout/', TSLogoutView.as_view(), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('login/', TSLoginView.as_view(), name='login'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]
