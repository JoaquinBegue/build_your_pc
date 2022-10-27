from django.urls import path

from . import views

app_name = 'builder'

urlpatterns = [
    # Index page / Brand choosing page.
    path('', views.index, name='index'),
    # CPU choosing page.
    path('cpu/<order_id>', views.cpu, name='cpu'),
    # Motherboard choosing page.
    path('motherboard/<order_id>/', views.motherboard, name='motherboard'),
    # GPU choosing page.
    path('gpu/<order_id>/', views.gpu, name='gpu'),
    # RAM choosing page.
    path('ram/<order_id>/', views.ram, name='ram'),
    # Order review page.
    path('order_review/<order_id>/', views.order_review, name='order_review'),
]