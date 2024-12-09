from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path("", views.index, name='index'),
#    path("register", views.register, name='register'),
#    path("register/action", views.register_action, name='register_action'),
#    path("test", views.test, name='test'),
]
