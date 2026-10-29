from django.db import models


# Create your models here.
class Product(models.Model):
    p_sku = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.IntegerField()
    location = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "products"
        ordering = ["-date_created"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.p_sku
