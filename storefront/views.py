from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from shop.models import Category, Product, Cart, CartItem, Order, OrderItem
from users.models import Profile
from .forms import RegisterForm, LoginForm, ProfileForm, CheckoutForm


def _cart_count(user):
    if not user.is_authenticated:
        return 0
    cart, _ = Cart.objects.get_or_create(user=user)
    return sum(i.quantity for i in cart.items.all())


def home(request):
    q = request.GET.get('q', '').strip()
    products = Product.objects.all().order_by('-created_at')
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))

    categories = Category.objects.all()
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    return render(request, 'storefront/home.html', {
        'products': products,
        'categories': categories,
        'query': q,
        'cart_count': _cart_count(request.user),
    })


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz!")
        return redirect('home')
    return render(request, 'storefront/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = LoginForm(request.POST or None)
    error = None
    if request.method == 'POST' and form.is_valid():
        user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next') or 'home')
        error = "Login yoki parol noto'g'ri"
    return render(request, 'storefront/login.html', {'form': form, 'error': error})


def logout_view(request):
    logout(request)
    messages.info(request, "Tizimdan chiqdingiz")
    return redirect('home')


@login_required(login_url='login')
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Profil saqlandi")
        return redirect('profile')
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'storefront/profile.html', {
        'form': form,
        'orders': orders,
        'cart_count': _cart_count(request.user),
    })


@login_required(login_url='login')
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'storefront/cart.html', {
        'cart': cart,
        'cart_count': _cart_count(request.user),
    })


@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        item.quantity = 1
    else:
        item.quantity += 1
    item.save()
    messages.success(request, f"“{product.name}” savatga qo'shildi")
    return redirect(request.META.get('HTTP_REFERER') or 'home')


@login_required(login_url='login')
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            item.quantity += 1
            item.save()
        elif action == 'decrease':
            item.quantity -= 1
            if item.quantity <= 0:
                item.delete()
            else:
                item.save()
        elif action == 'remove':
            item.delete()
    return redirect('cart')


@login_required(login_url='login')
def checkout_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    if not cart.items.exists():
        messages.warning(request, "Savat bo'sh")
        return redirect('cart')

    form = CheckoutForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        order = form.save(commit=False)
        order.user = request.user
        order.total_price = cart.total_price
        order.save()
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity,
            )
        cart.items.all().delete()
        return render(request, 'storefront/order_success.html', {'order': order})
        from django.http import JsonResponse
from django.conf import settings as dj_settings

def debug_csrf(request):
    return JsonResponse({
        "CSRF_TRUSTED_ORIGINS": dj_settings.CSRF_TRUSTED_ORIGINS,
        "ALLOWED_HOSTS": dj_settings.ALLOWED_HOSTS,
        "DEBUG": dj_settings.DEBUG,
    })

    return render(request, 'storefront/checkout.html', {
        'form': form,
        'cart': cart,
        'cart_count': _cart_count(request.user),
    })
from django.http import JsonResponse
from django.conf import settings as dj_settings

def debug_csrf(request):
    return JsonResponse({
        "CSRF_TRUSTED_ORIGINS": dj_settings.CSRF_TRUSTED_ORIGINS,
        "ALLOWED_HOSTS": dj_settings.ALLOWED_HOSTS,
        "DEBUG": dj_settings.DEBUG,
    })
