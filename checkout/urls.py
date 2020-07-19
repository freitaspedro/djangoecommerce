from django.urls import path

from . import views

app_name = 'checkout'
urlpatterns = [
    path('', views.cartitem, name='cartitem'),
    path('adicionar/<slug:slug>/', views.add_cartitem, name='add_cartitem'),
    path('finalizar', views.checkout, name='checkout'),
    path('meus-pedidos', views.order_list, name='order_list'),
    path('meus-pedidos/<int:pk>/', views.order_detail, name='order_detail'),
]
