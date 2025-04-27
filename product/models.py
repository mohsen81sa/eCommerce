from django.db import models
from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator
from account.models import User  # اضافه کردن ایمپورت مدل کاربر سفارشی

class ProductStatusType(models.IntegerChoices):
    publish = 1, "نمایش"
    draft = 2, "عدم نمایش"

class ProductCategoryModel(models.Model):
    title = models.CharField("عنوان", max_length=255)
    slug = models.SlugField("اسلاگ", allow_unicode=True, unique=True)

    created_date = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_date = models.DateTimeField("تاریخ بروزرسانی", auto_now=True)

    class Meta:
        ordering = ["-created_date"]
        verbose_name = "دسته‌بندی محصول"
        verbose_name_plural = "دسته‌بندی‌های محصول"

    def __str__(self):
        return self.title

class ProductModel(models.Model):
    user = models.ForeignKey(User, verbose_name="کاربر", on_delete=models.PROTECT)  # تغییر به مدل User مستقیم
    category = models.ManyToManyField(ProductCategoryModel, verbose_name="دسته‌بندی‌ها")
    title = models.CharField("عنوان", max_length=255)
    slug = models.SlugField("اسلاگ", allow_unicode=True, unique=True)
    image = models.ImageField("تصویر اصلی", default="/default/product-image.png", upload_to="product/img/")
    description = models.TextField("توضیحات کامل")
    brief_description = models.TextField("توضیح کوتاه", null=True, blank=True)

    stock = models.PositiveIntegerField("موجودی", default=0)
    status = models.IntegerField("وضعیت", choices=ProductStatusType.choices, default=ProductStatusType.draft.value)
    price = models.DecimalField("قیمت", default=0, max_digits=10, decimal_places=0)
    discount_percent = models.IntegerField("درصد تخفیف", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    avg_rate = models.FloatField("میانگین امتیاز", default=0.0)

    created_date = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_date = models.DateTimeField("تاریخ بروزرسانی", auto_now=True)

    class Meta:
        ordering = ["-created_date"]
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.title

    def get_price(self):
        discount_amount = self.price * Decimal(self.discount_percent / 100)
        discounted_amount = self.price - discount_amount
        return round(discounted_amount)

    def is_discounted(self):
        return self.discount_percent != 0

    def is_published(self):
        return self.status == ProductStatusType.publish.value

class ProductImageModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="product_images", verbose_name="محصول")
    file = models.ImageField("تصویر", upload_to="product/extra-img/")

    created_date = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_date = models.DateTimeField("تاریخ بروزرسانی", auto_now=True)

    class Meta:
        ordering = ["-created_date"]
        verbose_name = "تصویر اضافی محصول"
        verbose_name_plural = "تصاویر اضافی محصول"

class WishlistProductModel(models.Model):
    user = models.ForeignKey(User, verbose_name="کاربر", on_delete=models.PROTECT)  # تغییر به مدل User مستقیم
    product = models.ForeignKey(ProductModel, verbose_name="محصول", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "محصول مورد علاقه"
        verbose_name_plural = "محصولات مورد علاقه"
        unique_together = ('user', 'product')  # اضافه کردن این خط برای جلوگیری از تکرار

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"