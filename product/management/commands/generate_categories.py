from django.core.management.base import BaseCommand
from faker import Faker
from product.models import ProductCategoryModel  # تغییر مسیر به اپ product
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Generate fake categories'

    def handle(self, *args, **options):
        fake = Faker(locale="fa_IR")
        
        # لیست کلمات فارسی برای ایجاد دسته‌بندی‌های واقعی‌تر
        persian_categories = [
            'لباس مردانه', 'لباس زنانه', 'کفش', 'اکسسوری', 'لوازم الکترونیکی',
            'لوازم خانگی', 'کتاب', 'اسباب بازی', 'زیبایی و سلامت', 'ورزشی'
        ]

        for title in persian_categories:
            slug = slugify(title, allow_unicode=True)
            
            # ایجاد دسته‌بندی فقط در صورتی که وجود نداشته باشد
            category, created = ProductCategoryModel.objects.get_or_create(
                title=title,
                defaults={
                    'slug': slug,
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Category already exists: {title}'))

        self.stdout.write(self.style.SUCCESS('Successfully generated categories'))