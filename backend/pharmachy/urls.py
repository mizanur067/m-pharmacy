from django.urls import path

from .views import my_api_view,create_user,login_user,create_staff,login_staff

urlpatterns = [
    path('my-api/', my_api_view, name='my_api'),
    path('user-signup/', create_user, name='user_signup'),
    path('user-login/', login_user, name='user_login'),
    path('staff-signup/', create_staff, name='staff_signup'),
    path('staff-login/', login_staff, name='staff_login'),

]