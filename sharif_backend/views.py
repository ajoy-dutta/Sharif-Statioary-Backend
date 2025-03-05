from django.http import HttpResponse

def home(request):
    return HttpResponse("Sharif Stationary & Papers")
