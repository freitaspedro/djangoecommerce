import logging

from pagseguro import PagSeguro

from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import RedirectView, TemplateView, ListView, DetailView
from django.forms import modelformset_factory
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from catalog.models import Product

from .models import CartItem, Order


logger = logging.getLogger('checkout.views')


class PagSeguroView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        order_pk = self.kwargs.get('pk')
        order = get_object_or_404(Order.objects.filter(user=self.request.user), pk=order_pk)
        pagseguro = order.pagseguro()
        pagseguro.redirect_url = self.request.build_absolute_uri(reverse('checkout:order_detail', args=[order.pk]))
        pagseguro.notification_url = self.request.build_absolute_uri(reverse('checkout:pagseguro_notification'))
        response = pagseguro.checkout()
        return response.payment_url


pagseguro = PagSeguroView.as_view()



class PaypalView(LoginRequiredMixin, TemplateView):

    template_name = 'paypal.html'

    def get_context_data(self, **kwargs):
        context = super(PaypalView, self).get_context_data(**kwargs)
        order_pk = self.kwargs.get('pk')
        order = get_object_or_404(Order.objects.filter(user=self.request.user), pk=order_pk)
        paypal_dict = order.paypal()
        paypal_dict['return_url'] = self.request.build_absolute_uri(reverse('checkout:order_list'))
        paypal_dict['cancel_return'] = self.request.build_absolute_uri(reverse('checkout:order_list'))
        paypal_dict['notify_url'] = self.request.build_absolute_uri(reverse('paypal-ipn'))
        context['form'] = PayPalPaymentsForm(initial=paypal_dict)
        return context


paypal = PaypalView.as_view()



class OrderListView(LoginRequiredMixin, ListView):

    template_name = 'order_list.html'
    paginate_by = 3

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


order_list = OrderListView.as_view()



class OrderDetailView(LoginRequiredMixin, DetailView):

    template_name = 'order_detail.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


order_detail = OrderDetailView.as_view()



class CheckoutView(LoginRequiredMixin, TemplateView):

    template_name = 'checkout.html'

    def get(self, request, *args, **kwargs):
        session_key = request.session.session_key
        if session_key and CartItem.objects.filter(cart_key=session_key).exists():
            cart_items = CartItem.objects.filter(cart_key=session_key)
            order = Order.objects.add_order(user=request.user, cart_items=cart_items)
            cart_items.delete()
        else:
            messages.info(request, 'Não há itens no carrinho de compras')
            return redirect('checkout:cartitem')
        response = super(CheckoutView, self).get(request, *args, **kwargs)
        response.context_data['order'] = order
        return response


checkout = CheckoutView.as_view()



class AddCartItemView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        logger.debug('Produto %s adicionado ao carrinho' % product)
        if self.request.session.session_key is None:
            self.request.session.save()
        cart_item, created = CartItem.objects.add_item(self.request.session.session_key, product)
        if created:
            messages.success(self.request, 'Produto adicionado com sucesso')
        else:
            messages.success(self.request, 'Produto atualizado com sucesso')
        return reverse('checkout:cartitem')


add_cartitem = AddCartItemView.as_view()



class CartItemView(TemplateView):

    template_name = 'cart.html'

    def get_formset(self, clear=False):
        CartItemFormSet = modelformset_factory(CartItem, fields=('quantity',), can_delete=True, extra=0)
        session_key = self.request.session.session_key
        if session_key:
            if clear:
                formset = CartItemFormSet(queryset=CartItem.objects.filter(cart_key=session_key))
            else:
                formset = CartItemFormSet(queryset=CartItem.objects.filter(cart_key=session_key), data=self.request.POST or None)
        else:
            formset = CartItemFormSet(queryset=CartItem.objects.none())
        return formset

    def get_context_data(self, **kwargs):
        context = super(CartItemView, self).get_context_data(**kwargs)
        context['formset'] = self.get_formset()
        return context

    def post(self, request, *args, **kwargs):
        formset = self.get_formset()
        context = self.get_context_data(**kwargs)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Carrinho atualizado com sucesso')
            context['formset'] = self.get_formset(clear=True)
        return self.render_to_response(context)


cartitem = CartItemView.as_view()



@csrf_exempt
def pagseguro_notification(request):
    notification_code = request.POST.get('notificationCode', None)
    if notification_code:
        pagseguro = PagSeguro(email=settings.PAGSEGURO_EMAIL, token=settings.PAGSEGURO_TOKEN, config={'sandbox': settings.PAGSEGURO_SANDBOX})
        notification_data = pagseguro.check_notification(notification_code)
        status = notification_data.status
        reference = notification_data.reference
        try:
            order = Order.objects.get(pk=reference)
        except Order.DoesNotExist:
            pass
        else:
            order.pagseguro_update_status(status)
    return HttpResponse('OK')


def paypal_notification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED and ipn_obj.receiver_email == settings.PAYPAL_EMAIL:
        try:
            order = Order.objects.get(pk=ipn_obj.invoice)
            order.complete()
        except Order.DoesNotExist:
            pass

valid_ipn_received.connect(paypal_notification)