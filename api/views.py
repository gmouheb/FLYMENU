# from django.shortcuts import render
# from rest_framework import generics
#
# from Category.models import Category
# from .serializers import CategorySerializer
#
#
#
#
#
# # Create your views here.
#
#
# class CategoryAPIView(generics.ListAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

from rest_framework import generics, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.db.models import Q

from Category.models import Category
from Item.models import Item
from Menu.models import Menu
from .serializers import (
    CategorySerializer, CategoryListSerializer,
    ItemSerializer, ItemListSerializer,
    MenuSerializer, MenuListSerializer
)


# ==================== CATEGORY CRUD ====================

class CategoryListCreateView(generics.ListCreateAPIView):
    """
    GET: List all categories
    POST: Create a new category
    """
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CategoryListSerializer
        return CategorySerializer


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a specific category
    PUT/PATCH: Update a category
    DELETE: Delete a category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# ==================== ITEM CRUD ====================

class ItemListCreateView(generics.ListCreateAPIView):
    """
    GET: List all items (with optional filtering)
    POST: Create a new item
    """
    serializer_class = ItemSerializer

    def get_queryset(self):
        queryset = Item.objects.select_related('Category').all()

        # Optional filtering
        category_id = self.request.query_params.get('category', None)
        available = self.request.query_params.get('available', None)
        search = self.request.query_params.get('search', None)

        if category_id is not None:
            queryset = queryset.filter(Category_id=category_id)

        if available is not None:
            is_available = available.lower() in ['true', '1', 'yes']
            queryset = queryset.filter(Available=is_available)

        if search is not None:
            queryset = queryset.filter(
                Q(Name__icontains=search) |
                Q(Description__icontains=search)
            )

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ItemListSerializer
        return ItemSerializer


class ItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a specific item
    PUT/PATCH: Update an item
    DELETE: Delete an item
    """
    queryset = Item.objects.select_related('Category').all()
    serializer_class = ItemSerializer


# ==================== MENU CRUD ====================

class MenuListCreateView(generics.ListCreateAPIView):
    """
    GET: List all menus
    POST: Create a new menu
    """

    def get_queryset(self):
        return Menu.objects.prefetch_related('MenuItems__Category').all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MenuListSerializer
        return MenuSerializer


class MenuRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a specific menu with all items
    PUT/PATCH: Update a menu
    DELETE: Delete a menu
    """
    queryset = Menu.objects.prefetch_related('MenuItems__Category').all()
    serializer_class = MenuSerializer


# ==================== ADDITIONAL UTILITY VIEWS ====================

@api_view(['GET'])
def category_items(request, category_id):
    """
    GET: Retrieve all items in a specific category
    """
    category = get_object_or_404(Category, id=category_id)
    items = Item.objects.filter(Category=category)

    # Optional filtering within category
    available = request.query_params.get('available', None)
    if available is not None:
        is_available = available.lower() in ['true', '1', 'yes']
        items = items.filter(Available=is_available)

    return Response({
        'category': CategorySerializer(category).data,
        'items': ItemListSerializer(items, many=True).data
    })


@api_view(['POST'])
def add_items_to_menu(request, menu_id):
    """
    POST: Add items to an existing menu
    Expected payload: {"item_ids": [1, 2, 3]}
    """
    menu = get_object_or_404(Menu, id=menu_id)
    item_ids = request.data.get('item_ids', [])

    if not item_ids:
        return Response(
            {'error': 'item_ids is required and cannot be empty'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Verify all items exist
    items = Item.objects.filter(id__in=item_ids)
    if len(items) != len(item_ids):
        missing_ids = set(item_ids) - set(items.values_list('id', flat=True))
        return Response(
            {'error': f'Items with IDs {list(missing_ids)} do not exist'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Add items to menu
    menu.MenuItems.add(*items)

    # Return updated menu
    serializer = MenuSerializer(menu)
    return Response({
        'message': f'Successfully added {len(items)} items to menu',
        'menu': serializer.data
    })


@api_view(['DELETE'])
def remove_items_from_menu(request, menu_id):
    """
    DELETE: Remove items from an existing menu
    Expected payload: {"item_ids": [1, 2, 3]}
    """
    menu = get_object_or_404(Menu, id=menu_id)
    item_ids = request.data.get('item_ids', [])

    if not item_ids:
        return Response(
            {'error': 'item_ids is required and cannot be empty'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Remove items from menu (doesn't matter if some don't exist)
    menu.MenuItems.remove(*item_ids)

    # Return updated menu
    serializer = MenuSerializer(menu)
    return Response({
        'message': f'Successfully removed items from menu',
        'menu': serializer.data
    })


@api_view(['GET'])
def search_items(request):
    """
    GET: Search items across all categories
    Query params: ?q=search_term&category=1&available=true
    """
    query = request.query_params.get('q', '')
    category_id = request.query_params.get('category', None)
    available = request.query_params.get('available', None)

    if not query:
        return Response(
            {'error': 'Search query parameter "q" is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    items = Item.objects.select_related('Category').filter(
        Q(Name__icontains=query) |
        Q(Description__icontains=query)
    )

    if category_id:
        items = items.filter(Category_id=category_id)

    if available is not None:
        is_available = available.lower() in ['true', '1', 'yes']
        items = items.filter(Available=is_available)

    serializer = ItemListSerializer(items, many=True)
    return Response({
        'query': query,
        'count': len(serializer.data),
        'results': serializer.data
    })


@api_view(['GET'])
def menu_statistics(request, menu_id):
    """
    GET: Get statistics for a specific menu
    """
    menu = get_object_or_404(Menu, id=menu_id)
    items = menu.MenuItems.all()

    total_items = items.count()
    available_items = items.filter(Available=True).count()
    categories = items.values_list('Category__Name', flat=True).distinct()

    # Price statistics
    prices = items.values_list('Price', flat=True)
    if prices:
        min_price = min(prices)
        max_price = max(prices)
        avg_price = sum(prices) / len(prices)
    else:
        min_price = max_price = avg_price = 0

    return Response({
        'menu': {
            'id': menu.id,
            'title': menu.Title,
            'slug': menu.Slug
        },
        'statistics': {
            'total_items': total_items,
            'available_items': available_items,
            'unavailable_items': total_items - available_items,
            'categories': list(categories),
            'category_count': len(categories),
            'price_range': {
                'min': float(min_price) if min_price else 0,
                'max': float(max_price) if max_price else 0,
                'average': round(float(avg_price), 2) if avg_price else 0
            }
        }
    })


class MenuDetailBySlugView(RetrieveAPIView):
    queryset = Menu.objects.prefetch_related('MenuItems__Category').all()
    serializer_class = MenuSerializer
    lookup_field = 'Slug'