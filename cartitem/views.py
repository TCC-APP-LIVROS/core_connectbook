from django.shortcuts import render
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

        if client_id and announcement_id:
            try:
                announcement = Announcement.objects.get(pk=announcement_id)

                if quantity > announcement.quantity:
                    return JsonResponse({'error': 'Quantidade solicitada maior que o disponível'}, status=400)

                cart, created = Cart.objects.get_or_create(client=client_id)

                item_cart, created = Itemcart.objects.get_or_create(
                    cart=cart,
                    announcement=announcement,
                    defaults={'quantity': quantity}
                )

                if not created:
                    item_cart.quantity += quantity
                    item_cart.save()

                return JsonResponse({'message': 'Product added to cart'})
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
        client_id = data.get('client_id')
        announcement_id = data.get('announcement_id')
        quantity = data.get('quantity')

        if client_id and announcement_id:
            try:
                cart = Cart.objects.get(cliente=client_id)

                item_cart = Itemcart.objects.get(cart=cart, announcement_id=announcement_id)

                if quantity is not None:
                    item_cart.quantity = quantity

                item_cart.save()
                return JsonResponse({'message': 'Announcement updated successfully'})
            except Itemcart.DoesNotExist:
                return JsonResponse({'error': 'Item not found in cart'}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)


@csrf_exempt
def delete_item_cart(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        client_id = data.get('client_id')
        announcement_id = data.get('announcement_id')

        if client_id and announcement_id:
            try:
                cart = Cart.objects.get(cliente=client_id)

                item_cart = Itemcart.objects.get(cart=cart, announcement_id=announcement_id)

                item_cart.delete()
                return JsonResponse({'message': 'Item removed from cart'})
            except Itemcart.DoesNotExist:
                return JsonResponse({'error': 'Item not found in cart'}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
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
