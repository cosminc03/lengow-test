from django.db import models


class Order(models.Model):
    id = models.CharField(max_length=200, primary_key=True, unique=True)
    marketplace = models.CharField(max_length=200)
    purchase_date = models.DateTimeField(null=True)
    currency = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.marketplace}_{self.id}"
