import re
from django.shortcuts import render
from django.conf import settings
import boto3
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
import json

from django.views.decorators.http import condition

from auths.models import UserProfile

from .models import Product, Announcement

@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        study_area = request.POST.get('study_area')
        published_at = request.POST.get('published_at')
        author = request.POST.get('author')
        image = request.FILES.get('image')
        seller_id = request.POST.get('seller_id')  # Supondo que o ID do vendedor seja enviado no corpo da requisição
        print(image)
        if name and author and seller_id:
            try:
                # Obter o usuário vendedor com base no ID fornecido
                seller = User.objects.get(pk=seller_id)

                photo = UploadImageView(image)
                print(photo)

                # Criar o produto
                product = Product.objects.create(
                    name=name,
                    study_area=study_area,
                    published_at=published_at,
                    author=author,
                    image=photo,
                    seller=seller
                )

                return product
            except User.DoesNotExist:
                return JsonResponse({'error': 'Seller does not exist'}, status=400)
            except Exception as e:
                print(e)
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
                'image': product.image.url,
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
    title = request.get('title')
    description = request.get('description')
    condition = request.get('condition')
    price = request.get('price')
    quantity = request.get('quantity')
    product_id = request.get('product_id')
    seller_id = request.get('seller_id')
    status = request.get('status', 'activated')

    if title and condition and price and product_id and seller_id:
        try:
            # Verificar se o produto e o vendedor existem
            product = Product.objects.get(pk=product_id)
            seller = User.objects.get(pk=seller_id)

            # Criar o anúncio
            announcement = Announcement.objects.create(
                title=title,
                description=description,
                condition=condition,
                price=price,
                product=product,
                seller=seller,
                status=status,
                quantity=quantity
            )

            return announcement  # Retorna o objeto de anúncio criado
        except Product.DoesNotExist:
            print("Product does not exist")
            return None  # Retorna None em vez de JsonResponse
        except User.DoesNotExist:
            print("Seller does not exist")
            return None
        except Exception as e:
            print(f"Error creating announcement: {str(e)}")
            return None
    else:
        print("Missing required fields")
        return None
    
@csrf_exempt
def create_announcement_total(request):
    if request.method == 'POST':
        try:
            
            # Criação do produto
            product = create_product(request)
            
            # Dados da requisição
            post_data = request.POST.copy()
            post_data['product_id'] = product.id  # Atribuir o ID do produto criado

            # Criação do anúncioprint
            announcement = create_announcement(post_data)
            
            if product and announcement:
                return JsonResponse({'message': 'Announcement created successfully'})
            else:
                return JsonResponse({'error': 'Failed to create announcement'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def edit_announcement(request, announcement_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        title = data.get('title')
        description = data.get('description')
        price = data.get('price')
        quantity = data.get('quantity')
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
def delete_announcement(request, announcement_id):
    if request.method == 'DELETE':

        try:
            if not announcement_id:
                return JsonResponse({'erro': 'Announcement ID is required'}, status=400)

            announcement = Announcement.objects.get(pk=announcement_id)
            print(announcement.product_id)
            product = Product.objects.get(pk=announcement.product_id)

            announcement.delete()
            
            deleteImage(product.image)
            product.delete()

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
            seller = User.objects.get(pk=announcement.seller_id)
            seller_profile = UserProfile.objects.get(user_id=announcement.seller_id)
            product = Product.objects.get(pk=announcement.product_id)
            
            announcement_data = {
                'id': announcement_id,
                'title': announcement.title,
                'description': announcement.description,
                'condition': announcement.condition,
                'price': announcement.price,
                'quantity': announcement.quantity,
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'study_area': product.study_area,
                    'published_at': product.published_at,
                    'author': product.author,
                    'image': product.image
                },
                'seller': {
                    'username': seller.username,
                    'first_name': seller.first_name,
                    'last_name': seller.last_name,
                    'id': seller.id
                },
                'seller_profile': {
                    'photo': seller_profile.photo,
                },
                'status': announcement.status
            }

            return JsonResponse(announcement_data)
        except Announcement.DoesNotExist:
            return JsonResponse({'error': 'Announcement does not exist'}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def list_announcement(request, page):
    if request.method == 'GET':
        try:
            if not page:
                    return JsonResponse({'error': 'Page is required'}, status=400)
            
            user_id = request.GET.get('user')
            show_user = request.GET.get('show_user')
            itens_per_page = 10 # passar na req.

            if str(show_user).lower() == 'false':
                announcement = Announcement.objects.exclude(seller_id=user_id).values()
            else:
                announcement = Announcement.objects.filter(seller_id=user_id).values()
            
             # Serializa os dados do vendedor para cada anúncio
            announcement_list = []
            for a in announcement:
                seller = User.objects.get(pk=a['seller_id'])
                seller_profile = UserProfile.objects.get(user_id=a['seller_id'])
                product = Product.objects.get(pk=a['product_id'])
                print(product)
                a['seller'] = {
                    'username': seller.username,
                    'first_name': seller.first_name,
                    'last_name': seller.last_name
                }
                a['seller_profile'] = {
                    'photo': seller_profile.photo,
                }
                a['product_image'] = product.image
                announcement_list.append(a)

            paginator = Paginator(announcement, itens_per_page)
            
            return JsonResponse(list(paginator.get_page(page)), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=400)
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

@csrf_exempt
def announcement_toggle_status(request, announcement_id):
    if request.method == 'PUT':
        try:
            if not announcement_id:
                return JsonResponse({'error': 'Announcement ID is required'}, status=400)

            announcement = Announcement.objects.get(pk=announcement_id)
            
            if announcement.status == 'disabled':
                announcement.status = 'activated'
            else:
                announcement.status = 'disabled'
            
            announcement.save()

            return JsonResponse({'message': 'Announcement {announcement.status} successfully'})
        except Announcement.DoesNotExist:
            return JsonResponse({'error': 'Announcement does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    
def UploadImageView(image):
        print(image)
        if not image:
            return JsonResponse({"error": "Imagem não fornecida"}, status=400)

        # Inicializa o cliente S3 usando boto3
        s3 = boto3.client(
            "s3",
            aws_access_key_id='',
            aws_secret_access_key='',
            region_name='sa-east-1',
        )

        # Nome do arquivo no S3
        s3_filename = f"uploads/{image.name}"

        try:
            # Upload da imagem para o S3
            s3.upload_fileobj(
                image,
                '',
                s3_filename,
                ExtraArgs={'ACL':'public-read'}
            )

            # URL público da imagem no S3
            image_url = f"/{s3_filename}"
            print(image_url)

            return image_url

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

def deleteImage(imageUri):
        if not imageUri:
            return JsonResponse({"error": "Imagem não fornecida"}, status=400)

        # Inicializa o cliente S3 usando boto3
        s3 = boto3.client(
            "s3",
            aws_access_key_id='',
            aws_secret_access_key='',
            region_name='sa-east-1',
        )

        try:
            s3.delete_object(Bucket='', Key="uploads/" + extract_after_uploads(imageUri))

            return True

        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)}, status=500)
        

def extract_after_uploads(url):
    # Usando uma expressão regular para capturar tudo após 'uploads/'
    match = re.search(r'uploads/(.*)', url)
    if match:
        return match.group(1)
    else:
        return None