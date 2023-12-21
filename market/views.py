from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from .models import Product, Order
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, UserAuthenticationForm, ProductCreationForm, ProductForm
import json


# Проверка на админа
def is_admin(user):
    return user.is_authenticated and user.isAdmin


admin_required = user_passes_test(is_admin, login_url='login_user')


# Подробная информация о продукте
class ProductDetailView(View):
    template_name = 'product_detail.html'

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        return render(request, self.template_name, {'product': product})


def display_full_image(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'full_image_display.html', {'product': product})


def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Создаем или обновляем корзину в сессии
    cart = request.session.get('cart', {})
    if str(product_id) in cart.keys():
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1
    request.session['cart'] = cart

    return redirect('product_detail', product_id=product_id)


def cart_view(request):
    cart = dict(request.session.get('cart', {}))
    print(cart.items())
    products = Product.objects.filter(id__in=cart.keys())
    total_price = sum(product.price * cart[str(product.id)] for product in products)
    return render(request, 'cart.html', {'products': products, 'total_price': total_price, 'cart': cart})


def remove_from_cart_view(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart')


def submit_order_view(request):
    # Логика обработки заказа...

    # Пример сохранения заказа в базе данных
    cart = request.session.get("cart", {})
    products = Product.objects.filter(id__in=cart.keys())
    order = Order.objects.create(total_price=sum(product.price * cart[str(product.id)] for product in products),
                                 positions=json.dumps(cart))

    send_mail(
        'Новый заказ',
        'Номер заказа: {}'.format(order.id),
        'from@example.com',
        ['to@example.com'],
        fail_silently=True,
    )

    request.session['cart'] = {}

    return render(request, 'success.html')


# Список продуктов
class ProductListView(View):
    template_name = 'product_list.html'

    def get(self, request):
        sort_by = request.GET.get('sort_by', 'name')
        search_query = request.GET.get('q', '')
        products = Product.objects.all()

        if search_query:
            products = products.filter(name__icontains=search_query)

        if sort_by == 'price_asc':
            products = products.order_by('price')
        elif sort_by == 'price_desc':
            products = products.order_by('-price')
        elif sort_by == 'quantity_asc':
            products = products.order_by('stock_quantity')
        elif sort_by == 'quantity_desc':
            products = products.order_by('-stock_quantity')
        if request.user.is_authenticated and request.user.isAdmin:
            return render(request, 'admin_product_list.html', {'products': products})
        else:
            return render(request, self.template_name, {'products': products})


# регистрация пользователя
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


# Аутентификация пользователя
def login_user(request):
    if request.method == 'POST':
        form = UserAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product_list')
    else:
        form = UserAuthenticationForm()

    return render(request, 'login.html', {'form': form})


#
@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductCreationForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            return redirect('product_list')  # Замените 'product_list' на ваш путь к списку продуктов
    else:
        form = ProductCreationForm(request.user)

    return render(request, 'create_product.html', {'form': form})


@admin_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


@admin_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Замените 'product_list' на имя вашего URL для списка продуктов
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})
