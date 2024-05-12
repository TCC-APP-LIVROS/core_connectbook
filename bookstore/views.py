from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from .models import UserProfile, Address, UserAddress, Product, Announcement, Question


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        print("Payload de entrada:", request.body.decode('utf-8'))
        if request.body:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if username and password:
                print(username, password)
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return JsonResponse({'message': 'Authenticated successfully'})
                    else:
                        return JsonResponse({'error': 'Disable My Job'}, status=403)
                else:
                    return JsonResponse({'error': 'Invalid login'}, status=401)
            else:
                print(username, password)
                return JsonResponse({f'error': f'Missing username {username} or password {password}'}, status=400)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def user_logout(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'message': 'Logged out successfully'})
        else:
            return JsonResponse({'error': 'User is not authenticated'}, status=401)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def profile_register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        last_name = data.get('last_name')
        password = data.get('password')
        email = data.get('email')
        phone = data.get('phone')
        photo = request.FILES.get('photo')

        # Verificar se o nome de usuário já existe
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        # Verificar se o e-mail já está cadastrado
        # if UserProfile.objects.filter(email=email).exists():
        #     return JsonResponse({'error': 'Email already registered'}, status=400)

        if username and password and email and phone:
            try:
                # Create user with username, email, and password
                user = User.objects.create_user(username=username, last_name=last_name, email=email, password=password)
                # Create profile
                profile = UserProfile.objects.create(user=user, email=email, phone=phone, photo=photo)
                return JsonResponse({'message': 'User and profile registered successfully'})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def address_register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cep = data.get('cep')

        if cep:
            try:
                # Consultar a API ViaCEP para obter detalhes do endereço
                via_cep_url = f'https://viacep.com.br/ws/{cep}/json/'
                response = requests.get(via_cep_url)
                if response.status_code == 200:
                    via_cep_data = response.json()
                    # Preencher automaticamente os campos de bairro, cidade e estado
                    neighborhood = via_cep_data.get('bairro', '')
                    city = via_cep_data.get('localidade', '')
                    state = via_cep_data.get('uf', '')

                    # Verificar se os campos essenciais estão presentes no payload
                    if 'public_place' in data:
                        public_place = data.get('public_place')
                    else:
                        return JsonResponse({'error': 'Missing public_place field'}, status=400)

                    if 'public_place_type' in data:
                        public_place_type = data.get('public_place_type')
                    else:
                        public_place_type = 'default_type'

                    # Criar o novo endereço com os dados fornecidos e preenchidos automaticamente
                    new_address = Address.objects.create(
                        cep=cep,
                        neighborhood=neighborhood,
                        public_place=public_place,
                        public_place_type=public_place_type,
                        city=city,
                        state=state
                    )
                    return JsonResponse({'message': 'Address registered successfully'})
                else:
                    return JsonResponse({'error': 'Failed to fetch address details from ViaCEP'}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'Missing cep field'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def user_address_register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        address_data = data.get('address')
        number = address_data.get('number')
        complement = address_data.get('complement')
        nickname = address_data.get('nickname')

        if user_id and address_data and complement and nickname:
            try:
                user = User.objects.get(pk=user_id)

                # Verificar se o CEP existe no banco de dados
                cep = address_data.get('cep')
                address = Address.objects.filter(cep=cep).first()
                if address is None:
                    # Caso o CEP não exista, criar o endereço do usuário
                    address = Address.objects.create(
                        cep=cep,
                        public_place=address_data.get('public_place'),
                        public_place_type=address_data.get('public_place_type'),
                        neighborhood='',  # Este campo será preenchido automaticamente com base no CEP
                        city='',           # Este campo será preenchido automaticamente com base no CEP
                        state=''           # Este campo será preenchido automaticamente com base no CEP
                    )

                # Vincular o endereço ao usuário
                user_address = UserAddress.objects.create(
                    user=user,
                    address=address,
                    number=number,
                    complement=complement,
                    nickname=nickname
                )

                return JsonResponse({'message': 'User address registered successfully'})
            except User.DoesNotExist:
                return JsonResponse({'error': 'User does not exist'}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



@csrf_exempt
@login_required
def edit_profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user  # Obtém o usuário atualmente logado

        # Atualiza as informações do usuário, se fornecidas no payload
        if 'phone' in data:
            user.userprofile.phone = data['phone']
        if 'address' in data:
            user.userprofile.address = data['address']
        if 'password' in data:
            user.set_password(data['password'])

        # Salva as alterações no usuário
        user.save()

        return JsonResponse({'message': 'Profile updated successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        # Gerar token para redefinição de senha
        token = default_token_generator.make_token(user)

        # Construir URL de redefinição de senha
        reset_url = request.build_absolute_uri(
            reverse('password_reset_confirm', kwargs={
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token
            })
        )

        # Renderizar o e-mail de redefinição de senha
        subject = 'Password Reset'
        message = render_to_string('password_reset_email.html', {
            'reset_url': reset_url
        })
        plain_message = strip_tags(message)

        # Enviar e-mail
        send_mail(subject, plain_message, 'your_email@example.com', [email], html_message=message)

        return JsonResponse({'message': 'Password reset email sent successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


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

