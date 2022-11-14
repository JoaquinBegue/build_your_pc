from django.urls import path

from . import views

app_name = 'builder'

urlpatterns = [
    # Index page / Brand choosing page.
    path('', views.index, name='index'),
    # Component choosing page.
    path('choose_component/<order_id>/<comp>', views.choose_component,
        name='choose_component'),
    # Order review page.
    path('order_review/<order_id>', views.order_review, name='order_review')
]