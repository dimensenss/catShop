from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.http import HttpResponseRedirect

from carts.models import Cart
from orders.models import Order
from users.forms import RegisterUserForm, LoginUserForm

User = get_user_model()
class SignUpUserView(CreateView):
    template_name = 'users/signup.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('goods:main')

    def form_valid(self, form):
        user = form.instance
        if user:
            form.save()

            session_key = self.request.session.session_key
            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

                existing_orders = Order.objects.filter(session=session_key)

                if existing_orders:
                    User.objects.get(username=existing_orders[0].user.username).delete()
                    for order in existing_orders:
                        order.user = user
                        order.save()

            auth.login(self.request, user)
            return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Реєстрація'
        return context


class LoginUserView(LoginView):
    template_name = 'users/login.html'
    form_class = LoginUserForm

    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('users:logout'):
            return redirect_page
        return reverse_lazy('goods:main')

    def form_valid(self, form):
        user = form.get_user()
        session_key = self.request.session.session_key
        if user:
            auth.login(self.request, user)
            if session_key:
                Cart.objects.filter(user=user).delete()
                Cart.objects.filter(session_key=session_key).update(user=user)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизація'
        return context


def logout(request):
    auth.logout(request)
    referer_url = request.META.get('HTTP_REFERER')
    if referer_url:
        return HttpResponseRedirect(referer_url)
    else:
        return redirect('users:login')
