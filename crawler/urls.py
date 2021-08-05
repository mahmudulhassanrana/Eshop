from django.urls import path
from . import views

urlpatterns = [
    path('search', views.showProduct, name="search"),
    #path('<product_title>/<search_item>', views.singlee_Product, name="singlee_Product"),
    path('compare', views.compare, name="compare_Product"),
    path('compare_show', views.compare_show, name="compare_show"),
    path('<id>', views.single_Product, name="single_Product"),
]
