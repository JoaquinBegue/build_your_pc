from django.urls import path

from . import views

app_name = 'builder'

urlpatterns = [
    # Index page / Brand choosing page.
    path('', views.index, name='index'),
    # CPU choosing page.
    path('cpu/<order>', views.cpu, name='cpu'),
    # Motherboard choosing page.
    path('motherboard/<order>/', views.motherboard, name='motherboard'),
]