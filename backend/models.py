from django.db import models

class ItemType(models.Model):
    barcode = models.CharField(max_length=50,primary_key=True)
    name = models.CharField(max_length=50)
    accountType = models.ForeignKey('AccountType', on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class AccountType(models.Model):
    name = models.CharField(max_length=50,primary_key=True)

    def __str__(self):
        return self.name
    
class IndividualItem(models.Model):
    expirationDate = models.DateField()
    itemType = models.ForeignKey('ItemType', on_delete=models.CASCADE)
    amount = models.IntegerField()
    def __str__(self):
        return self.barcode
class ShopingList(models.Model):
    itemType = models.ForeignKey('ItemType', on_delete=models.CASCADE,primary_key=True)
    amount = models.IntegerField()
    def __str__(self):
        return self.name