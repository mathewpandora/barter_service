from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def info_page(request):
    print("тут")
    return render(request, 'info/info.html')
