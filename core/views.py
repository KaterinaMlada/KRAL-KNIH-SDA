from django.shortcuts import render




def books(request):
    context = {}
    return render(request,'books.html', context)

def cart(request):
    context = {}
    return render(request,'cart.html', context)


def checkout(request):
    context = {}
    return render(request,'checkout.html', context)


def show_about(request):
    return render(
        request,
        template_name='show_about.html',
        context={'names': ['Stepan Kubicek', 'Katerina Mlada']}
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

