from django.urls import path

from . import views


urlpatterns = [
    path('', views.products, name='products'),
    path('<slug:slug>/', views.category, name='category'),
    path('<slug:c_slug>/<slug:p_slug>/', views.product, name='product'),
]
