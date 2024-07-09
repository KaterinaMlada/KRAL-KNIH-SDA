from rest_framework import serializers

class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=100)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)