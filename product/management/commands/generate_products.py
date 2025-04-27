import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from product.models import ProductModel, ProductCategoryModel, ProductStatusType
from account.models import User  # تغییر به آدرس صحیح مدل کاربر
from pathlib import Path
from django.core.files import File

BASE_DIR = Path(__file__).resolve().parent


class Command(BaseCommand):
    help = 'Generate fake products'

    def handle(self, *args, **options):
        fake = Faker(locale="fa_IR")
        
        # دریافت یک کاربر مدیر (یا اولین کاربر موجود)
        try:
            # اگر می‌خواهید از کاربران مدیر استفاده کنید، باید فیلد is_staff یا is_superuser را بررسی کنید
            user = User.objects.filter(is_staff=True).first() or User.objects.first()
            if not user:
                raise User.DoesNotExist
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('No user found. Please create a user first.'))
            return

        # لیست تصاویر
        image_list = [
            "./images/img1.jpg",
            "./images/img2.jpg",
            "./images/img3.jpg",
            "./images/img4.jpg",
            "./images/img5.jpg",
            "./images/img6.jpg",
            "./images/img7.jpg",
            "./images/img8.jpg",
            # اضافه کردن تصاویر بیشتر در صورت نیاز
        ]

        categories = ProductCategoryModel.objects.all()

        for _ in range(10):  # تولید 10 محصول فیک
            num_categories = random.randint(1, 4)
            selected_categories = random.sample(list(categories), num_categories)
            title = ' '.join([fake.word() for _ in range(1,3)])
            slug = slugify(title, allow_unicode=True)
            selected_image = random.choice(image_list)
            image_obj = File(file=open(BASE_DIR / selected_image, "rb"), name=Path(selected_image).name)
            description = fake.paragraph(nb_sentences=10)
            brief_description = fake.paragraph(nb_sentences=1)
            stock = fake.random_int(min=0, max=10)
            status = random.choice(ProductStatusType.choices)[0]
            price = fake.random_int(min=10000, max=100000)
            discount_percent = fake.random_int(min=0, max=50)

            product = ProductModel.objects.create(
                user=user,
                title=title,
                slug=slug,
                image=image_obj,
                description=description,
                brief_description=brief_description,
                stock=stock,
                status=status,
                price=price,
                discount_percent=discount_percent,
            )
            product.category.set(selected_categories)

        self.stdout.write(self.style.SUCCESS('Successfully generated 10 fake products'))