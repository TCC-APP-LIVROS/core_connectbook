from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Review
from django.contrib.auth.models import User
from django.db import IntegrityError


@csrf_exempt
def list_reviews(request):
    if request.method == 'GET':
        reviews = Review.objects.all().values()
        return JsonResponse(list(reviews), safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def create_review(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        rating = data.get('rating')
        comment = data.get('comment')
        announcement_id = data.get('announcement_id')
        customer_id = data.get('customer_id')

        if rating is not None and comment and announcement_id and customer_id:
            try:
                customer = User.objects.get(pk=customer_id)
                review, created = Review.objects.get_or_create(
                    customer=customer,
                    announcement_id=announcement_id,
                    defaults={'rating': rating, 'comment': comment}
                )
                if created:
                    return JsonResponse({'message': 'Review created successfully', 'id': review.id})
                else:
                    return JsonResponse({'error': 'Review already exists for this user and announcement'}, status=400)
            except User.DoesNotExist:
                return JsonResponse({'error': 'Customer does not exist'}, status=400)
            except IntegrityError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def delete_review(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        review_id = data.get('review_id')

        try:
            if not review_id:
                return JsonResponse({'erro': 'Review ID is required'}, status=400)

            review = Review.objects.get(pk=review_id)

            review.delete()

            return JsonResponse({'message': 'Review deleted successfully'})
        except Review.DoesNotExist:
            return JsonResponse({'error': 'Review does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)