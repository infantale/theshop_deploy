from django.urls import path

from .views import *

app_name = 'core'
urlpatterns = [
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/logout/', TSLogoutView.as_view(), name='logout'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/change/<int:pk>/', profile_bb_change, name='profile_bb_change'),
    path('accounts/profile/delete/<int:pk>/', profile_bb_delete, name='profile_bb_delete'),
    path('accounts/profile/add/', profile_bb_add, name='profile_bb_add'),
    path('accounts/profile/<int:pk>/', profile_bb_detail, name='profile_bb_detail'),
    path('accounts/profile/', profile, name='profile'),
    path('login/', TSLoginView.as_view(), name='login'),
    path('<int:category_pk>/<int:pk>/', detail, name='detail'),
    path('<int:pk>/', by_category, name='by_category'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]
