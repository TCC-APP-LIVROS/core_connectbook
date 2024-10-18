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
from .models import UserProfile, Address, UserAddress


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        print("Payload de entrada:", request.body.decode('utf-8'))
        if request.body:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if username and password:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        user_profile = UserProfile.objects.get(user=user)
                        response = {
                            'message': 'Authenticated successfully',
                            'id': user.id,
                            'profile_uuid': str(user_profile.uuid),
                            'photo': user_profile.photo.url if user_profile.photo else None,
                            'name': user.username,
                        }
                        return JsonResponse(response)
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

        if Address.objects.filter(cep=cep).exists():
            address_existing = Address.objects.get(cep=cep)
            address_data = {
                'cep': address_existing.cep,
                'neighborhood': address_existing.neighborhood,
                'city': address_existing.city,
                'state': address_existing.state
            }

            add_address = Address.objects.create(
                cep=cep,
                neighborhood=address_existing.neighborhood,
                city=address_existing.city,
                state=address_existing.state
            )
            return JsonResponse({'message': 'Address registered successfully'})
        else:
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

                        # Criar o novo endereço com os dados fornecidos e preenchidos automaticamente
                        new_address = Address.objects.create(
                            cep=cep,
                            neighborhood=neighborhood,
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

def get_Address_by_cep(cep):
    try:
        address_db = Address.objects.filter(cep=cep)
        if address_db.exists():
            return address_db.first()
        else:
            # Consultar a API ViaCEP para obter detalhes do endereço
            via_cep_url = f'https://viacep.com.br/ws/{cep}/json/'
            response = requests.get(via_cep_url)
            if response.status_code == 200:
                via_cep_data = response.json()

                # Preencher automaticamente os campos de bairro, cidade e estado
                neighborhood = via_cep_data.get('bairro', '')
                city = via_cep_data.get('localidade', '')
                state = via_cep_data.get('uf', '')
                street = via_cep_data.get('logradouro', '')
                
                # Criar o novo endereço com os dados fornecidos e preenchidos automaticamente
                new_address = {
                    'cep': cep,
                    'neighborhood': neighborhood,
                    'city': city,
                    'state': state,
                    'street': street,
                }

                #Se não existe, cria o endereço no DB
                address = Address.objects.create(
                        cep=new_address['cep'],
                        neighborhood=new_address['neighborhood'],
                        city=new_address['city'],
                        state=new_address['state'],
                        street=new_address['street']
                )
                return address
            else:
                return JsonResponse({'error': 'Failed to fetch address details from ViaCEP'}, status=400)
    except Exception as e:
                    print(e)
                    return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def user_address_register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        address_data = data.get('address')
        number = address_data.get('number')
        complement = address_data.get('complement')
        nickname = address_data.get('nickname')
        receiver_name = address_data.get('receiver_name')

        if user_id and address_data and complement and nickname:
            try:
                user = User.objects.get(pk=user_id)

                # Verificar se o CEP existe no banco de dados
                cep = address_data.get('cep')
                address = get_Address_by_cep(cep)
                
                # Vincular o endereço ao usuário
                UserAddress.objects.create(
                    user=user,
                    address=address,
                    number=number,
                    complement=complement,
                    nickname=nickname,
                    receiver_name=receiver_name,
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
def user_address_update(request, id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        cep = data.get('cep')

        number = data.get('number')
        complement = data.get('complement')
        nickname = data.get('nickname')
        receiver_name = data.get('receiver_name')

        if number and nickname and receiver_name:
            
            try:

                # Verificar se o CEP existe no banco de dados
                address = get_Address_by_cep(cep)
                user_address = UserAddress.objects.get(pk=id)

                user_address.number = number
                user_address.complement = complement
                user_address.nickname = nickname
                user_address.receiver_name = receiver_name
                user_address.address = address
                
                # Preciso dar um update no endereço
                user_address.save()

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
def user_address_delete(request, id):
    print("Entrou no delete")
    if request.method == 'DELETE':
        if not id:
            return JsonResponse({'error': 'id is required'}, status=400)

        try:
            user_address = UserAddress.objects.get(pk=id)
            user_address.delete()

            return JsonResponse({'message': 'User address deleted successfully'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def user_address_list(request,user_id):
    if request.method == 'GET':
        if not user_id:
                return JsonResponse({'error': 'user_id is required'}, status=400)

        user_addresses  = UserAddress.objects.filter(user_id=user_id).values()

        items_data = []
        for item in user_addresses:
            address = Address.objects.get(pk=item['address_id'])
            items_data.append({
                'id': item['id'],
                'cep': address.cep,
                'neighborhood': address.neighborhood,
                'city': address.city,
                'state': address.state,
                'street': address.street,
                'number': item['number'],
                'complement': item['complement'],
                'nickname': item['nickname'],
                'receiver_name': item['receiver_name']
            })
        print(items_data)
            
        return JsonResponse({'addresses' : items_data})
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
def list_auths(request):
    if request.method == 'GET':
        user = User.objects.all().values()
        return JsonResponse(list(user), safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)