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


