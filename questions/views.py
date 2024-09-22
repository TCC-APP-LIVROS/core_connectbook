from django.shortcuts import render
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Question
from django.contrib.auth.models import User
from django.db import IntegrityError


@csrf_exempt
def list_questions(request):
    if request.method == 'GET':
        
        data = json.loads(request.body)
        announcement_id = data.get('announcement_id')
        page = data.get('page')
        
        questions = Question.objects.filter(announcement_id=announcement_id).values()
        itens_per_page = 5
        paginator = Paginator(questions, itens_per_page)
        
        return JsonResponse(list(paginator.get_page(page)), safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def create_question(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        question_client = data.get('question_client')
        announcement_id = data.get('announcement_id')
        client_id = data.get('client_id')

        if question_client and announcement_id and client_id:
            try:
                client = User.objects.get(pk=client_id)
                question = Question.objects.create(
                    question_client=question_client,
                    announcement_id=announcement_id,
                    client=client
                )
                return JsonResponse({'message': 'Question created successfully', 'id': question.id})
            except User.DoesNotExist:
                return JsonResponse({'error': 'Client does not exist'}, status=400)
            except IntegrityError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def reply_question(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        reply = data.get('reply')
        question_id = data.get('question_id')

        if question_id and reply:
            try:
                question = Question.objects.get(pk=question_id)
                if(question.reply):
                    return JsonResponse({'error': 'Question already replied'}, status=400)

                question.reply = reply
                
                question.save()

                return JsonResponse({'message': 'Question replied successfully', 'id': question.id})
            except IntegrityError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)