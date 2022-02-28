from rest_framework import serializers 
from book_inventory.models import BookInventory
 
class BookInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = BookInventory
        fields =  '__all__'