from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from orders.models import Order
from cartitem.models import Itemcart



@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_cart = data.get('item_cart')
        announcement = data.get('announcement')

        if item_cart:
            try:
                item = Itemcart.objects.get(pk=item_cart)

                order = Order.objects.create(
                    item_cart = item,
                    announcement = announcement
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

@csrf_exempt
def order_detail(request):
    if request.method == 'GET':
        orders = Order.objects.all().values()

        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)

        paginator = Paginator(orders, page_size)

        max_pages = 10
        total_pages = min(paginator.num_pages, max_pages)

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
