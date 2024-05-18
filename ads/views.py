from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Product, Announcement, Question


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
def create_announcement(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        study_area = data.get('study_area')
        condition = data.get('condition')
        price = data.get('price')
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
        status = data.get('status')
        remove_announcement = data.get('remove_announcement')

        try:
            announcement = Announcement.objects.get(pk=announcement_id)

            # Atualizar os campos, se fornecidos
            if title is not None:
                announcement.title = title
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