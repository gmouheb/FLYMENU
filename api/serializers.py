# from rest_framework import serializers
#
#
# from Category.models import Category
# from Item.models import Item
# from Menu.models import Menu
#
#
#
# class CategorySerializer(serializers.ModelSerializer):
#
#     class Meta:
#
#         model = Category
#         fields = '__all__'

from rest_framework import serializers
from Category.models import Category
from Item.models import Item
from Menu.models import Menu
from django.utils.text import slugify




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing categories"""

    class Meta:
        model = Category
        fields = ['id', 'Name']


class ItemSerializer(serializers.ModelSerializer):
    # Display category details in responses
    Category = CategorySerializer(read_only=True)
    # Accept category ID for create/update operations
    category_id = serializers.IntegerField(write_only=True, source='Category_id')

    class Meta:
        model = Item
        fields = ['id', 'Name', 'Category', 'category_id', 'Price', 'Image', 'Available', 'Description']

    def validate_category_id(self, value):
        """Ensure the category exists"""
        if not Category.objects.filter(id=value).exists():
            raise serializers.ValidationError("Category with this ID does not exist.")
        return value


class ItemListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing items"""
    Category = CategoryListSerializer(read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'Name', 'Category', 'Price', 'Available']


class MenuSerializer(serializers.ModelSerializer):
    # Display full item details in responses
    MenuItems = ItemSerializer(many=True, read_only=True)
    # Accept item IDs for create/update operations
    menu_items_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        allow_empty=True
    )
    Table = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Menu
        fields = ['id', 'Title', 'Slug', 'MenuItems', 'menu_items_ids', 'Table']
        extra_kwargs = {
            'Slug': {'read_only': True}
        }

    def validate_menu_items_ids(self, value):
        """Ensure all items exist"""
        if value:
            existing_items = Item.objects.filter(id__in=value).count()
            if existing_items != len(value):
                raise serializers.ValidationError("Some items do not exist.")
        return value

    # def create(self, validated_data):
    #     menu_items_ids = validated_data.pop('menu_items_ids', [])
    #     menu = Menu.objects.create(**validated_data)
    #     if menu_items_ids:
    #         menu.MenuItems.set(menu_items_ids)
    #     return menu

    def create(self, validated_data):
        menu_items_ids = validated_data.pop('menu_items_ids', [])

        # Generate slug from Title
        title = validated_data.get('Title')
        validated_data['Slug'] = slugify(title)

        menu = Menu.objects.create(**validated_data)

        if menu_items_ids:
            menu.MenuItems.set(menu_items_ids)

        return menu

    def update(self, instance, validated_data):
        menu_items_ids = validated_data.pop('menu_items_ids', None)

        # Update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update menu items if provided
        if menu_items_ids is not None:
            instance.MenuItems.set(menu_items_ids)

        return instance


class MenuListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing menus"""
    items_count = serializers.SerializerMethodField()
    Table = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Menu
        fields = ['id', 'Title', 'Slug', 'items_count', 'Table']

    def get_items_count(self, obj):
        return obj.MenuItems.count()