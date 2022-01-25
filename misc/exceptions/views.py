from django.http import JsonResponse


def custom_handler404(request, exception, *args, **kwargs):
    return JsonResponse({"message": "Not Found.", "detail": "Url does not exist"}, status=404)


def custom_handler500(request, *args, **kwargs):
    return JsonResponse({"message": "Something went wrong"}, status=500)