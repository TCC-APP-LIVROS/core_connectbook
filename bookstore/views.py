from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
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
                user = User.objects.create_user(username=username, email=email, password=password)
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