from bboard.models import UserProfile, Cart, Product, OrderLine
from bboard.services.services import get_userprofile


def add_to_cart(request):
    user = get_userprofile(request)

    try:
        cart = Cart.objects.get(id_customer=user)
    except:
        cart = Cart.objects.create(id_customer=user)
    product_id = request.POST['product_id']
    product = Product.objects.get(id=product_id)
    try:
        order_line = OrderLine.objects.filter(id_cart=cart, product=product).first()
        if order_line is not None:
            if product.amount > order_line.number_of_products + 1:
                OrderLine.objects.filter(id=order_line.id).update(number_of_products=order_line.number_of_products + 1, product_price=order_line.product_price + product.price)

        else:
            raise
    except:
        if product.amount > 0:
            OrderLine.objects.create(id_cart=cart, product=product, number_of_products=1, product_price=product.price)
