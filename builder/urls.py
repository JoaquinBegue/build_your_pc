from django.urls import path

from . import views

app_name = 'builder'

urlpatterns = [
    # Index page / Brand choosing page.
    path('', views.index, name='index'),
    # CPU choosing page.
    path('choose_component/<order_id>/<comp>', views.choose_component,
        name='choose_cpu'),
    # Motherboard choosing page.
    path('choose_component/<order_id>/<comp>', views.choose_component,
        name='choose_motherboard'),
    # GPU choosing page.
    path('choose_component/<order_id>/<comp>', views.choose_component,
        name='choose_gpu'),
    # RAM choosing page.
    path('choose_component/<order_id>/<comp>', views.choose_component,
        name='choose_ram'),
    # Ref. System choosing page.
    path('choose_component/<order_id>/<comp>', views.choose_component,
        name='choose_ref_system'),
    # Case choosing page.
    path('choose_component/<order_id>/<comp>', views.choose_component,
        name='choose_case'),
    # Power SUpply choosing page.
    path('choose_component/<order_id>/<comp>', views.choose_component,
        name='choose_power_supply'),
    # Order review page.
    path('order_review/<order_id>/', views.order_review, name='order_review')
]