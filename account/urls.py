from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='account'),
    path('login', views.login_action, name='login'),
    path('signup', views.signup_action, name='signup'),
    path('logout', views.logout_action, name='logout'),
    path('history', views.history_action, name='history'),
]