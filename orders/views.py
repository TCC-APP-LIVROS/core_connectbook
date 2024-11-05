from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ads.models import Announcement
from auths.models import Address, UserAddress
from orders.models import Order
from cartitem.models import Itemcart
from django.contrib.auth.models import User



@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        announcement = data.get('announcement')
        buyer = data.get('buyer')
        quantity = data.get('quantity')
        address = data.get('address')

        if announcement and buyer and quantity:
            try:
                buyer = User.objects.get(pk=buyer)
                announcement = Announcement.objects.get(pk=announcement)
                address = UserAddress.objects.get(pk=address)

                order = Order.objects.create(
                    buyer=buyer,
                    seller=announcement.seller,
                    announcement=announcement,
                    status='PENDING',
                    quantity=quantity,
                    address=address
                )

                return JsonResponse({'message': 'Order Create'})
            except Itemcart.DoesNotExist:
                return JsonResponse({'error': 'Item Cart does not exist'}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_order(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        order_id = data.get('order_id')

        try:
            if not order_id:
                return JsonResponse({'erro': 'Order ID is required'}, status=400)

            order = Order.objects.get(pk=Order)

            order.status = 'DELETED'

            order.save()

            return JsonResponse({'message': 'Order deleted successfully'})
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

# ADICIONAR QUERY STRING. QUERO FILTRAR POR COMPRADOR OU VENDEDOR
@csrf_exempt
def order_list(request, user_id, mode):
    if request.method == 'GET':

        if mode == "seller":
            orders = Order.objects.filter(seller_id=user_id).values()
        else:
            orders = Order.objects.filter(buyer_id=user_id).values()
        
        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)

        paginator = Paginator(orders, page_size)

        max_pages = 10
        total_pages = min(paginator.num_pages, max_pages)

        # for loop for every order
        for order in orders:
            try:
                announcement = Announcement.objects.filter(id=order['announcement_id']).values().first()
                order['announcement'] = announcement  # Now a dictionary
            except Announcement.DoesNotExist:
                order['announcement'] = None  # Handle case where announcement doesn't exist

        try:
            page_obj = paginator.page(page_number)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

        response_data = {
            'total_pages': total_pages,
            'current_page': page_obj.number,
            'orders': list(page_obj.object_list)
        }

        return JsonResponse(response_data, safe=False)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
def order_details(request, order_id, mode):
    if request.method == 'GET':
        print(order_id)
        order = Order.objects.filter(id=order_id).values().first()

        if order is None:
            return JsonResponse({'error': 'Order not found'}, status=404)

        if mode == "seller":
            user = User.objects.filter(pk=order['seller_id']).values().first()
        else:
            user = User.objects.filter(pk=order['buyer_id']).values().first()

        user_address = UserAddress.objects.filter(pk=order['address_id']).values().first()
        address = Address.objects.filter(pk=user_address['address_id']).values().first()

        if user is None:
            return JsonResponse({'error': 'User not found'}, status=404)
        user['password'] = '********'
        response_data = {
            'user': user,
            'order': order,
            'address': {
                'number': user_address['number'],
                'complement': user_address['complement'],
                'nickname': user_address['nickname'],
                'receiver_name': user_address['receiver_name'],
                'cep': address['cep'],
                'neighborhood': address['neighborhood'],
                'city': address['city'],
                'state': address['state'],
                'street': address['street'],
            }
        }

        return JsonResponse(response_data, safe=False)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def order_cancel(request, order_id, mode):
    if request.method == 'DELETE':
        order = Order.objects.get(pk=order_id)
        order.status = 'CANCELLED'
        order.save()
    
        return JsonResponse({'message': "OK"}, safe=False)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
