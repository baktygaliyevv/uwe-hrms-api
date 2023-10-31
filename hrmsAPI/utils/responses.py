from django.http import JsonResponse

def error(code=400, message=None):
    return JsonResponse({'status': 'Error', 'message': message}, status=code)

def ok(payload=None):
    return JsonResponse({'status': 'Ok', 'payload':payload}, status=200)
