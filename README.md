<<<<<<< HEAD
# FashionFit - Smart Fashion Try-On Platform

A modern e-commerce platform that revolutionizes online clothing shopping by integrating virtual try-on features and personalized size recommendations.

## Features

### 🎯 Core Features
- **Smart Size Recommendations**: Get personalized size suggestions based on body measurements
- **Virtual Try-On**: Visualize how clothes look on different body types
- **Outfit Builder**: Create and save complete outfits with drag-and-drop interface
- **Product Reviews**: Rate products on fit, comfort, and style
- **Wishlist**: Save favorite products for later
- **User Profiles**: Manage body measurements and preferences

### 🛠 Technical Features
- **Responsive Design**: Built with Tailwind CSS for mobile-first design
- **User Authentication**: Secure registration and login system
- **Admin Panel**: Comprehensive content management
- **Search & Filter**: Advanced product search and filtering
- **Rating System**: Multi-dimensional product ratings

## Technology Stack

- **Backend**: Django 5.2.4 (Python)
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Database**: PostgreSQL
- **Image Processing**: Pillow
- **Authentication**: Django's built-in authentication system

## Installation

### Prerequisites
- Python 3.10+
- PostgreSQL database
- Virtual environment

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd FashionFit
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**
   - Create a PostgreSQL database named `fashiondb`
   - Update database credentials in `FashionFit/settings.py`:
   ```python
   DATABASES = {
       "default": {
           "ENGINE": "django.db.backends.postgresql",
           "NAME": "fashiondb",
           "USER": "your_username",
           "PASSWORD": "your_password",
           "HOST": "localhost",
           "PORT": "5432",
       }
   }
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Populate sample data (optional)**
   ```bash
   python manage.py populate_data
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
FashionFit/
├── FashionFit/          # Main project settings
├── accounts/            # User authentication and profiles
├── products/            # Product management
├── outfits/            # Outfit creation and management
├── reviews/            # Product reviews and ratings
├── core/               # Core functionality and home page
├── templates/          # HTML templates
├── static/             # Static files (CSS, JS, images)
├── media/              # User-uploaded media files
├── requirements.txt    # Python dependencies
└── manage.py          # Django management script
```

## Apps Overview

### 1. Accounts App
- Custom user model with body measurements
- User registration, login, logout
- Profile management
- Size recommendations based on measurements

### 2. Products App
- Product catalog with categories
- Size charts and availability
- Product images and details
- Search and filtering

### 3. Outfits App
- Outfit creation and management
- Outfit builder interface
- Social features (likes, public outfits)
- Outfit sharing

### 4. Reviews App
- Multi-dimensional ratings (fit, comfort, style)
- Review comments and images
- User review history
- Product rating aggregation

### 5. Core App
- Home page and navigation
- Wishlist functionality
- Virtual try-on sessions
- Search functionality

## Database Schema

### Key Models

**CustomUser**
- Extended Django user model
- Body measurements (height, weight, chest, waist, hips)
- Body type and gender
- Size recommendation logic

**Product**
- Product information and pricing
- Category classification
- Size chart associations
- Image management

**Outfit**
- User-created outfit collections
- Product associations
- Privacy settings
- Social features

**Review**
- Multi-dimensional ratings
- Comment system
- User associations
- Product feedback

## Admin Panel

Access the admin panel at `/admin/` to:
- Manage users and their profiles
- Add/edit products and categories
- Configure size charts
- Moderate reviews and outfits
- View site analytics

## API Endpoints

### Size Recommendations
- `GET /products/size-recommendation/<product_id>/` - Get size recommendation for a product

### Outfit Management
- `POST /outfits/<pk>/like/` - Toggle outfit like
- `GET /outfits/builder/` - Access outfit builder

### Wishlist
- `POST /wishlist/add/<product_id>/` - Add to wishlist
- `POST /wishlist/remove/<product_id>/` - Remove from wishlist

## Customization

### Adding New Product Categories
1. Update `CATEGORY_CHOICES` in `products/models.py`
2. Run migrations
3. Update templates if needed

### Modifying Size Recommendation Logic
Edit the `get_recommended_size()` method in `accounts/models.py`

### Styling Changes
- Global styles: Update Tailwind classes in templates
- Custom CSS: Add to `static/css/` directory

## Sample Data

The `populate_data` management command creates:
- Size charts (XS, S, M, L, XL)
- Sample products across all categories
- Admin user (username: admin, password: admin123)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For questions or issues:
- Check the documentation
- Review existing GitHub issues
- Create a new issue with detailed description

## Future Enhancements

- [ ] AI-powered size recommendations
- [ ] 3D virtual try-on
- [ ] Social sharing features
- [ ] Mobile app
- [ ] Payment integration
- [ ] Inventory management
- [ ] Analytics dashboard
- [ ] Multi-language support

---

Built with ❤️ using Django and Tailwind CSS
=======
# Fashion-Fit
>>>>>>> 062c0b573f0422da8a90ff550333d17d7fbea7b6
