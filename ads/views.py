from django.shortcuts import render
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
        description = data.get('description')
        study_area = data.get('study_area')
        condition = data.get('condition')
        price = data.get('price')
        product_id = data.get('product_id')
        seller = data.get('seller_id')
        status = data.get('status', 'disable')

        if title and study_area and condition and price and product_id:
            try:
                # Verificar se o produto associado existe
                product = Product.objects.get(pk=product_id)

                # Criar o anúncio
                announcement = Announcement.objects.create(
                    title=title,
                    description=description,
                    study_area=study_area,
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
        remove_announcement = data.get('remove_announcement')

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

            # Remover o anúncio, se solicitado
            if remove_announcement:
                announcement.delete()
                return JsonResponse({'message': 'Announcement removed successfully'})

            announcement.save()
            return JsonResponse({'message': 'Announcement updated successfully'})
        except Announcement.DoesNotExist:
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
                'description': announcement.description,
                'study_area': announcement.study_area,
                'condition': announcement.condition,
                'price': announcement.price,
                'product_id': announcement.product_id,
                'seller_id': announcement.seller_id,
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
