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
        print(data)
        client_id = data.get('client_id')
        announcement_id = data.get('announcement_id')
        quantity = data.get('quantity', 1)

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


@csrf_exempt
def edit_item_cart(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        item_cart_id = data.get('item_cart_id')
        cart_id = data.get('cart_id')
        product_id = data.get('product_id')

        try:
            item_cart = Itemcart.objects.get(pk=item_cart_id)

            # Atualizar os campos, se fornecidos
            if cart_id is not None:
                item_cart.cart_id = cart_id
            if product_id is not None:
                item_cart.product_id = product_id

            item_cart.save()
            return JsonResponse({'message': 'Item Cart updated successfully'})
        except Itemcart.DoesNotExist:
            return JsonResponse({'error': 'Item Cart does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def delete_item_cart(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        item_cart_id = data.get('item_cart_id')

        try:
            if not item_cart_id:
                return JsonResponse({'erro': 'Item Cart ID is required'}, status=400)

            item_cart = Itemcart.objects.get(pk=item_cart_id)

            item_cart.delete()

            return JsonResponse({'message': 'Item Cart deleted successfully'})
        except Itemcart.DoesNotExist:
            return JsonResponse({'error': 'Item Cart does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



@csrf_exempt
def item_cart_detail(request, id):
    if request.method == 'GET':
        try:
            if not id:
                return JsonResponse({'error': 'Item Cart ID is required'}, status=400)

            cart = Cart.objects.get(client_id=id)
            print(cart)
            item_cart = Itemcart.objects.get(cart=cart.id)

            item_cart_data = {
                'cart': item_cart.client,
                'product': item_cart.product
            }

            return JsonResponse(item_cart_data)
        except Itemcart.DoesNotExist:
            return JsonResponse({'error': 'Item Cart does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



@csrf_exempt
def item_cart_detail(request, id):
    if request.method == 'GET':
        try:
            if not id:
                return JsonResponse({'error': 'Item Cart ID is required'}, status=400)

            cart = Cart.objects.get(client_id=id)
            print(cart)
            item_cart = Itemcart.objects.get(cart=cart.id)

            item_cart_data = {
                'cart': item_cart.client,
                'product': item_cart.product
            }

            return JsonResponse(item_cart_data)
        except Itemcart.DoesNotExist:
            return JsonResponse({'error': 'Item Cart does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
