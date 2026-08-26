from django.db import models
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, default='')  # необязательное
    preview = models.ImageField(upload_to='course_previews', blank=True, null=True)

    class Meta:
        ordering = ['id']  # сортировка для пагинации

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, default='')  # необязательное
    video_url = models.URLField(blank=True, null=True)
    preview = models.ImageField(upload_to='lesson_previews', blank=True, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.amount}'


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscriptions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
        ordering = ['id']

    def __str__(self):
        return f'{self.user.email} -> {self.course.title}'
