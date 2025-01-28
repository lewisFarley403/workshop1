



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
import json
from django.views.generic import TemplateView
from django.urls import path
# Assuming you have a model like this:
from .models import IndividualItem, ItemType, ShopingList,ItemType

class ListView(TemplateView):
    template_name = 'list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all ItemTypes and their related IndividualItems
        # context['item_types'] = IndividualItem.objects.all()
        context['individual_items'] = IndividualItem.objects.select_related('itemType').all()
        print(context)
        return context
@csrf_exempt
def add_item(request):
    if request.method == 'PUT':
        try:
            body = json.loads(request.body)
            item_type = body.get('itemType')
            expiration_date = body.get('expirationDate')
            amount = body.get('amount')

            if not item_type or not expiration_date or not amount:
                return JsonResponse({"error": "Missing required parameters."}, status=400)

            try:
                expiration_date = parse_date(expiration_date)
                if not expiration_date:
                    raise ValueError
            except ValueError:
                return JsonResponse({"error": "Invalid expirationDate format. Use YYYY-MM-DD."}, status=400)

            if not isinstance(amount, int) or amount <= 0:
                return JsonResponse({"error": "Amount must be a positive integer."}, status=400)

            IndividualItem.objects.create(
                item_type=item_type,
                expiration_date=expiration_date,
                amount=amount
            )

            return JsonResponse({"message": "Item added successfully."}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method. Use PUT."}, status=405)

@csrf_exempt
def remove_item(request):
    if request.method == 'DELETE':
        try:
            body = json.loads(request.body)
            item_id = body.get('ID')

            if not item_id:
                return JsonResponse({"error": "Missing required parameter: ID."}, status=400)

            try:
                item = IndividualItem.objects.get(id=item_id)
                item.delete()
                return JsonResponse({"message": "Item removed successfully."}, status=200)
            except IndividualItem.DoesNotExist:
                return JsonResponse({"error": "Item not found."}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method. Use DELETE."}, status=405)

@csrf_exempt
def remove_items(request):
    if request.method == 'DELETE':
        try:
            body = json.loads(request.body)
            ids = body.get('IDs')

            if not ids or not isinstance(ids, list):
                return JsonResponse({"error": "Missing or invalid parameter: IDs."}, status=400)

            deleted_count = IndividualItem.objects.filter(id__in=ids).delete()[0]
            return JsonResponse({"message": f"{deleted_count} items removed successfully."}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method. Use DELETE."}, status=405)

@csrf_exempt
def new_type(request):
    if request.method == 'PUT':
        try:
            body = json.loads(request.body)
            barcode = body.get('unique barcode')
            name = body.get('name')
            amount_type = body.get('amount type')

            if not barcode or not name or not amount_type:
                return JsonResponse({"error": "Missing required parameters."}, status=400)

            ItemType.objects.create(
                barcode=barcode,
                name=name,
                amount_type=amount_type
            )

            return JsonResponse({"message": "Item type added successfully."}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method. Use PUT."}, status=405)

@csrf_exempt
def remove_type(request):
    if request.method == 'DELETE':
        try:
            body = json.loads(request.body)
            barcode = body.get('unique barcode')

            if not barcode:
                return JsonResponse({"error": "Missing required parameter: unique barcode."}, status=400)

            if IndividualItem.objects.filter(item_type__barcode=barcode).exists():
                return JsonResponse({"error": "Cannot delete type while items of this type exist in the fridge."}, status=400)

            try:
                item_type = ItemType.objects.get(barcode=barcode)
                item_type.delete()
                return JsonResponse({"message": "Item type removed successfully."}, status=200)
            except ItemType.DoesNotExist:
                return JsonResponse({"error": "Item type not found."}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method. Use DELETE."}, status=405)

@csrf_exempt
def add_to_shopping_list(request):
    if request.method == 'PUT':
        try:
            body = json.loads(request.body)
            item_type = body.get('item type')
            amount = body.get('amount')

            if not item_type or not amount:
                return JsonResponse({"error": "Missing required parameters."}, status=400)

            if not isinstance(amount, int) or amount <= 0:
                return JsonResponse({"error": "Amount must be a positive integer."}, status=400)

            shopping_item, created = ShoppingList.objects.get_or_create(item_type=item_type)
            shopping_item.amount += amount
            shopping_item.save()

            return JsonResponse({"message": "Item added to shopping list successfully."}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method. Use PUT."}, status=405)

@csrf_exempt
def remove_from_shopping_list(request):
    if request.method == 'DELETE':
        try:
            body = json.loads(request.body)
            item_type = body.get('itemType')
            amount = body.get('amount')

            if not item_type or not amount:
                return JsonResponse({"error": "Missing required parameters."}, status=400)

            if not isinstance(amount, int) or amount <= 0:
                return JsonResponse({"error": "Amount must be a positive integer."}, status=400)

            try:
                shopping_item = ShoppingList.objects.get(item_type=item_type)
                shopping_item.amount -= amount

                if shopping_item.amount <= 0:
                    shopping_item.delete()
                else:
                    shopping_item.save()

                return JsonResponse({"message": "Item removed from shopping list successfully."}, status=200)
            except ShoppingList.DoesNotExist:
                return JsonResponse({"error": "Item not found in shopping list."}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method. Use DELETE."}, status=405)

@csrf_exempt
def purchase_item(request):
    if request.method == 'PATCH':
        try:
            body = json.loads(request.body)
            item_type = body.get('item type')
            amount = body.get('amount')
            expiration_date = body.get('expiration date')

            if not item_type or not amount or not expiration_date:
                return JsonResponse({"error": "Missing required parameters."}, status=400)

            try:
                expiration_date = parse_date(expiration_date)
                if not expiration_date:
                    raise ValueError
            except ValueError:
                return JsonResponse({"error": "Invalid expiration date format. Use YYYY-MM-DD."}, status=400)

            if not isinstance(amount, int) or amount <= 0:
                return JsonResponse({"error": "Amount must be a positive integer."}, status=400)

            try:
                shopping_item = ShoppingList.objects.get(item_type=item_type)
                shopping_item.amount -= amount

                if shopping_item.amount <= 0:
                    shopping_item.delete()
                else:
                    shopping_item.save()

                IndividualItem.objects.create(
                    item_type=item_type,
                    amount=amount,
                    expiration_date=expiration_date
                )

                return JsonResponse({"message": "Item purchased and added to fridge successfully."}, status=200)
            except ShoppingList.DoesNotExist:
                return JsonResponse({"error": "Item not found in shopping list."}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method. Use PATCH."}, status=405)



urlpatterns = [
    path('api/v1/addItem', add_item, name='add_item'),
    path('api/v1/removeItem', remove_item, name='remove_item'),
    path('api/v1/removeItems', remove_items, name='remove_items'),
    path('api/v1/newType', new_type, name='new_type'),
    path('api/v1/removeType', remove_type, name='remove_type'),
    path('api/v1/addToShoppingList', add_to_shopping_list, name='add_to_shopping_list'),
    path('api/v1/removeFromShoppingList', remove_from_shopping_list, name='remove_from_shopping_list'),
    path('api/v1/purchaseItem', purchase_item, name='purchase_item'),
]

