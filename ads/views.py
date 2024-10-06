from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Product, Announcement

@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        study_area = data.get('study_area')
        published_at = data.get('published_at')
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
                    study_area=study_area,
                    published_at=published_at,
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
        study_area = data.get('study_area')
        published_at = data.get('published_at')
        author = data.get('author')
        image = request.FILES.get('image')

        try:
            if not product_id:
                return JsonResponse({'error': 'Product ID is required'}, status=400)

            product = Product.objects.get(pk=product_id)

            if name is not None:
                product.name = name
            if study_area is not None:
                product.study_area = study_area
            if published_at is not None:
                product.published_at = published_at
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
                'study_area': product.study_area,
                'published_at': product.published_at,
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
def list_product(request, page):
    if request.method == 'GET':

        if not page:
                return JsonResponse({'error': 'Page is required'}, status=400)

        product = Product.objects.all().values()
        itens_per_page = 10
        paginator = Paginator(product, itens_per_page)

        return JsonResponse(list(paginator.get_page(page)), safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def create_announcement(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        description = data.get('description')
        condition = data.get('condition')
        price = data.get('price')
        product_id = data.get('product_id')
        seller = data.get('seller_id')
        status = data.get('status', 'disable')

        if title and condition and price and product_id:
            try:
                # Verificar se o produto associado existe
                product = Product.objects.get(pk=product_id)
                seller = User.objects.get(pk=seller)

                # Criar o anúncio
                announcement = Announcement.objects.create(
                    title=title,
                    description=description,
                    condition=condition,
                    price=price,
                    product=product,
                    seller=seller,
                    status=status
                )

                return JsonResponse({'message': 'Announcement created successfully'})
            except Product.DoesNotExist:
                return JsonResponse({'error': 'Product does not exist'}, status=400)
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
        description = data.get('description')
        price = data.get('price')
        status = data.get('status')

        try:
            announcement = Announcement.objects.get(pk=announcement_id)

            # Atualizar os campos, se fornecidos
            if title is not None:
                announcement.title = title
            if description is not None:
                announcement.description = description
            if price is not None:
                announcement.price = price
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

            announcement = Announcement.objects.get(pk=announcement_id)
            print(announcement)
            announcement_data = {
                'id': announcement_id,
                'title': announcement.title,
                'description': announcement.description,
                'condition': announcement.condition,
                'price': announcement.price,
                'product': {
                    'id': announcement.product.id,
                    'name': announcement.product.name,
                    'study_area': announcement.product.study_area,
                    'published_at': announcement.product.published_at,
                    'author': announcement.product.author,
                    'image': announcement.product.image.url if announcement.product.image else None,
                },
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
def list_announcement(request, page):
    if request.method == 'GET':
        if not page:
                return JsonResponse({'error': 'Page is required'}, status=400)

        announcement = Announcement.objects.all().values()
        itens_per_page = 10
        paginator = Paginator(announcement, itens_per_page)
        
        return JsonResponse(list(paginator.get_page(page)), safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def search_annoucement(request):
    if request.method == 'GET':
        data = json.loads(request.body)
        title = data.get('title')

        try:
            if title:
                announcements = Announcement.objects.filter(title=title)

            if announcements.exists():
                announcement_data = [{
                    'id': announcements.id,
                    'title': announcements.title,
                    'study_area': announcements.study_area,
                    'condition': announcements.condition,
                    'price': announcements.price,
                    'product_id': announcements.product_id,
                    'question_id': announcements.question_id,
                    'status': announcements.status
                } for announcement in announcements]

                return JsonResponse({'annoucement': announcement_data})
        except Announcement.DoesNotExist:
            return JsonResponse({'error': 'Announcement does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def announcement_toggle_status(request, announcement_id):
    if request.method == 'PUT':
        try:
            if not announcement_id:
                return JsonResponse({'error': 'Announcement ID is required'}, status=400)

            announcement = Announcement.objects.get(pk=announcement_id)
            
            if announcement.status == 'disable':
                announcement.status = 'activated'
            else:
                announcement.status = 'disable'
            
            announcement.save()

            return JsonResponse({'message': 'Announcement {announcement.status} successfully'})
        except Announcement.DoesNotExist:
            return JsonResponse({'error': 'Announcement does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

