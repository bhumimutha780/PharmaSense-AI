from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

from .models import Medicine, Batch, Sale


def dashboard(request):
    today = timezone.now().date()
    expiry_limit = today + timedelta(days=90)

    total_medicines = Medicine.objects.count()

    total_stock = Batch.objects.aggregate(
        total=Sum('quantity')
    )['total'] or 0

    today_sales = Sale.objects.filter(
        sale_date=today
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    low_stock_medicines = []

    for medicine in Medicine.objects.all():
        stock = medicine.batches.aggregate(
            total=Sum('quantity')
        )['total'] or 0

        if stock <= medicine.minimum_stock:
            low_stock_medicines.append({
                'medicine': medicine,
                'stock': stock
            })

    expiring_batches = Batch.objects.filter(
        expiry_date__lte=expiry_limit,
        expiry_date__gte=today
    ).order_by('expiry_date')

    context = {
        'total_medicines': total_medicines,
        'total_stock': total_stock,
        'today_sales': today_sales,
        'low_stock_medicines': low_stock_medicines,
        'expiring_batches': expiring_batches,
    }

    return render(
        request,
        'inventory/dashboard.html',
        context
    )


def alerts(request):
    today = timezone.now().date()
    ninety_days = today + timedelta(days=90)

    expired_batches = Batch.objects.filter(
        expiry_date__lt=today
    ).select_related('medicine')

    expiring_batches = Batch.objects.filter(
        expiry_date__gte=today,
        expiry_date__lte=ninety_days
    ).select_related('medicine')

    low_stock_batches = Batch.objects.filter(
        quantity__lte=10
    ).select_related('medicine')

    context = {
        'expired_batches': expired_batches,
        'expiring_batches': expiring_batches,
        'low_stock_batches': low_stock_batches,
    }

    return render(
        request,
        'inventory/alerts.html',
        context
    )