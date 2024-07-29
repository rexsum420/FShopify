from rest_framework import serializers
from .models import Store
from users.serializers import UserSerializer

class StoreSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Store
        fields = ['id', 'owner', 'name']
        
    def create(self, validated_data):
        store = super().create(validated_data)
        owner = store.owner
        if owner.role == 'customer':
            owner.role = 'store_owner'
            owner.save()
        return store
