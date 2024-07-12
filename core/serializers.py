from rest_framework import serializers
from core.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'unit_price', 'category']
    category = serializers.StringRelatedField()

