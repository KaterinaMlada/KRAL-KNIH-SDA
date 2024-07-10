from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import status
from .models import Book
from .serializers import BookSerializer


def home(request):
    return render(request,'home.html')


def show_about(request):
    return render(request, 'stepi_template.html', {'name1': 'Stepan Kubicek',
                                                   'name2': "Katerina Mlada"})


@api_view(['GET', 'POST'])
def book_list(request):
    if request.method == 'GET':
        queryset = Book.objects.select_related('category').all()
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data
        return Response('ok')


@api_view()
def book_detail(request, id):
    book = get_object_or_404(Book, pk=id)
    serializer = BookSerializer(book)
    return Response(serializer.data)
