from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View

from .models import Book

def home(request):
    return render(request,'home.html')


def show_about(request):
    return render(
        request,
        template_name='stepi_template.html',
        context={'names': ['Stepan Kubicek', 'Katerina Mlada']}
    )


class BooksView(View):
    def get(self, request):
        return render(
            request,
            template_name='books.html',
            context={'books': Book.objects.all()}
        )
#dole pokus o API, asi necháme pro Krále Knih 2.0 :D
"""
@api_view(['GET', 'POST'])
def book_list(request):
    if request.method == 'GET':
        queryset = Book.objects.select_related('category').all()
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('ok')


@api_view()
def book_detail(request, id):
    book = get_object_or_404(Book, pk=id)
    serializer = BookSerializer(book)
    return Response(serializer.data)
"""

