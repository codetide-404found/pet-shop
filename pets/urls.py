from django.urls import path
from . import views

app_name = "pets"

urlpatterns = [
    path("debug-products/", views.debug_products, name="debug_products"),

    path("", views.index, name="index"),  # Home page
    path("list/", views.product_list, name="product_list"),  # All products
    path("<int:pk>/", views.product_detail, name="product_detail"),  # Single product details

    # Cart routes
    path("cart/", views.view_cart, name="cart"),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("update/<int:product_id>/", views.update_cart, name="update_cart"),

    # Checkout and order confirmation
    path("checkout/", views.checkout, name="checkout"),
    path("order-confirmation/", views.order_confirmation, name="order_confirmation"),
   
]