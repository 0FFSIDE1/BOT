# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .tasks import process_update_task
import json

@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        
        # Send the update to the Celery task
        process_update_task.delay(data)
        
        return JsonResponse({"status": "ok"})
    return JsonResponse({"error": "Invalid request"}, status=400)
