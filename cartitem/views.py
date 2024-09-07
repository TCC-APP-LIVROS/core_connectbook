from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Itemcart
from cart.models import Cart
from ads.models import Announcement


@csrf_exempt
def add_item_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cart_id = data.get('cart_id')
        product_id = data.get('product_id')

        if cart_id and product_id:
            try:
                cart = Cart.objects.get(pk=cart_id)
                product = Announcement.objects.get(pk=product_id)

                item_cart = Itemcart.objects.create(
                    cart=cart,
                    product=product
                )

                return JsonResponse({'message': 'Item added to cart'})
            except Cart.DoesNotExist:
                return JsonResponse({'error': 'Cart does not exist'}, status=400)
            except Announcement.DoesNotExist:
                return JsonResponse({'error': 'Announcement does not exist'}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

        else:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)