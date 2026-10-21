from django.db import models
from django.contrib.auth.models import User


class Table(models.Model):
    number = models.PositiveIntegerField(unique=True, verbose_name="Stol raqami")
    seats = models.PositiveIntegerField(default=4, verbose_name="O'rinlar soni")
    is_available = models.BooleanField(default=True, verbose_name="Bo'shmi")

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"Stol №{self.number}"


class MenuItem(models.Model):
    CATEGORIES = [
        ('food', 'Taom'),
        ('drink', 'Ichimlik'),
        ('dessert', 'Desert'),
    ]
    name = models.CharField(max_length=100, verbose_name="Nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")
    category = models.CharField(max_length=10, choices=CATEGORIES, default='food', verbose_name="Kategoriya")
    is_available = models.BooleanField(default=True, verbose_name="Mavjud")

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUSES = [
        ('new', 'Yangi'),
        ('preparing', 'Tayyorlanmoqda'),
        ('done', 'Tayyor'),
        ('paid', "To'langan"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    table = models.ForeignKey(Table, on_delete=models.PROTECT, related_name='orders', verbose_name="Stol")
    items = models.ManyToManyField(MenuItem, related_name='orders', verbose_name="Taomlar")
    status = models.CharField(max_length=10, choices=STATUSES, default='new', verbose_name="Holat")
    note = models.CharField(max_length=200, blank=True, verbose_name="Izoh")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def total_price(self):
        return sum(item.price for item in self.items.all())

    def __str__(self):
        return f"Buyurtma #{self.pk} - {self.table}"