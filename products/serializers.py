from rest_framework import serializers
from .models import Product, Category, Tag
from store.serializers import StoreSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    store = StoreSerializer(read_only=True)
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'store', 'description', 'price', 'stock', 'category', 'tags', 'created_at']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        category_data = validated_data.pop('category')
        category, created = Category.objects.get_or_create(**category_data)
        product = Product.objects.create(category=category, **validated_data)
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            product.tags.add(tag)
        return product

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags')
        category_data = validated_data.pop('category')
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.category, created = Category.objects.get_or_create(**category_data)
        
        instance.tags.clear()
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            instance.tags.add(tag)
        
        instance.save()
        return instance
