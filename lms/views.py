from rest_framework import generics, viewsets
from rest_framework.exceptions import PermissionDenied
from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer


def is_moderator(user):
    return user.groups.filter(name='moderators').exists()


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        if is_moderator(self.request.user):
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        if is_moderator(self.request.user):
            raise PermissionDenied('Модератор не может создавать курсы')
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        if is_moderator(self.request.user):
            raise PermissionDenied('Модератор не может удалять курсы')
        instance.delete()


class LessonListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        if is_moderator(self.request.user):
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        if is_moderator(self.request.user):
            raise PermissionDenied('Модератор не может создавать уроки')
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        if is_moderator(self.request.user):
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)

    def perform_destroy(self, instance):
        if is_moderator(self.request.user):
            raise PermissionDenied('Модератор не может удалять уроки')
        instance.delete()
