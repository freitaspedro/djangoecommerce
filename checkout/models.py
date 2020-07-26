from pagseguro import PagSeguro

from django.db import models
from django.conf import settings

from catalog.models import Product



class OrderManager(models.Manager):

    def add_order(self, user, cart_items):
        order = self.create(user=user)
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(order=order, quantity=cart_item.quantity, product=cart_item.product, price=cart_item.price)
        return order



class Order(models.Model):

	user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete=models.CASCADE)

	STATUS_CHOICES = (
		(0, 'Aguardando Pagamento'),
		(1, 'Concluída'),
		(2, 'Cancelada'),
	)

	status = models.IntegerField('Situação', choices=STATUS_CHOICES, default=0, blank=True)

	PAYMENT_OPTION_CHOICES = (
        ('deposit', 'Depósito'),
        ('pagseguro', 'PagSeguro'),
        ('paypal', 'Paypal'),
    )
	payment_option = models.CharField('Opção de Pagamento', choices=PAYMENT_OPTION_CHOICES, max_length=20, default='deposit')

	created = models.DateTimeField('Criado em', auto_now_add=True)
	modified = models.DateTimeField('Modificado em', auto_now=True)

	objects = OrderManager()

	class Meta:
	    verbose_name = 'Pedido'
	    verbose_name_plural = 'Pedidos'

	def __str__(self):
	    return 'Pedido #{}'.format(self.pk)

	def products(self):
		products_ids = self.items.values_list('product')
		return Product.objects.filter(pk__in=products_ids)

	def total(self):
		aggregate_queryset = self.items.aggregate(
			total=models.Sum(
				models.F('price') * models.F('quantity'),
				output_field=models.DecimalField()
			)
		)
		return aggregate_queryset['total']

	def pagseguro(self):
		self.payment_option = 'pagseguro'
		self.save()
		pagseguro = PagSeguro(email=settings.PAGSEGURO_EMAIL, token=settings.PAGSEGURO_TOKEN, config={'sandbox': settings.PAGSEGURO_SANDBOX})
		pagseguro.sender = {'email': self.user.email}
		pagseguro.reference_prefix = ''
		pagseguro.shipping = None
		pagseguro.reference = self.pk
		for item in self.items.all():
		    pagseguro.items.append(
		        {
		            'id': item.product.pk,
		            'description': item.product.name,
		            'quantity': item.quantity,
		            'amount': '%.2f' % item.price
		        }
		    )
		return pagseguro

	def pagseguro_update_status(self, status):
		if status == '3':
			self.status = 1
		elif status == '7':
			self.status = 2
		self.save()

	def complete(self):
		self.status = 1
		self.save()



class OrderItem(models.Model):

    order = models.ForeignKey(Order, verbose_name='Pedido', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Produto', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=8)

    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens dos pedidos'

    def __str__(self):
        return '[{}] {}'.format(self.order, self.product)



class CartItemManager(models.Manager):

	def add_item(self, cart_key, product):
		if self.filter(cart_key=cart_key, product=product).exists():
			cart_item = self.get(cart_key=cart_key, product=product)
			cart_item.quantity = cart_item.quantity + 1
			cart_item.save()
			created = False
		else:
			cart_item = CartItem.objects.create(cart_key=cart_key, product=product, price=product.price)
			created = True
		return cart_item, created



class CartItem(models.Model):

	cart_key = models.CharField('Chave do Carrinho', max_length=40, db_index=True)
	product = models.ForeignKey(Product, verbose_name='Produto', on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField('Quantidade', default=1)
	price = models.DecimalField('Preço', decimal_places=2, max_digits=8)

	objects = CartItemManager()

	class Meta:
		verbose_name = 'Item do Carinho'
		verbose_name_plural = 'Itens dos Carrinhos'
		unique_together = (('cart_key', 'product'),)

	def __str__(self):
		return '{} [{}]'.format(self.product, self.quantity)



def post_save_cart_item(instance, **kwargs):
    if instance.quantity < 1:
        instance.delete()


models.signals.post_save.connect(
    post_save_cart_item, sender=CartItem, dispatch_uid='post_save_cart_item'
)