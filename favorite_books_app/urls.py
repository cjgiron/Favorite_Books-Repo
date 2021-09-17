from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('login_process', views.login_process),
    path('dashboard', views.dashboard),
    path('register_process', views.register_process),
    path('logout', views.logout),
    path('process_book', views.process_book),
]