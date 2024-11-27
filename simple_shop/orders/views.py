from email.mime.image import MIMEImage

from django.contrib import messages, auth
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.db.models import Prefetch, F
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from carts.models import Cart
from .tasks import send_order_to_queue
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem
User = get_user_model()

def create_order(request):
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    session_key = request.session.session_key
                    if request.user.is_authenticated:
                        user = request.user
                    elif User.objects.filter(email=form.cleaned_data['email']):
                        messages.warning(request, 'Користувач з таким email вже існує. Будь ласка, увійдіть.')
                        return redirect('orders:create_order')

                    elif form.cleaned_data['requires_registration'] == '1':
                        user = User.objects.create_user(
                            username=form.cleaned_data['email'],
                            email=form.cleaned_data['email'],
                            password=form.cleaned_data['password1'],
                            first_name=form.cleaned_data['first_name'],
                            last_name=form.cleaned_data['last_name'],
                        )
                        user.save()
                        user.backend = 'users.authentication.EmailAuthBackend'

                        Cart.objects.filter(session_key=session_key).update(user=user)

                    elif form.cleaned_data['requires_registration'] == '0':  # Не авторизирован и не хочет рег
                        user = User.objects.create_user(User.objects.make_random_password(),
                                                        User.objects.make_random_password(),
                                                        first_name=form.cleaned_data['first_name'],
                                                        last_name=form.cleaned_data['last_name'])
                        Cart.objects.filter(session_key=session_key).update(user=user)

                    cart_items = Cart.objects.filter(user=user)

                    if cart_items.exists():
                        order = Order.objects.create(
                            user=user,
                            email=form.cleaned_data['email'],
                            requires_delivery=form.cleaned_data['requires_delivery'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_on_get=form.cleaned_data['payment_on_get'],
                            session=session_key
                        )
                        for cart_item in cart_items:
                            product = cart_item.product
                            title = cart_item.product.title
                            price = cart_item.product.price
                            quantity = cart_item.quantity

                            if product.quantity < quantity:
                                raise ValidationError(f'Недостатня кількість товарів {title} на складі \
                                В наявності - {product.quantity}')

                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=title,
                                price=price,
                                quantity=quantity,
                            )
                            product.quantity -= quantity
                            product.save()

                        cart_items.delete()
                        send_order_to_queue.delay(order.id)
                        messages.success(request, 'Замовлення оформлено!')

                        if form.cleaned_data['requires_registration'] == '1':
                            user.backend = 'users.authentication.EmailAuthBackend'
                            login(request, user, backend='users.authentication.EmailAuthBackend')

                        if request.user.is_authenticated:
                            return redirect('orders:success_order', order_id=order.id)

                        if form.cleaned_data['requires_registration'] == '0':
                            return redirect('goods:main')

                    else:
                        raise ValidationError(f'Ваш кошик порожній')

            except ValidationError as e:
                messages.warning(request, '; '.join(e.messages))
                return redirect('orders:create_order')
    else:
        if request.user.is_authenticated:
            initial = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
            form = CreateOrderForm(initial=initial)
        else:
            form = CreateOrderForm()

    context = {'form': form, 'order': True, 'title': "Створення замовлення", 'request':request}

    return render(request, 'create_order.html', context=context)

@login_required
def success_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if order.user != request.user:
        messages.warning(request, 'У вас немає доступу до цього замовлення')
        return redirect('goods:main')

    orders = Order.objects.filter(user=request.user).prefetch_related(
        Prefetch(
            "orderitem_set",
            queryset=OrderItem.objects.select_related("product").annotate(
                product_slug=F("product__slug"),
            ),
        )
    ).order_by("-id")

    return render(request, 'success_order.html', {'orders': orders, 'order': order})