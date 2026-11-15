from django.urls import path

from .views import my_api_view,create_user,login_user

urlpatterns = [
    path('my-api/', my_api_view, name='my_api'),
    path('user-signup/', create_user, name='user_signup'),
    path('user-login/', login_user, name='user_login'),

]