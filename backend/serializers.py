from rest_framework import serializers
from .models import ItemType, AccountType, IndividualItem, ShopingList

# Serializer for AccountType model
class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = ['name']

# Serializer for ItemType model
class ItemTypeSerializer(serializers.ModelSerializer):
    accountType = AccountTypeSerializer()  # Nested serializer for AccountType

    class Meta:
        model = ItemType
        fields = ['barcode', 'name', 'accountType']

# Serializer for IndividualItem model
class IndividualItemSerializer(serializers.ModelSerializer):
    itemType = ItemTypeSerializer()  # Nested serializer for ItemType

    class Meta:
        model = IndividualItem
        fields = ['expirationDate', 'itemType', 'amount']

# Serializer for ShopingList model
class ShopingListSerializer(serializers.ModelSerializer):
    itemType = ItemTypeSerializer()  # Nested serializer for ItemType

    class Meta:
        model = ShopingList
        fields = ['itemType', 'amount']