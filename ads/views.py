from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.views.decorators.http import condition

from .models import Product, Announcement
from questions.models import Question

@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        description = data.get('description')
        author = data.get('author')
        image = request.FILES.get('image')
        seller_id = data.get('seller_id')  # Supondo que o ID do vendedor seja enviado no corpo da requisição

        if name and author and seller_id:
            try:
                # Obter o usuário vendedor com base no ID fornecido
                seller = User.objects.get(pk=seller_id)

                # Criar o produto
                product = Product.objects.create(
                    name=name,
                    description=description,
                    author=author,
                    image=image,
                    seller=seller
                )

                return JsonResponse({'message': 'Product created successfully'})
            except User.DoesNotExist:
                return JsonResponse({'error': 'Seller does not exist'}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def edit_product(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        name = data.get('name')
        description = data.get('description')
        author = data.get('author')
        image = request.FILES.get('image')

        try:
            if not product_id:
                return JsonResponse({'error': 'Product ID is required'}, status=400)

            product = Product.objects.get(pk=product_id)

            if name is not None:
                product.name = name
            if description is not None:
                product.description = description
            if author is not None:
                product.author = author
            if image is not None:
                product.image = image

            product.save()

            return JsonResponse({'message': 'Product update successfully'})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_product(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        product_id = data.get('product_id')

        try:
            if not product_id:
                return JsonResponse({'erro': 'Product ID is required'}, status=400)

            product = Product.objects.get(pk=product_id)

            product.delete()

            return JsonResponse({'message': 'Product deleted successfully'})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def product_detail(request, product_id):
    if request.method == 'GET':
        try:
            if not product_id:
                return JsonResponse({'error': 'Product ID is required'}, status=400)

            product = Product.objects.get(pk=product_id)

            product_data = {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'author': product.author,
                'image': product.image.url if product.image else None,
            }

            return JsonResponse(product_data)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def list_product(request):
    if request.method == 'GET':
        product = Product.objects.all().values()
        return JsonResponse(list(product), safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def create_announcement(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        study_area = data.get('study_area')
        condition = data.get('condition')
        price = data.get('price')
        quantity = data.get('quantity')
        product_id = data.get('product_id')
        question_id = data.get('question_id')
        status = data.get('status', 'disable')

        if title and study_area and condition and price and product_id:
            try:
                # Verificar se o produto associado existe
                product = Product.objects.get(pk=product_id)

                # Verificar se a questão associada existe, se houver
                question = None
                if question_id:
                    question = Question.objects.get(pk=question_id)

                # Criar o anúncio
                announcement = Announcement.objects.create(
                    title=title,
                    study_area=study_area,
                    condition=condition,
                    price=price,
                    quantity=quantity,
                    product=product,
                    question=question,
                    status=status
                )

                return JsonResponse({'message': 'Announcement created successfully'})
            except Product.DoesNotExist:
                return JsonResponse({'error': 'Product does not exist'}, status=400)
            except Question.DoesNotExist:
                return JsonResponse({'error': 'Question does not exist'}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def edit_announcement(request, announcement_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        title = data.get('title')
        price = data.get('price')
        quantity = data.get('quantity')
        status = data.get('status')

        try:
            announcement = Announcement.objects.get(pk=announcement_id)

            # Atualizar os campos, se fornecidos
            if title is not None:
                announcement.title = title
            if price is not None:
                announcement.price = price
            if quantity is not None:
                announcement.quantity = quantity
            if status is not None:
                announcement.status = status

            announcement.save()
            return JsonResponse({'message': 'Announcement updated successfully'})
        except Announcement.DoesNotExist:
            return JsonResponse({'error': 'Announcement does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_announcement(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        announcement_id = data.get('announcement_id')

        try:
            if not announcement_id:
                return JsonResponse({'erro': 'Announcement ID is required'}, status=400)

            announcement = Announcement.objects.get(pk=announcement_id)

            announcement.delete()

            return JsonResponse({'message': 'Announcement deleted successfully'})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Announcement does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



@csrf_exempt
def announcement_detail(request, announcement_id):
    if request.method == 'GET':
        try:
            if not announcement_id:
                return JsonResponse({'error': 'Announcement ID is required'}, status=400)

            announcement = Product.objects.get(pk=announcement_id)

            announcement_data = {
                'id': announcement_id,
                'title': announcement.title,
                'study_area': announcement.study_area,
                'condition': announcement.condition,
                'price': announcement.price,
                'quantity': announcement.quantity,
                'product_id': announcement.product_id,
                'question_id': announcement.question_id,
                'status': announcement.status
            }

            return JsonResponse(announcement_data)
        except Announcement.DoesNotExist:
            return JsonResponse({'error': 'Announcement does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def list_announcement(request):
    if request.method == 'GET':
        announcement = Announcement.objects.all().values()
        return JsonResponse(list(announcement), safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def search_annoucement(request):
    if request.method == 'GET':
        data = json.loads(request.body)
        title = data.get('title')
        study_area = data.get('study_area')
        condition = data.get('condition')

        try:
            if title:
                announcements = Announcement.objects.filter(title=title)
            if study_area:
                announcements = Announcement.objects.filter(study_area=study_area)
            if condition:
                announcements = Announcement.objects.filter(condition=condition)

            if announcements.exists():
                announcement_data = [{
                    'id': announcements.id,
                    'title': announcements.title,
                    'study_area': announcements.study_area,
                    'condition': announcements.condition,
                    'price': announcements.price,
                    'quantity': announcements.quantity,
                    'product_id': announcements.product_id,
                    'question_id': announcements.question_id,
                    'status': announcements.status
                } for announcement in announcements]

                return JsonResponse({'annoucement': announcement_data})
            else:
                return JsonResponse({'message': 'No annoucements found'}, status=404)
        except Announcement.DoesNotExist:
            return JsonResponse({'error': 'Announcement does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
