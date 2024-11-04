from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ads.models import Announcement
from auths.models import UserAddress
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

