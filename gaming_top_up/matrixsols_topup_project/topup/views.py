from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import TopUpOrderSerializer

class TopUpOrderCreateAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = TopUpOrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return Response({"message": "Order created successfully", "order_id": order.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from django.shortcuts import render
from datetime import timedelta
from django.utils import timezone
from .models import TopUpOrder

@staff_member_required
def dashboard_view(request):
    # Top 5 most purchased products
    top_products = (
        TopUpOrder.objects.filter(status='success')
        .values('product__name')
        .annotate(total_orders=Count('id'))
        .order_by('-total_orders')[:5]
    )

    # Daily revenue for last 7 days
    today = timezone.now().date()
    last_week = today - timedelta(days=6)
    daily_revenue = (
        TopUpOrder.objects.filter(status='success', created_at__date__gte=last_week)
        .extra(select={'day': 'date(created_at)'})
        .values('day')
        .annotate(total_revenue=Sum('product__price'))
        .order_by('day')
    )

    # Failed payments current month
    now = timezone.now()
    failed_count = TopUpOrder.objects.filter(
        status='failed',
        created_at__year=now.year,
        created_at__month=now.month
    ).count()

    return render(request, 'topup/dashboard.html', {
        'top_products': top_products,
        'daily_revenue': daily_revenue,
        'failed_count': failed_count
    })
