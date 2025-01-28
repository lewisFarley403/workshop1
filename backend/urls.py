"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path,include


from django.conf import settings
from django.conf.urls.static import static

from apis.views import add_item, remove_item, remove_items, new_type, remove_type, add_to_shopping_list, remove_from_shopping_list, purchase_item, grid_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('gridView', grid_view, name='grid_view'),
    path('addItem', add_item, name='add_item'),
    path('removeItem', remove_item, name='remove_item'),
    path('removeItems', remove_items, name='remove_items'),
    path('newType', new_type, name='new_type'),
    path('removeType', remove_type, name='remove_type'),
    path('addToShoppingList', add_to_shopping_list, name='add_to_shopping_list'),
    path('removeFromShoppingList', remove_from_shopping_list, name='remove_from_shopping_list'),
    path('purchaseItem', purchase_item, name='purchase_item'),
    path('', include('apis.urls')),
]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




