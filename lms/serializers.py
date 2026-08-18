from lms.models import Course, Lesson
from rest_framework import serializers
from lms.models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Lesson
        fields = ['id', 'course', 'owner', 'title', 'description', 'preview', 'video_url']


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Course
        fields = ['id', 'owner', 'title', 'preview', 'description', 'lessons', 'lessons_count']

    def get_lessons_count(self, obj):
        return obj.lessons.count()
