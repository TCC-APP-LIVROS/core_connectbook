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
from .models import UserProfile, Address


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
        address = data.get('address')
        number = data.get('number')
        complement = data.get('complement')
        nickname = data.get('nickname')

        if address and number and nickname:
            try:
                new_address = Address.objects.create(address=address, number=number, complement=complement, nickname=nickname)
                return JsonResponse({'message': 'Address registered successfully'})
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