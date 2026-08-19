from django.db import models
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=200)
    preview = models.ImageField(upload_to='course_previews/', null=True, blank=True)
    description = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='courses'
    )

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    description = models.TextField()
    preview = models.ImageField(upload_to='lesson_previews/', null=True, blank=True)
    video_url = models.URLField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='lessons'
    )

    def __str__(self):
        return self.title

class Payment(models.Model):
    CASH = 'cash'
    TRANSFER = 'transfer'

    PAYMENT_METHODS = [
        (CASH, 'Наличные'),
        (TRANSFER, 'Перевод'),
    ]

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='payments'
    )
    payment_date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHODS,
        default=TRANSFER,
    )

    def __str__(self):
        return f'{self.user.email} - {self.amount}'
