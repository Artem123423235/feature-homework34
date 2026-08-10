from django.urls import path
from users.views import UserProfileView, PaymentListView

urlpatterns = [
    path('<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('payments/', PaymentListView.as_view(), name='payment-list'),
]

urlpatterns = [
    path('<int:pk>/', UserProfileView.as_view(), name='user-profile'),
]
