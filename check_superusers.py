import os
import sys
import django

# Add the project directory to sys.path
sys.path.append('d:/Python Dev/Python-Fullstack/FashionFit')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashionFit.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print("=== All Users ===")
all_users = User.objects.all()
for user in all_users:
    print(f"Username: {user.username} | Email: {user.email} | Superuser: {user.is_superuser} | Staff: {user.is_staff} | Active: {user.is_active}")

print("\n=== Superusers Only ===")
superusers = User.objects.filter(is_superuser=True)
if superusers.exists():
    for superuser in superusers:
        print(f"- {superuser.username} ({superuser.email})")
else:
    print("No superusers found in the system")

print(f"\nTotal users: {User.objects.count()}")
print(f"Total superusers: {User.objects.filter(is_superuser=True).count()}")
print(f"Total staff users: {User.objects.filter(is_staff=True).count()}")
