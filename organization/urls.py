from django.urls import path
from . import views

app_name = 'organization'

urlpatterns = [
    # 1. مسار صفحة العرض (HTML)
    path('org-chart/', views.org_chart_view, name='org_chart'),
    
    # 2. مسار جلب البيانات بصيغة JSON للـ JavaScript
    path('api/org-chart-data/', views.get_org_chart_data, name='org_chart_data'),
]