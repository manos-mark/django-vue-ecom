from io import BytesIO
from PIL import Image

from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.files import File
from django.db import models

from apps.userprofile.models import Userprofile

class Store(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)

    date_added = models.DateTimeField(auto_now_add=True)
    num_visits = models.IntegerField(default=0)
    last_visit = models.DateTimeField(blank=True, null=True)

    is_activated = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/%s/' % (self.slug)

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.name)
        super().save(*args, **kwargs)

class StoreAdmin(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, blank=True, null=True)
    store = models.ForeignKey(Store, related_name='store', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.user.username + ": " + self.store.name

class Category(models.Model):
    store = models.ForeignKey(Store, related_name='categories', on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    ordering = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('ordering',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/%s/' % (self.slug)

class Product(models.Model):
    store = models.ForeignKey(Store, related_name='products', on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    is_featured = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    num_available = models.IntegerField(default=1)
    num_visits = models.IntegerField(default=0)
    last_visit = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.title
    
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)
        return thumbnail

    def get_absolute_url(self):
        return '/%s/%s/' % (self.category.slug, self.slug)

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image) 
                self.save()
                return self.thumbnail.url
            else:
                return ''

    def get_rating(self):
        total = sum(int(review['stars']) for review in self.reviews.values())

        if self.reviews.count() > 0:
            return total / self.reviews.count()
        else: 
            return 0
    
# class ProductImage(models.Model):
#     product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)

#     image = models.ImageField(upload_to='uploads/', blank=True, null=True)
#     thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)

#     def make_thumbnail(self, image, size=(300, 200)):
#         img = Image.open(image)
#         img.convert('RGB')
#         img.thumbnail(size)
        
#         thumb_io = BytesIO()
#         img.save(thumb_io, 'JPEG', quality=85)

#         thumbnail = File(thumb_io, name=image.name)
#         return thumbnail

#     def save(self, *args, **kwargs):
#         self.thumbnail = self.make_thumbnail(self.image)
#         super().save(*args, **kwargs)

class ProductReview(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)

    content = models.TextField(blank=True, null=True)
    stars = models.IntegerField()

    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title
