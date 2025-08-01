# 🖼️ Image Management Guide for FashionFit

## 📁 Directory Structure

```
FashionFit/
├── media/                          # User-uploaded & dynamic content
│   ├── products/                   # Product images
│   │   ├── classic_white_tshirt.jpg
│   │   ├── slim_fit_jeans.jpg
│   │   └── ...
│   └── users/                      # User profile pictures
│       └── avatars/
│
├── static/                         # Static design assets
│   ├── images/                     # Website graphics
│   │   ├── logo.png
│   │   ├── hero-banner.jpg
│   │   └── icons/
│   ├── css/
│   └── js/
│
└── templates/                      # HTML templates
```

## 🎯 Where to Put Different Types of Images

### 1. **Product Images** → `media/products/`
- **Purpose**: Images of fashion items (shirts, jeans, dresses, etc.)
- **Upload via**: Admin panel or user uploads
- **Template usage**: `{{ product.image.url }}`
- **Example**: `media/products/summer_dress.jpg`

### 2. **User Profile Pictures** → `media/users/`
- **Purpose**: User avatars and profile photos
- **Upload via**: User profile forms
- **Template usage**: `{{ user.profile_picture.url }}`
- **Example**: `media/users/john_doe_avatar.jpg`

### 3. **Website Graphics** → `static/images/`
- **Purpose**: Logos, icons, banners, backgrounds
- **Upload via**: Developer adds directly to folder
- **Template usage**: `{% load static %}` then `{% static 'images/logo.png' %}`
- **Example**: `static/images/logo.png`

## 📝 How to Add Images

### Method 1: Through Django Admin
1. Go to: http://127.0.0.1:8000/admin/
2. Login with: `admin` / `admin123`
3. Navigate to Products → Add/Edit Product
4. Upload image in the "Image" field
5. Save the product

### Method 2: Direct File Upload
1. **For products**: Copy images to `media/products/`
2. **For static assets**: Copy images to `static/images/`
3. **Update database**: Link the image path in the model

### Method 3: Programmatically (for developers)
```python
# In Django shell or management command
from products.models import Product
from django.core.files import File

product = Product.objects.get(id=1)
with open('path/to/image.jpg', 'rb') as f:
    product.image.save('image.jpg', File(f))
```

## 🌐 Template Usage Examples

### Product Images (Media Files)
```html
<!-- Check if image exists -->
{% if product.image %}
    <img src="{{ product.image.url }}" alt="{{ product.title }}">
{% else %}
    <div class="placeholder-image">No Image</div>
{% endif %}
```

### Static Images (Website Graphics)
```html
{% load static %}
<img src="{% static 'images/logo.png' %}" alt="FashionFit Logo">
<img src="{% static 'images/hero-banner.jpg' %}" alt="Hero Banner">
```

## 🔧 Current Setup Status

✅ **Media serving**: Configured in `urls.py`
✅ **Media directory**: Created at `media/`
✅ **Static directory**: Created at `static/`
✅ **Sample images**: Generated automatically
✅ **Database links**: Products linked to images

## 🚀 Quick Start: Adding Your Own Images

1. **Replace placeholder images**:
   ```bash
   # Navigate to media/products/
   cd "d:\Python Dev\Python-Fullstack\FashionFit\media\products"
   
   # Replace with your actual product images
   # Keep the same filenames or update database
   ```

2. **Add website graphics**:
   ```bash
   # Navigate to static/images/
   cd "d:\Python Dev\Python-Fullstack\FashionFit\static\images"
   
   # Add your logo, banners, etc.
   # Reference in templates with {% static 'images/filename.jpg' %}
   ```

3. **Test image display**:
   - Start server: `python manage.py runserver`
   - Visit: http://127.0.0.1:8000/
   - Check if product images show up

## 🎨 Image Recommendations

### Product Images
- **Size**: 400x500px (or 4:5 ratio)
- **Format**: JPG or PNG
- **Quality**: High resolution for detail
- **Background**: Clean, preferably white

### Static Graphics
- **Logo**: PNG with transparency
- **Banners**: 1920x600px for hero sections
- **Icons**: SVG or PNG 32x32px

## 🔍 Troubleshooting

### Images Not Showing?
1. Check if file exists in correct directory
2. Verify `MEDIA_URL` and `MEDIA_ROOT` in settings
3. Ensure media serving is enabled in `urls.py`
4. Check file permissions

### Database Issues?
1. Update product records to point to correct image path
2. Use Django admin to re-upload images
3. Run `python manage.py populate_data` to reset sample data

## 📱 Current Image URLs

Your product images are accessible at:
- http://127.0.0.1:8000/media/products/classic_white_tshirt.jpg
- http://127.0.0.1:8000/media/products/slim_fit_jeans.jpg
- http://127.0.0.1:8000/media/products/summer_dress.jpg
- http://127.0.0.1:8000/media/products/leather_jacket.jpg
- http://127.0.0.1:8000/media/products/running_shoes.jpg
- http://127.0.0.1:8000/media/products/designer_handbag.jpg
