from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from lms.models import Course, Lesson, Subscription
from lms.serializers import CourseSerializer, LessonSerializer
from lms.paginators import CoursePaginator, LessonPaginator
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ... остальные методы (subscribe, unsubscribe) ...


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPaginator
    permission_classes = [IsAuthenticatedOrReadOnly]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator

    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk=None):
        course = self.get_object()
        user = request.user

        if not user.is_authenticated:
            return Response(
                {'error': 'Требуется авторизация'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        Subscription.objects.get_or_create(user=user, course=course)
        return Response({'status': 'subscribed'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def unsubscribe(self, request, pk=None):
        course = self.get_object()
        user = request.user

        Subscription.objects.filter(user=user, course=course).delete()
        return Response({'status': 'unsubscribed'}, status=status.HTTP_204_NO_CONTENT)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPaginator
