# products/management/commands/add_categories.py

from django.core.management.base import BaseCommand
from products.models import Category

class Command(BaseCommand):
    help = 'Add predefined categories to the Category model'

    def handle(self, *args, **kwargs):
        categories = [
            { 'name': 'Electronics', 'icon': 'category/electronics.png' },
            { 'name': 'Clothing', 'icon': 'category/clothing.png' },
            { 'name': 'Home & Kitchen', 'icon': 'category/kitchen.png' },
            { 'name': 'Beauty & Personal Care', 'icon': 'category/beauty.png' },
            { 'name': 'Health & Wellness', 'icon': 'category/health.png' },
            { 'name': 'Toys & Games', 'icon': 'category/games.png' },
            { 'name': 'Sports & Outdoors', 'icon': 'category/outdoors.png' },
            { 'name': 'Automotive', 'icon': 'category/automotive.png' },
            { 'name': 'Books', 'icon': 'category/books.png' },
            { 'name': 'Music & Movies', 'icon': 'category/movies.png' },
            { 'name': 'Office Supplies', 'icon': 'category/office.png' },
            { 'name': 'Pet Supplies', 'icon': 'category/pets.png' },
            { 'name': 'Baby Products', 'icon': 'category/baby.png' },
            { 'name': 'Garden & Outdoor', 'icon': 'category/garden.png' },
            { 'name': 'Jewelry & Accessories', 'icon': 'category/jewelery.png' },
            { 'name': 'Shoes & Footwear', 'icon': 'category/footware.png' },
            { 'name': 'Handmade Products', 'icon': 'category/homemade.png' },
            { 'name': 'Groceries', 'icon': 'category/groceries.png' },
            { 'name': 'Furniture', 'icon': 'category/furniture.png' },
            { 'name': 'Appliances', 'icon': 'category/appliances.png' },
            { 'name': 'Tools & Home Improvement', 'icon': 'category/tools.png' },
            { 'name': 'Arts & Crafts', 'icon': 'category/crafts.png' },
            { 'name': 'Travel & Luggage', 'icon': 'category/luggage.png' },
            { 'name': 'Smart Home Devices', 'icon': 'category/smartdevice.png' },
            { 'name': 'Software', 'icon': 'category/software.png' },
            { 'name': 'Industrial & Scientific', 'icon': 'category/industrial.png' },
            { 'name': 'Collectibles & Fine Art', 'icon': 'category/fineart.png' },
            { 'name': 'Musical Instruments', 'icon': 'category/instruments.png' },
            { 'name': 'Gift Cards', 'icon': 'category/giftcards.png' },
            { 'name': 'Watches', 'icon': 'category/watches.png' },
        ]

        for category in categories:
            Category.objects.get_or_create(name=category['name'])
            self.stdout.write(self.style.SUCCESS(f"Category '{category['name']}' added or already exists."))
