from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "landingPage/landingPage.html")

def informacion(request):
    return render(request, "landingPage/landingPage.html")

