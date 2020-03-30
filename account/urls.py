from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_action, name='login'),
    path('signup', views.signup_action, name='signup'),
    path('logout', views.logout_action, name='logout'),
]