from django.db import models


class Medicine(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    minimum_stock = models.PositiveIntegerField(default=10)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Batch(models.Model):
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name='batches'
    )
    batch_number = models.CharField(max_length=100)
    expiry_date = models.DateField()
    quantity = models.PositiveIntegerField(default=0)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicine.name} - {self.batch_number}"

class Sale(models.Model):
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name='sales'
    )
    batch = models.ForeignKey(
        Batch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sales'
    )
    quantity = models.PositiveIntegerField()
    sale_date = models.DateField()
    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    @property
    def total_amount(self):
        return self.quantity * self.selling_price

    def __str__(self):
        return f"{self.medicine.name} - {self.sale_date}"