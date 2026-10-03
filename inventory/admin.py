from django.contrib import admin
from .models import Medicine, Batch, Sale


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'manufacturer',
        'minimum_stock',
        'selling_price',
        'created_at',
    )
    search_fields = ('name', 'manufacturer')
    list_filter = ('category',)


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = (
        'medicine',
        'batch_number',
        'expiry_date',
        'quantity',
        'purchase_price',
        'supplier',
    )
    search_fields = ('batch_number', 'medicine__name', 'supplier')
    list_filter = ('expiry_date',)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = (
        'medicine',
        'batch',
        'quantity',
        'sale_date',
        'selling_price',
        'total_amount',
    )
    search_fields = ('medicine__name', 'batch__batch_number')
    list_filter = ('sale_date', 'medicine')