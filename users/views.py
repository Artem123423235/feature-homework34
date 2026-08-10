from rest_framework import generics
from users.models import User, Payment
from users.serializers import UserProfileSerializer, PaymentSerializer


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        queryset = Payment.objects.all()
        course_id = self.request.query_params.get('course')
        lesson_id = self.request.query_params.get('lesson')
        method = self.request.query_params.get('method')
        ordering = self.request.query_params.get('ordering')

        if course_id:
            queryset = queryset.filter(course_id=course_id)
        if lesson_id:
            queryset = queryset.filter(lesson_id=lesson_id)
        if method:
            queryset = queryset.filter(payment_method=method)

        # Сортировка по дате: 'payment_date' или '-payment_date'
        if ordering in ['payment_date', '-payment_date']:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by('-payment_date')

        return queryset

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
