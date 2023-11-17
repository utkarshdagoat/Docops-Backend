from django.urls import path
from .views import NotificationListView , NotificationDeleteAPIView


urlpatterns = [
    path('list/' , NotificationListView.as_view()), 
    path('delete/<int:pk>' , NotificationDeleteAPIView.as_view())
]