from django.urls import path

from . import views

app_name = 'checkout'
urlpatterns = [
    path('', views.cartitem, name='cartitem'),
    path('adicionar/<slug:slug>/', views.add_cartitem, name='add_cartitem'),
    path('finalizar', views.checkout, name='checkout'),
    path('meus-pedidos', views.order_list, name='order_list'),
    path('meus-pedidos/<int:pk>/', views.order_detail, name='order_detail'),
    path('finalizar/<int:pk>/pagseguro/', views.pagseguro, name='pagseguro'),
    path('notificacoes/pagseguro/', views.pagseguro_notification, name='pagseguro_notification'),
    path('finalizando/<int:pk>/paypal/', views.paypal, name='paypal'),
]
