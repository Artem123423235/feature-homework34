# habits/tasks.py
from celery import shared_task
from .models import Habit  # если есть модель Habit
from django.utils import timezone
from datetime import timedelta


@shared_task
def send_habit_reminders():
    """
    Логика отправки напоминаний пользователям.
    Здесь вы будете получать все привычки, у которых наступило время отправки,
    и отправлять сообщения через Telegram.
    """
    # Пример: берём все привычки, где время напоминания <= текущему времени + 5 минут
    # и пользователь заполнил chat_id
    now = timezone.now()
    habits = Habit.objects.filter(
        user__telegram_chat_id__isnull=False,
        reminder_time__lte=now + timedelta(minutes=5),
        # ... другие условия
    )
    for habit in habits:
        chat_id = habit.user.telegram_chat_id
        # отправить сообщение через бота
        pass
