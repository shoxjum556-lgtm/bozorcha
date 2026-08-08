from django.urls import path

from .views import (
    CategoryListView, ProductListView, ProductDetailView,
    CartView, CartAddItemView, CartItemDetailView,
    OrderListView, OrderCreateView,
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),

    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    path('cart/', CartView.as_view(), name='cart-detail'),
    path('cart/add/', CartAddItemView.as_view(), name='cart-add'),
    path('cart/item/<int:pk>/', CartItemDetailView.as_view(), name='cart-item-detail'),

    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
]
