import os
import random
import sys
import django
from pathlib import Path
from django.core.files import File
from django.utils.text import slugify

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

# This allows easy placement of apps within the interior divine_shop directory.
current_path = Path(__file__).parent.resolve()
sys.path.append(str(current_path / "divine_shop"))

django.setup()

from divine_shop.products.models import Category, Product, ProductImage
from django.contrib.auth import get_user_model

User = get_user_model()

def seed(count=50):
    print(f"Starting seeding of {count} products...")
    
    # 1. Get or create a category
    category, _ = Category.objects.get_or_create(
        name="Accessoires",
        defaults={"slug": "accessoires", "description": "Tous nos accessoires en perles"}
    )
    
    # 2. Get a user (seller)
    user = User.objects.filter(is_superuser=True).first()
    if not user:
        user = User.objects.first()
    
    if not user:
        print("No user found. Please create a superuser first.")
        return

    # 3. Get images from media
    media_dir = "divine_shop/media"
    images = [f for f in os.listdir(media_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    if not images:
        print(f"No images found in {media_dir}")
        return

    print(f"Found {len(images)} images: {images}")

    # 4. Create products
    for i in range(1, count + 1):
        name = f"Collier de perles Artisanat {i}"
        slug = slugify(f"collier-perles-{i}")
        
        # Ensure unique slug
        if Product.objects.filter(slug=slug).exists():
            slug = slugify(f"collier-perles-{i}-{random.randint(100, 999)}")

        product = Product.objects.create(
            category=category,
            seller=user,
            name=name,
            slug=slug,
            description=f"Une pièce unique faite à la main. Idéal pour toutes les occasions. Produit numéro {i}.",
            price=random.randint(2500, 15000),
            stock=random.randint(5, 30),
            is_available=True,
            is_featured=random.choice([True, False, False]),
            is_new=random.choice([True, False])
        )
        
        # Add image
        img_name = images[(i-1) % len(images)]
        img_path = os.path.join(media_dir, img_name)
        
        with open(img_path, 'rb') as f:
            product_image = ProductImage(product=product, is_main=True)
            product_image.image.save(img_name, File(f), save=True)
            
        print(f"Created product: {name}")

    print("Seeding completed successfully!")

if __name__ == "__main__":
    seed(50)
