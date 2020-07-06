from django.urls import path

from . import views

app_name = 'checkout'
urlpatterns = [
    path('', views.cartitem, name='cartitem'),
    path('adicionar/<slug:slug>/', views.add_cartitem, name='add_cartitem'),
]
