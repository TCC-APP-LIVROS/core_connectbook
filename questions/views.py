from django.shortcuts import render
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
        questions = Question.objects.all().values()
        return JsonResponse(list(questions), safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def create_question(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        question_client = data.get('question_client')
        reply = data.get('reply')
        announcement_id = data.get('announcement_id')
        client_id = data.get('client_id')

        if question_client and reply and announcement_id and client_id:
            try:
                client = User.objects.get(pk=client_id)
                question = Question.objects.create(
                    question_client=question_client,
                    reply=reply,
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
def delete_question(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        question_id = data.get('question_id')

        try:
            if not question_id:
                return JsonResponse({'erro': 'Question ID is required'}, status=400)

            question = Question.objects.get(pk=question_id)

            question.delete()

            return JsonResponse({'message': 'Question deleted successfully'})
        except Question.DoesNotExist:
            return JsonResponse({'error': 'Question does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)