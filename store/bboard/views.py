from django.shortcuts import render

# Create your views here.

def bboard(requiest):
    return render(requiest,'bboard/basis/index.html')

