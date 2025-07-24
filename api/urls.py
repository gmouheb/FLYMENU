# from django.urls import path
# from .views import CategoryAPIView
#
#
# urlpatterns = [
#     path('', CategoryAPIView.as_view()),
# ]

from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # ==================== CATEGORY CRUD ====================
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),
    path('categories/<int:category_id>/items/', views.category_items, name='category-items'),

    # ==================== ITEM CRUD ====================
    path('items/', views.ItemListCreateView.as_view(), name='item-list-create'),
    path('items/<int:pk>/', views.ItemRetrieveUpdateDestroyView.as_view(), name='item-detail'),
    path('items/search/', views.search_items, name='item-search'),

    # ==================== MENU CRUD ====================
    path('menus/', views.MenuListCreateView.as_view(), name='menu-list-create'),
    path('menus/<int:pk>/', views.MenuRetrieveUpdateDestroyView.as_view(), name='menu-detail'),
    path('menus/<slug:Slug>/', views.MenuDetailBySlugView.as_view(), name='menu-detail-by-slug'),
    path('menus/<int:menu_id>/items/add/', views.add_items_to_menu, name='menu-add-items'),
    path('menus/<int:menu_id>/items/remove/', views.remove_items_from_menu, name='menu-remove-items'),
    path('menus/<int:menu_id>/statistics/', views.menu_statistics, name='menu-statistics'),
]