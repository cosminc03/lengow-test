from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from orders import views


urlpatterns = [
    path("", views.OrderList.as_view(), name="order_list"),
    path("<str:pk>", views.OrderDetail.as_view(), name="order_detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
