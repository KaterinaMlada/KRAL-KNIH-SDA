from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request,"core/index.html")


def show_about(request):
    return render(request, 'stepi_template.html', {'name1':'Stepan Kubicek',
                                                   'name2': "Katerina Mlada"})
