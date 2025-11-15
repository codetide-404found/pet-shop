from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from .models import Product


from django.http import HttpResponse
def debug_products(request):
    names = ", ".join(p.name for p in Product.objects.all())
    return HttpResponse(f"Products in DB: {names}")


# ------------------ HOME / INDEX ------------------ #

def index(request):
    """Pet shop home page."""
    products = Product.objects.filter(available=True).order_by("name")
    return render(request, "pets/index.html", {"products": products})


# ------------------ CART VIEW ------------------ #

def view_cart(request):
    """
    Displays cart items stored in session.
    Cart format: {"<product_id>": quantity}
    """
    session_cart = request.session.get("cart", {})
    cart_items = []

    for product_id_str, qty in session_cart.items():
        try:
            product_id = int(product_id_str)
            product = Product.objects.get(pk=product_id)
        except (ValueError, Product.DoesNotExist):
            continue

        quantity = int(qty)
        cart_items.append({
            "id": product.id,
            "name": product.name,
            "quantity": quantity,
            "image_url": product.image.url if getattr(product, "image", None) else None,
            "available": product.available,
            "stock": product.stock,
        })

    context = {"cart_items": cart_items}
    return render(request, "pets/cart.html", context)


# ------------------ CART ACTIONS ------------------ #

def _is_ajax(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


def _cart_summary(cart):
    """Return simple cart item count."""
    total_items = sum(int(q) for q in cart.values())
    return {"total_items": total_items}


def add_to_cart(request, product_id):
    if request.method not in ("GET", "POST"):
        return HttpResponseNotAllowed(["GET", "POST"])

    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get("cart", {})

    qty = 1
    if request.method == "POST":
        try:
            qty = int(request.POST.get("quantity", 1))
        except (ValueError, TypeError):
            return HttpResponseBadRequest("Invalid quantity")

    if qty <= 0:
        return HttpResponseBadRequest("Quantity must be >= 1")

    key = str(product_id)
    cart[key] = int(cart.get(key, 0)) + qty
    request.session["cart"] = cart
    request.session.modified = True

    if _is_ajax(request):
        return JsonResponse({"success": True, **_cart_summary(cart)})
    return redirect("pets:product_detail", pk=product_id)


def remove_from_cart(request, product_id):
    if request.method not in ("GET", "POST"):
        return HttpResponseNotAllowed(["GET", "POST"])

    cart = request.session.get("cart", {})
    key = str(product_id)
    if key in cart:
        del cart[key]
        request.session["cart"] = cart
        request.session.modified = True

    if _is_ajax(request):
        return JsonResponse({"success": True, **_cart_summary(cart)})
    return redirect("pets:cart")


def update_cart(request, product_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    try:
        quantity = int(request.POST.get("quantity", 0))
    except (ValueError, TypeError):
        return HttpResponseBadRequest("Invalid quantity")

    cart = request.session.get("cart", {})
    key = str(product_id)

    if quantity <= 0:
        cart.pop(key, None)
    else:
        cart[key] = quantity

    request.session["cart"] = cart
    request.session.modified = True

    if _is_ajax(request):
        return JsonResponse({"success": True, **_cart_summary(cart)})
    return redirect("pets:cart")


# ------------------ PRODUCT PAGES ------------------ #

def product_list(request):
    """List all available pets/products (paginated)."""
    qs = Product.objects.filter(available=True).order_by("name")
    paginator = Paginator(qs, 12)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj, "products": page_obj.object_list}
    return render(request, "pets/product_list.html", context)


def product_detail(request, pk):
    """Show details for a single pet/product."""
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, "pets/product_detail.html", context)


# ------------------ CHECKOUT & ORDER CONFIRMATION ------------------ #

@require_http_methods(["GET", "POST"])
def checkout(request):
    """
    Placeholder checkout page.
    On POST → clears cart and redirects to order confirmation.
    """
    if request.method == "POST":
        request.session.pop("cart", None)
        request.session.modified = True
        return redirect("pets:order_confirmation")

    return render(request, "pets/checkout.html")



@require_http_methods(["GET"])
def order_confirmation(request):
    """Order confirmation page."""
    return render(request, "pets/order_confirmation.html")
