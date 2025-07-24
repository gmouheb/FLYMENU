# Restaurant Menu API

A Django REST Framework API for managing restaurant menus, items, and categories. This API provides complete CRUD operations for managing menu systems with categories, items, and menu collections.

## Features

- **Complete CRUD Operations** for Categories, Items, and Menus
- **Advanced Filtering and Search** capabilities
- **Optimized Database Queries** with select_related and prefetch_related
- **Menu Statistics** and analytics
- **Flexible Menu Management** with item associations
- **Image Upload Support** for menu items
- **RESTful API Design** following Django REST Framework best practices

## Models

### Category
- **Name**: Category name (CharField, max 255 chars)
- **Description**: Optional category description (TextField)

### Item
- **Name**: Item name (CharField, max 255 chars)
- **Category**: Foreign key to Category
- **Price**: Item price (DecimalField, max 10 digits, 2 decimal places)
- **Image**: Optional item image (ImageField)
- **Available**: Availability status (BooleanField, default True)
- **Description**: Optional item description (TextField)

### Menu
- **Title**: Menu title (CharField, max 255 chars)
- **Slug**: Auto-generated unique slug (SlugField)
- **MenuItems**: Many-to-many relationship with Items

## API Endpoints

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/categories/` | List all categories |
| POST | `/api/categories/` | Create new category |
| GET | `/api/categories/{id}/` | Get specific category |
| PUT/PATCH | `/api/categories/{id}/` | Update category |
| DELETE | `/api/categories/{id}/` | Delete category |
| GET | `/api/categories/{id}/items/` | Get all items in category |

### Items

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/items/` | List all items (with filtering) |
| POST | `/api/items/` | Create new item |
| GET | `/api/items/{id}/` | Get specific item |
| PUT/PATCH | `/api/items/{id}/` | Update item |
| DELETE | `/api/items/{id}/` | Delete item |
| GET | `/api/items/search/` | Search items by name/description |

### Menus

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/menus/` | List all menus |
| POST | `/api/menus/` | Create new menu |
| GET | `/api/menus/{id}/` | Get specific menu with items |
| GET | `/api/menus/{slug}/` | Get specific menu by slug |
| PUT/PATCH | `/api/menus/{id}/` | Update menu |
| DELETE | `/api/menus/{id}/` | Delete menu |
| POST | `/api/menus/{id}/items/add/` | Add items to menu |
| DELETE | `/api/menus/{id}/items/remove/` | Remove items from menu |
| GET | `/api/menus/{id}/statistics/` | Get menu statistics |

## Query Parameters

### Items Filtering
- `category`: Filter by category ID
- `available`: Filter by availability (true/false)
- `search`: Search in name and description

**Example:**
```
GET /api/items/?category=1&available=true&search=pizza
```

### Category Items Filtering
- `available`: Filter items by availability within a category

**Example:**
```
GET /api/categories/1/items/?available=true
```

### Item Search
- `q`: Search query (required)
- `category`: Filter by category ID
- `available`: Filter by availability

**Example:**
```
GET /api/items/search/?q=chicken&category=1&available=true
```

## Request/Response Examples

### Create Category
```http
POST /api/categories/
Content-Type: application/json

{
    "Name": "Main Courses",
    "Description": "Hearty main dishes and entrees"
}
```

**Response:**
```json
{
    "id": 1,
    "Name": "Main Courses",
    "Description": "Hearty main dishes and entrees"
}
```

### Create Item
```http
POST /api/items/
Content-Type: application/json

{
    "Name": "Margherita Pizza",
    "category_id": 1,
    "Price": "15.99",
    "Available": true,
    "Description": "Classic pizza with tomato sauce, mozzarella, and fresh basil"
}
```

**Response:**
```json
{
    "id": 1,
    "Name": "Margherita Pizza",
    "Category": {
        "id": 1,
        "Name": "Main Courses",
        "Description": "Hearty main dishes and entrees"
    },
    "Price": "15.99",
    "Image": null,
    "Available": true,
    "Description": "Classic pizza with tomato sauce, mozzarella, and fresh basil"
}
```

### Create Menu
```http
POST /api/menus/
Content-Type: application/json

{
    "Title": "Lunch Special",
    "menu_items_ids": [1, 2, 3]
}
```

**Response:**
```json
{
    "id": 1,
    "Title": "Lunch Special",
    "Slug": "lunch-special",
    "MenuItems": [
        {
            "id": 1,
            "Name": "Margherita Pizza",
            "Category": {
                "id": 1,
                "Name": "Main Courses",
                "Description": "Hearty main dishes and entrees"
            },
            "Price": "15.99",
            "Image": null,
            "Available": true,
            "Description": "Classic pizza with tomato sauce, mozzarella, and fresh basil"
        }
    ]
}
```

### Add Items to Menu
```http
POST /api/menus/1/items/add/
Content-Type: application/json

{
    "item_ids": [4, 5, 6]
}
```

### Get Menu Statistics
```http
GET /api/menus/1/statistics/
```

**Response:**
```json
{
    "menu": {
        "id": 1,
        "title": "Lunch Special",
        "slug": "lunch-special"
    },
    "statistics": {
        "total_items": 5,
        "available_items": 4,
        "unavailable_items": 1,
        "categories": ["Main Courses", "Beverages"],
        "category_count": 2,
        "price_range": {
            "min": 8.99,
            "max": 24.99,
            "average": 16.79
        }
    }
}
```

## API Responses Overview

Below is a summary of the main API endpoints and the JSON data they provide:

### Categories
- **GET `/api/categories/`**: List all categories.
  ```json
  [
    {"id": 1, "Name": "Main Courses"},
    {"id": 2, "Name": "Beverages"}
  ]
  ```
- **GET `/api/categories/{id}/`**: Get details of a specific category.
  ```json
  {"id": 1, "Name": "Main Courses", "Description": "Hearty main dishes and entrees"}
  ```
- **GET `/api/categories/{id}/items/`**: List all items in a category.
  ```json
  {
    "category": {"id": 1, "Name": "Main Courses", "Description": "Hearty main dishes and entrees"},
    "items": [
      {"id": 1, "Name": "Margherita Pizza", "Category": {"id": 1, "Name": "Main Courses"}, "Price": "15.99", "Available": true}
    ]
  }
  ```

### Items
- **GET `/api/items/`**: List all items (with optional filtering).
  ```json
  [
    {"id": 1, "Name": "Margherita Pizza", "Category": {"id": 1, "Name": "Main Courses"}, "Price": "15.99", "Available": true}
  ]
  ```
- **GET `/api/items/{id}/`**: Get details of a specific item.
  ```json
  {
    "id": 1,
    "Name": "Margherita Pizza",
    "Category": {"id": 1, "Name": "Main Courses", "Description": "Hearty main dishes and entrees"},
    "Price": "15.99",
    "Image": null,
    "Available": true,
    "Description": "Classic pizza with tomato sauce, mozzarella, and fresh basil"
  }
  ```
- **GET `/api/items/search/?q=...`**: Search items by name/description.
  ```json
  {
    "query": "pizza",
    "count": 1,
    "results": [
      {"id": 1, "Name": "Margherita Pizza", "Category": {"id": 1, "Name": "Main Courses"}, "Price": "15.99", "Available": true}
    ]
  }
  ```

### Menus
- **GET `/api/menus/`**: List all menus.
  ```json
  [
    {"id": 1, "Title": "Lunch Special", "Slug": "lunch-special", "items_count": 3}
  ]
  ```
- **GET `/api/menus/{id}/`**: Get details of a specific menu by ID.
- **GET `/api/menus/{slug}/`**: Get details of a specific menu by slug.
  ```json
  {
    "id": 1,
    "Title": "Lunch Special",
    "Slug": "lunch-special",
    "MenuItems": [
      {"id": 1, "Name": "Margherita Pizza", "Category": {"id": 1, "Name": "Main Courses", "Description": "Hearty main dishes and entrees"}, "Price": "15.99", "Image": null, "Available": true, "Description": "Classic pizza with tomato sauce, mozzarella, and fresh basil"}
    ]
  }
  ```
- **GET `/api/menus/{id}/statistics/`**: Get statistics for a menu.
  ```json
  {
    "menu": {"id": 1, "title": "Lunch Special", "slug": "lunch-special"},
    "statistics": {
      "total_items": 5,
      "available_items": 4,
      "unavailable_items": 1,
      "categories": ["Main Courses", "Beverages"],
      "category_count": 2,
      "price_range": {"min": 8.99, "max": 24.99, "average": 16.79}
    }
  }
  ```

For more details and request/response examples, see the sections above.

## Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd restaurant-menu-api
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install django djangorestframework pillow
```

4. **Configure settings:**
Add to your `settings.py`:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'Category',
    'Item',
    'Menu',
    'api',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

5. **Include API URLs:**
In your main `urls.py`:
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

6. **Run migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Create superuser (optional):**
```bash
python manage.py createsuperuser
```

8. **Run the server:**
```bash
python manage.py runserver
```

## Project Structure

```
restaurant-menu-api/
├── Category/
│   ├── models.py
│   ├── admin.py
│   └── ...
├── Item/
│   ├── models.py
│   ├── admin.py
│   └── ...
├── Menu/
│   ├── models.py
│   ├── admin.py
│   └── ...
├── api/
│   ├── views.py          # All CRUD operations
│   ├── serializers.py    # All serializers
│   ├── urls.py           # API endpoints
│   └── ...
├── media/                # Uploaded images
├── manage.py
└── requirements.txt
```

## Dependencies

- Django >= 3.2
- Django REST Framework >= 3.12
- Pillow >= 8.0 (for image handling)

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Invalid data or missing required fields
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

Error responses include descriptive messages:
```json
{
    "error": "Category with this ID does not exist."
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the repository.