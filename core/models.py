from django.db import models
from django.utils.text import slugify

class Trip(models.Model):
    CATEGORY_CHOICES = [
        ('trekking', 'Trekking'),
        ('tour', 'Tour'),
        ('sightseeing', 'Sightseeing'),
        ('climbing', 'Climbing'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    region = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)  # e.g. "16 days" or "8 hours"
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.PositiveIntegerField(default=0)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='trips/')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title