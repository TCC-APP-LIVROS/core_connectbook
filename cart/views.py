from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Cart
from django.contrib.auth.models import User


@csrf_exempt
def car_detail(request, client_id):
    if request.method == 'GET':
        try:
            cart = Cart.objects.get(client=client_id)
            items = cart.itemcart_set.all()

            cart_data = []

            for item in items:
                cart_data.append({
                    'product': item.announcement.product,
                    'quantity': item.quantity,
                })
            return JsonResponse({'cart': cart_data})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def delete_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        client_id = data.get('client_id')

        if client_id:
            try:
                cart = Cart.objects.get(client=client_id)

                cart.itemcart_set.all().delete()

                return JsonResponse({'message': 'Cart successfully cleaned'})
            except Cart.DoesNotExist:
                return JsonResponse({'error': 'Carrinho não encontrado'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'User not found'}, status=404)
    else:
        return JsonResponse({'error': 'Cart not found'}, status=405)
