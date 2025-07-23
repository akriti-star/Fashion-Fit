# Virtual Try-On Testing Instructions

## Step 1: Start the Server
1. Double-click on `start_server.bat` in your FashionFit folder
2. Or open command prompt and run:
   ```
   cd "d:\Python Dev\Python-Fullstack\FashionFit"
   python manage.py runserver
   ```

## Step 2: Load Sample Data (REQUIRED)
The database needs products for try-on to work. Run this command:

```bash
python manage.py loaddata fixtures/sample_data.json
```

This creates:
- Test buyer account: `testbuyer` / password: `testpass123` 
- Test seller account: `testseller` / password: `testpass123`
- Product categories: Tops, Bottoms
- Sample products: Blue T-Shirt (ID:1), Dark Jeans (ID:2), Red Polo (ID:3)

**Alternative: Create via Django Admin**
1. Create superuser: `python manage.py createsuperuser`
2. Go to: http://127.0.0.1:8000/admin/
3. Create Categories and Products manually

## Step 3: Access Virtual Try-On
You can now access virtual try-on in multiple ways:

### � **Header Navigation (Always Available)**
- **Virtual Try-On Button**: Available in the main navigation bar on every page
  - **For authenticated users**: "VIRTUAL TRY-ON" button with gradient styling
  - **For guests**: "TRY ON" button redirects to login first
  - **User dropdown**: Buyers have additional "Virtual Try-On" option in their profile menu

### 🛍️ **Product Pages with Try-On Prompt**
- **Products Page**: http://127.0.0.1:8000/products/
  - Each product card has a "Try On" button
  - View individual products at: http://127.0.0.1:8000/products/<product_id>/
  - **Auto-prompt**: A modal will appear asking if you want to try virtual try-on (after 3 seconds or when scrolling)

### 🧪 **Testing Page**
- **Try-On Test Page**: http://127.0.0.1:8000/try-on-test/
  - Shows authentication status
  - Lists all available products with direct try-on buttons

## Step 4: Authentication
- **Test accounts available after loading sample data**:
  - Username: `testbuyer` / Password: `testpass123` (for try-on)
  - Username: `testseller` / Password: `testpass123` (for selling)
- **Login URL**: http://127.0.0.1:8000/accounts/login/
- **Note**: Use the `testbuyer` account for virtual try-on functionality

## Step 5: Direct Try-On URLs (After Loading Sample Data)
- http://127.0.0.1:8000/try-on/1/ (Blue Cotton T-Shirt)
- http://127.0.0.1:8000/try-on/2/ (Dark Denim Jeans)  
- http://127.0.0.1:8000/try-on/3/ (Red Polo Shirt)

## Troubleshooting

### If try-on page shows "Page not found":
1. Make sure the server is running
2. Check that products exist in database
3. Verify you're logged in

### If you see "No products found":
1. Run: `python create_tryon_products.py`
2. Refresh the try-on test page

### If try-on button is grayed out:
1. Make sure you're logged in as a buyer (not seller)
2. Check authentication status on try-on test page

## Quick Check Commands
```bash
# Check if products exist
python manage.py shell -c "from products.models import Product; print(f'Products: {Product.objects.count()}')"

# Check if users exist  
python manage.py shell -c "from accounts.models import CustomUser; print(f'Users: {CustomUser.objects.count()}')"
```

The virtual try-on functionality is fully implemented. The issue might be:
1. Server not running
2. No products in database  
3. Not logged in
4. Accessing wrong URL

Follow these steps and the try-on feature should work!
