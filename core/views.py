from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, FormView
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
import json
import base64
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
from products.models import Product
from outfits.models import Outfit
from .models import Wishlist, TryOnSession, Contact
from .forms import ContactForm


class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.filter(is_active=True)[:8]
        context['recent_outfits'] = Outfit.objects.filter(is_public=True)[:6]
        return context


class ImageTestView(TemplateView):
    template_name = 'image_test.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['summer_dress'] = Product.objects.get(title='Summer Dress')
        import time
        context['timestamp'] = int(time.time())
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_outfits'] = Outfit.objects.filter(user=user)[:5]
        context['wishlist_items'] = Wishlist.objects.filter(user=user)[:5]
        context['recommended_size'] = user.get_recommended_size()
        return context


class SizeGuideView(TemplateView):
    template_name = 'core/size_guide.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from products.models import SizeChart
        context['size_charts'] = SizeChart.objects.all()
        return context


class WishlistView(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = 'core/wishlist.html'
    context_object_name = 'wishlist_items'
    paginate_by = 12
    
    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user, 
        product=product
    )
    
    if created:
        messages.success(request, f'{product.title} added to wishlist!')
    else:
        messages.info(request, f'{product.title} is already in your wishlist!')
    
    return redirect('products:detail', pk=product_id)


@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        wishlist_item = Wishlist.objects.get(user=request.user, product=product)
        wishlist_item.delete()
        messages.success(request, f'{product.title} removed from wishlist!')
    except Wishlist.DoesNotExist:
        messages.error(request, 'Product not found in wishlist!')
    
    return redirect('core:wishlist')


@login_required
def try_on_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Create try-on session
    TryOnSession.objects.create(user=request.user, product=product)
    
    context = {
        'product': product,
        'user_measurements': {
            'height': request.user.height_cm,
            'weight': request.user.weight_kg,
            'body_type': request.user.body_type,
            'gender': request.user.gender,
        }
    }
    
    return render(request, 'core/try_on.html', context)


class TryOnTestView(TemplateView):
    template_name = 'core/try_on_test.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()[:6]  # Show first 6 products
        return context


class SearchView(ListView):
    model = Product
    template_name = 'core/search.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Product.objects.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) | 
                Q(category__icontains=query),
                is_active=True
            )
        return Product.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


@csrf_exempt
@require_http_methods(["POST"])
def virtual_tryon_api(request):
    """
    API endpoint for virtual try-on processing
    """
    try:
        print("Virtual try-on API called")  # Debug log
        data = json.loads(request.body)
        user_image = data.get('user_image')
        product_id = data.get('product_id')
        product_image = data.get('product_image')
        
        print(f"Received data: product_id={product_id}, has_user_image={bool(user_image)}")  # Debug log
        
        if not user_image or not product_id:
            print("Missing required data")  # Debug log
            return JsonResponse({'error': 'Missing required data'}, status=400)
        
        # Get the product
        try:
            product = Product.objects.get(id=product_id)
            print(f"Found product: {product.title}")  # Debug log
        except Product.DoesNotExist:
            print("Product not found")  # Debug log
            return JsonResponse({'error': 'Product not found'}, status=404)
        
        # Process the virtual try-on
        print("Processing virtual try-on...")  # Debug log
        result_image = process_virtual_tryon(user_image, product)
        print("Virtual try-on processing completed")  # Debug log
        
        # Save the try-on session if user is authenticated
        if request.user.is_authenticated:
            TryOnSession.objects.create(
                user=request.user,
                product=product
            )
            print("Try-on session saved")  # Debug log
        
        return JsonResponse({
            'success': True,
            'result_image': result_image,
            'product_name': product.title,
            'message': 'Virtual try-on completed successfully!'
        })
        
    except Exception as e:
        print(f"Error in virtual try-on API: {e}")  # Debug log
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


def process_virtual_tryon(user_image_data, product):
    """
    Enhanced virtual try-on with realistic clothing overlay
    """
    try:
        print("Starting virtual try-on processing...")  # Debug log
        
        # Decode base64 image
        image_data = user_image_data.split(',')[1]
        user_image = Image.open(io.BytesIO(base64.b64decode(image_data)))
        print(f"User image loaded: {user_image.size}, mode: {user_image.mode}")  # Debug log
        
        # Convert to RGB if needed
        if user_image.mode != 'RGB':
            user_image = user_image.convert('RGB')
        
        # Resize to standard dimensions for processing
        user_image = user_image.resize((400, 600), Image.Resampling.LANCZOS)
        print("User image resized to (400, 600)")  # Debug log
        
        # Load product image if available
        product_image = None
        if product.image:
            try:
                product_image = Image.open(product.image.path)
                print(f"Product image loaded: {product_image.size}")  # Debug log
            except Exception as e:
                print(f"Failed to load product image: {e}")  # Debug log
                pass
        else:
            print("No product image available")  # Debug log
        
        # Create realistic clothing overlay
        print("Creating realistic clothing overlay...")  # Debug log
        result = create_realistic_clothing_overlay(user_image, product_image, product)
        print("Clothing overlay created successfully")  # Debug log
        
        # Convert back to base64
        buffer = io.BytesIO()
        result.save(buffer, format='JPEG', quality=90)
        result_b64 = base64.b64encode(buffer.getvalue()).decode()
        print("Result image converted to base64")  # Debug log
        
        return f"data:image/jpeg;base64,{result_b64}"
        
    except Exception as e:
        print(f"Error in virtual try-on processing: {e}")
        import traceback
        traceback.print_exc()
        return user_image_data


def create_realistic_clothing_overlay(user_image, product_image, product):
    """Create realistic clothing overlay with proper fitting"""
    width, height = user_image.size
    result = user_image.copy()
    
    # Define body regions
    body_regions = {
        'head': (width//4, height//8, width//2, height//4),
        'upper_torso': (width//6, height//4, 2*width//3, height//3),
        'lower_torso': (width//4, 7*height//12, width//2, 5*height//12),
        'full_body': (width//8, height//6, 3*width//4, 2*height//3)
    }
    
    if product_image:
        # Use actual product image
        result = overlay_product_image(result, product_image, product, body_regions)
    else:
        # Create stylized clothing representation
        result = create_stylized_clothing(result, product, body_regions)
    
    # Add realistic effects
    result = add_clothing_effects(result, product)
    
    return result


def overlay_product_image(user_image, product_image, product, body_regions):
    """Overlay actual product image onto user"""
    # Process product image
    processed_product = process_product_for_overlay(product_image, product)
    
    # Get clothing region
    region = get_clothing_region(product.category, body_regions)
    
    # Fit product to body region
    fitted_product = fit_product_to_region(processed_product, region, product.category)
    
    # Create overlay
    overlay = Image.new('RGBA', user_image.size, (0, 0, 0, 0))
    
    # Position clothing
    x, y = calculate_clothing_position(region, fitted_product.size, product.category)
    
    # Paste with proper blending
    if fitted_product.mode == 'RGBA':
        overlay.paste(fitted_product, (x, y), fitted_product)
    else:
        fitted_product = fitted_product.convert('RGBA')
        # Make background transparent
        fitted_product = remove_white_background(fitted_product)
        overlay.paste(fitted_product, (x, y), fitted_product)
    
    # Blend with user image
    result = Image.alpha_composite(user_image.convert('RGBA'), overlay)
    return result.convert('RGB')


def process_product_for_overlay(product_image, product):
    """Process product image for better overlay"""
    # Remove background
    if product_image.mode != 'RGBA':
        product_image = product_image.convert('RGBA')
    
    # Remove white/light backgrounds
    product_image = remove_white_background(product_image)
    
    # Enhance for overlay
    from PIL import ImageEnhance
    
    # Increase contrast slightly
    enhancer = ImageEnhance.Contrast(product_image)
    product_image = enhancer.enhance(1.1)
    
    # Adjust saturation
    enhancer = ImageEnhance.Color(product_image)
    product_image = enhancer.enhance(1.05)
    
    return product_image


def remove_white_background(image):
    """Remove white/light background from product image using PIL only"""
    # Convert to RGBA if needed
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # Get pixel data
    data = list(image.getdata())
    new_data = []
    
    # Process each pixel
    for item in data:
        # If pixel is close to white/light gray, make it transparent
        r, g, b = item[:3]
        alpha = item[3] if len(item) == 4 else 255
        
        # Calculate brightness
        brightness = (r + g + b) / 3
        
        # Check if it's a light background pixel
        if brightness > 240 and abs(r - g) < 20 and abs(g - b) < 20 and abs(r - b) < 20:
            # Make transparent
            new_data.append((r, g, b, 0))
        elif brightness > 220 and abs(r - g) < 30 and abs(g - b) < 30 and abs(r - b) < 30:
            # Semi-transparent
            new_data.append((r, g, b, alpha // 2))
        else:
            # Keep original
            new_data.append(item)
    
    # Create new image
    new_image = Image.new('RGBA', image.size)
    new_image.putdata(new_data)
    
    # Apply edge smoothing
    new_image = new_image.filter(ImageFilter.SMOOTH_MORE)
    
    return new_image


def get_clothing_region(category, body_regions):
    """Get appropriate body region for clothing category"""
    category = category.lower()
    
    if category in ['shirt', 't-shirt', 'top', 'blouse', 'tank top']:
        return body_regions['upper_torso']
    elif category in ['dress', 'jumpsuit', 'romper']:
        return body_regions['full_body']
    elif category in ['pants', 'jeans', 'trousers', 'leggings']:
        return body_regions['lower_torso']
    elif category in ['skirt']:
        # Lower part of torso
        region = body_regions['lower_torso']
        return (region[0], region[1] + region[3]//3, region[2], 2*region[3]//3)
    elif category in ['jacket', 'blazer', 'coat', 'cardigan']:
        # Slightly larger than upper torso
        region = body_regions['upper_torso']
        return (region[0] - 10, region[1] - 20, region[2] + 20, region[3] + 40)
    else:
        return body_regions['upper_torso']


def fit_product_to_region(product_image, region, category):
    """Fit product image to body region with appropriate transformations"""
    target_width = region[2]
    target_height = region[3]
    
    # Resize product to fit region
    product_fitted = product_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    # Apply category-specific transformations
    if category.lower() in ['shirt', 't-shirt', 'top']:
        # Add slight perspective for body curvature
        product_fitted = apply_body_curve(product_fitted, 'upper')
    elif category.lower() in ['pants', 'jeans']:
        # Add leg perspective
        product_fitted = apply_body_curve(product_fitted, 'lower')
    elif category.lower() in ['dress']:
        # Full body curve
        product_fitted = apply_body_curve(product_fitted, 'full')
    
    return product_fitted


def apply_body_curve(image, body_part):
    """Apply realistic body curvature to clothing"""
    w, h = image.size
    
    if body_part == 'upper':
        # Slight inward curve for torso
        transform = (0, 0.05, 1, -0.05, 1, 0.95, 0, 1)
    elif body_part == 'lower':
        # Leg tapering
        transform = (0, 0, 1, 0.02, 1, 0.98, 0, 1)
    elif body_part == 'full':
        # Full body curve
        transform = (0, 0.02, 1, -0.02, 1, 0.98, 0, 1)
    else:
        return image
    
    try:
        curved = image.transform(
            (w, h),
            Image.Transform.PERSPECTIVE,
            transform,
            Image.Resampling.LANCZOS
        )
        return curved
    except:
        return image


def calculate_clothing_position(region, clothing_size, category):
    """Calculate optimal position for clothing on body"""
    region_x, region_y, region_w, region_h = region
    cloth_w, cloth_h = clothing_size
    
    # Center horizontally
    x = region_x + (region_w - cloth_w) // 2
    
    # Adjust vertical position based on clothing type
    if category.lower() in ['shirt', 't-shirt', 'top']:
        y = region_y + 10  # Slightly below shoulders
    elif category.lower() in ['pants', 'jeans']:
        y = region_y  # At waist level
    elif category.lower() in ['dress']:
        y = region_y - 20  # Higher for dress
    elif category.lower() in ['jacket', 'blazer']:
        y = region_y - 10  # Slightly higher
    else:
        y = region_y
    
    return max(0, x), max(0, y)


def create_stylized_clothing(user_image, product, body_regions):
    """Create stylized clothing when no product image is available"""
    overlay = Image.new('RGBA', user_image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Get clothing region
    region = get_clothing_region(product.category, body_regions)
    region_x, region_y, region_w, region_h = region
    
    # Get product color
    color = get_enhanced_product_color(product)
    
    # Create clothing shape based on category
    if product.category.lower() in ['shirt', 't-shirt', 'top']:
        create_shirt_shape(draw, region, color)
    elif product.category.lower() in ['pants', 'jeans']:
        create_pants_shape(draw, region, color)
    elif product.category.lower() in ['dress']:
        create_dress_shape(draw, region, color)
    elif product.category.lower() in ['jacket', 'blazer']:
        create_jacket_shape(draw, region, color)
    else:
        create_generic_clothing_shape(draw, region, color)
    
    # Add product label
    add_product_label(draw, user_image.size, product, region)
    
    # Blend with user image
    result = Image.alpha_composite(user_image.convert('RGBA'), overlay)
    return result.convert('RGB')


def create_shirt_shape(draw, region, color):
    """Create realistic shirt shape"""
    x, y, w, h = region
    
    # Main shirt body
    draw.rounded_rectangle([x+10, y+20, x+w-10, y+h-10], radius=15, fill=(*color, 120))
    
    # Sleeves
    draw.ellipse([x-5, y+15, x+25, y+h//2], fill=(*color, 100))
    draw.ellipse([x+w-25, y+15, x+w+5, y+h//2], fill=(*color, 100))
    
    # Neckline
    draw.ellipse([x+w//2-15, y+10, x+w//2+15, y+35], fill=(0, 0, 0, 0))


def create_pants_shape(draw, region, color):
    """Create realistic pants shape"""
    x, y, w, h = region
    
    # Left leg
    draw.rounded_rectangle([x+5, y, x+w//2-2, y+h], radius=10, fill=(*color, 130))
    
    # Right leg
    draw.rounded_rectangle([x+w//2+2, y, x+w-5, y+h], radius=10, fill=(*color, 130))
    
    # Waistband
    draw.rectangle([x, y-5, x+w, y+15], fill=(*darken_color(color), 150))


def create_dress_shape(draw, region, color):
    """Create realistic dress shape"""
    x, y, w, h = region
    
    # Upper part (fitted)
    draw.rounded_rectangle([x+15, y, x+w-15, y+h//2], radius=12, fill=(*color, 125))
    
    # Lower part (flared)
    draw.rounded_rectangle([x+5, y+h//3, x+w-5, y+h], radius=15, fill=(*color, 115))
    
    # Sleeves (optional)
    draw.ellipse([x, y+5, x+20, y+h//3], fill=(*color, 100))
    draw.ellipse([x+w-20, y+5, x+w, y+h//3], fill=(*color, 100))


def create_jacket_shape(draw, region, color):
    """Create realistic jacket shape"""
    x, y, w, h = region
    
    # Main jacket body
    draw.rounded_rectangle([x, y, x+w, y+h], radius=18, fill=(*color, 110))
    
    # Lapels
    points = [(x+w//4, y), (x+w//2, y+30), (x+w//4, y+h//3)]
    draw.polygon(points, fill=(*darken_color(color), 130))
    
    points = [(x+3*w//4, y), (x+w//2, y+30), (x+3*w//4, y+h//3)]
    draw.polygon(points, fill=(*darken_color(color), 130))
    
    # Sleeves
    draw.rounded_rectangle([x-10, y+10, x+15, y+h], radius=12, fill=(*color, 105))
    draw.rounded_rectangle([x+w-15, y+10, x+w+10, y+h], radius=12, fill=(*color, 105))


def create_generic_clothing_shape(draw, region, color):
    """Create generic clothing shape"""
    x, y, w, h = region
    draw.rounded_rectangle([x+8, y+8, x+w-8, y+h-8], radius=12, fill=(*color, 115))


def darken_color(color, factor=0.7):
    """Darken a color by a factor"""
    return tuple(int(c * factor) for c in color)


def get_enhanced_product_color(product):
    """Enhanced color detection for products"""
    color_map = {
        'navy': (25, 25, 112),
        'denim': (72, 106, 139),
        'khaki': (189, 183, 107),
        'olive': (128, 128, 0),
        'burgundy': (128, 0, 32),
        'maroon': (128, 0, 0),
        'teal': (0, 128, 128),
        'coral': (255, 127, 80),
        'lavender': (230, 230, 250),
        'mint': (152, 255, 152),
        'beige': (245, 245, 220),
        'cream': (255, 253, 208),
        'charcoal': (54, 69, 79),
        'steel': (70, 130, 180),
    }
    
    # Add basic colors
    basic_colors = {
        'blue': (70, 130, 180),
        'red': (220, 20, 60),
        'green': (34, 139, 34),
        'black': (47, 79, 79),
        'white': (245, 245, 245),
        'pink': (255, 182, 193),
        'purple': (147, 112, 219),
        'yellow': (255, 215, 0),
        'orange': (255, 140, 0),
        'brown': (139, 69, 19),
        'gray': (128, 128, 128),
        'grey': (128, 128, 128),
    }
    
    color_map.update(basic_colors)
    
    # Check product fields for color keywords
    text_fields = [
        getattr(product, 'color', ''),
        product.title,
        getattr(product, 'description', '')
    ]
    
    search_text = ' '.join(str(field) for field in text_fields).lower()
    
    for color_name, rgb in color_map.items():
        if color_name in search_text:
            return rgb
    
    # Default to a neutral color
    return (100, 149, 237)


def add_product_label(draw, image_size, product, region):
    """Add product name label"""
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    text = product.title[:20] + "..." if len(product.title) > 20 else product.title
    
    # Calculate text position
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (image_size[0] - text_width) // 2
    y = region[1] + region[3] + 10
    
    # Draw background
    padding = 8
    draw.rounded_rectangle(
        [x - padding, y - padding//2, x + text_width + padding, y + text_height + padding//2],
        radius=8,
        fill=(255, 255, 255, 200)
    )
    
    # Draw text
    draw.text((x, y), text, font=font, fill=(40, 44, 63))


def add_clothing_effects(image, product):
    """Add realistic effects like shadows and highlights"""
    from PIL import ImageEnhance, ImageFilter
    
    # Enhance contrast for more realistic look
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.05)
    
    # Add subtle sharpening
    image = image.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=2))
    
    # Adjust based on material type
    material = getattr(product, 'material', '').lower()
    
    if 'silk' in material or 'satin' in material:
        # Add slight brightness for sheen
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.03)
    elif 'denim' in material or 'cotton' in material:
        # Slightly muted colors
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(0.98)
    elif 'leather' in material:
        # Higher contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.1)
    
    return image


def get_product_color(product):
    """
    Get color for product overlay based on product properties
    """
    color_map = {
        'blue': (100, 149, 237),
        'red': (220, 20, 60),
        'green': (34, 139, 34),
        'black': (47, 79, 79),
        'white': (245, 245, 245),
        'pink': (255, 63, 108),
        'purple': (147, 112, 219),
        'yellow': (255, 215, 0),
        'orange': (255, 140, 0),
    }
    
    # Check product color or title for color keywords
    color_text = (product.color or product.title).lower()
    
    for color_name, rgb in color_map.items():
        if color_name in color_text:
            return rgb
    
    # Default to Myntra pink
    return (255, 63, 108)


class ContactView(FormView):
    template_name = 'core/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('core:contact')
    
    def form_valid(self, form):
        # Save contact message to database
        contact = Contact.objects.create(
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            phone=form.cleaned_data.get('phone', ''),
            inquiry_type=form.cleaned_data['inquiry_type'],
            subject=form.cleaned_data['subject'],
            message=form.cleaned_data['message']
        )
        
        # Add success message
        messages.success(
            self.request, 
            f'Thank you, {form.cleaned_data["name"]}! Your message has been sent successfully. We will get back to you within 24 hours.'
        )
        
        # You can add email sending functionality here
        # send_contact_email(contact)
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(
            self.request,
            'There was an error with your submission. Please check the form and try again.'
        )
        return super().form_invalid(form)


class HelpCenterView(TemplateView):
    template_name = 'core/help_center.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'core/privacy_policy.html'


class TermsOfServiceView(TemplateView):
    template_name = 'core/terms_of_service.html'
