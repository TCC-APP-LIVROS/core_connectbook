from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Cart
from ads.models import Announcement


@csrf_exempt
def add_car(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        client_id = data.get('client_id')
        product_id = data.get('product_id')

        if client_id and product_id:
            try:
                client = User.objects.get(pk=client_id)
                product = Announcement.objects.get(pk=product_id)

                cart = Cart.objects.create(
                    client=client,
                    product=product
                )

                return JsonResponse({'message': 'Added to cart'})
            except User.DoesNotExist:
                return JsonResponse({'error': 'User does not exist'}, status=400)
            except Announcement.DoesNotExist:
                return JsonResponse({'error': 'Announcement does not exist'}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

        else:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def edit_car(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        cart_id = data.get('cart_id')
        product_id = data.get('product_id')

        try:
            cart = Cart.objects.get(pk=cart_id)

            # Atualizar os campos, se fornecidos
            if product_id is not None:
                cart.product_id = product_id

            cart.save()
            return JsonResponse({'message': 'Cart updated successfully'})
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def car_detail(request, cart_id):
    if request.method == 'GET':
        try:
            if not cart_id:
                return JsonResponse({'error': 'Cart ID is required'}, status=400)

            cart = Cart.objects.get(pk=cart_id)

            cart_data = {
                'client': cart.client,
                'product': cart.product
            }

            return JsonResponse(cart_data)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

