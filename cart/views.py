from itertools import product
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Cart
from django.contrib.auth.models import User


@csrf_exempt
def add_car(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        client_id = data.get('client_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        if client_id and product_id:
            try:
                # Verifica se o cliente e o produto existem
                client = User.objects.get(pk=client_id)
                product = Product.objects.get(pk=product_id)

                # Verifica se o produto já está no carrinho
                cart = Cart.objects.filter(client=client).first()
                if not cart:
                    cart = Cart.objects.create(client=client)

                existing_item = Itemcart.objects.filter(cart=cart, product=product).first()

                if existing_item:
                    # Atualiza a quantidade se o item já estiver no carrinho
                    existing_item.quantity = quantity
                    existing_item.save()
                else:
                    # Adiciona o novo item ao carrinho se não estiver presente
                    cart_item = Itemcart.objects.create(cart=cart, product=product, quantity=quantity)
                    cart_item.save()

                return JsonResponse({'message': 'Added to cart'})

            except User.DoesNotExist:
                return JsonResponse({'error': 'User does not exist'}, status=400)
            except Product.DoesNotExist:
                return JsonResponse({'error': 'Product does not exist'}, status=400)
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
            
            print(cart_id)
            
            # Get the Cart object directly without using .values()
            cart = Cart.objects.get(client_id=cart_id)
            print(cart)

            # Get the items related to this cart
            items = Itemcart.objects.filter(cart_id=cart.id)
            items_data = []

            for item in items:
                product = Product.objects.get(pk=item.product_id)
                announcement = Announcement.objects.get(product=product)
                items_data.append({
                    'announcemente_id': announcement.id,
                    'title': product.name,
                    'price': announcement.price,
                    'quantity': item.quantity,
                    'max_quantity': announcement.quantity,
                    'image': product.image
                })

            # Create the response data
            cart_data = {
                'items': items_data
            }

            return JsonResponse(cart_data)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart does not exist'}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

