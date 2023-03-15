from django.shortcuts import render


def urls_view(request):
    return render(request, 'urls.html')