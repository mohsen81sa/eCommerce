from django.db import models
from django.utils.text import slugify
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(unique=True, blank=True, verbose_name="اسلاگ")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام برند")
    logo = models.ImageField(upload_to='brands/', blank=True, null=True, verbose_name="لوگوی برند")

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_CHOICES = [
        ('draft', 'پیش‌نویس'),
        ('active', 'فعال'),
        ('out_of_stock', 'ناموجود'),
        ('discontinued', 'متوقف شده'),
    ]

    title = models.CharField(max_length=255, verbose_name="عنوان محصول")
    slug = models.SlugField(unique=True, blank=True, verbose_name="اسلاگ")
    description = models.TextField(verbose_name="توضیحات")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="قیمت تخفیف")
    stock = models.PositiveIntegerField(default=0, verbose_name="موجودی")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products', verbose_name="دسته‌بندی")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="برند")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="وضعیت")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="تصویر محصول")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")
    is_featured = models.BooleanField(default=False, verbose_name="محصول ویژه")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_final_price(self):
        return self.discount_price if self.discount_price else self.price

    def is_in_stock(self):
        return self.stock > 0 and self.status == 'active'

    def get_formatted_price(self):
        # تبدیل قیمت به تومان و جداسازی سه رقم
        price = self.get_final_price()
        return f"{int(price):,} تومان"

    def __str__(self):
        return self.title
