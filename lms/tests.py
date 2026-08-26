from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from lms.models import Course, Lesson, Subscription


class LessonCRUDTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@test.com',
            password='testpass123'
        )
        self.course = Course.objects.create(title='Test Course')
        self.lesson = Lesson.objects.create(
            course=self.course,
            title='Existing Lesson',
            video_url='https://www.youtube.com/watch?v=abc123'
        )
        self.lesson_data = {
            'course': self.course.id,
            'title': 'New Lesson',
            'video_url': 'https://www.youtube.com/watch?v=xyz789'
        }

    def test_list_lessons_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/lms/lessons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_lesson_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/lms/lessons/', self.lesson_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_lesson_with_external_link_fails(self):
        self.client.force_authenticate(user=self.user)
        invalid_data = self.lesson_data.copy()
        invalid_data['video_url'] = 'https://vk.com/video123'
        response = self.client.post('/lms/lessons/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_lesson(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f'/lms/lessons/{self.lesson.id}/',
            {'title': 'Updated'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/lms/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_cannot_create_lesson(self):
        response = self.client.post('/lms/lessons/', self.lesson_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SubscriptionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@test.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            email='other@test.com',
            password='testpass123'
        )
        self.course = Course.objects.create(title='Subscription Course')

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/lms/courses/{self.course.id}/subscribe/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_unsubscribe_from_course(self):
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/lms/courses/{self.course.id}/unsubscribe/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_course_list_shows_is_subscribed_for_current_user(self):
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/lms/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['results'][0]['is_subscribed'])

    def test_course_list_shows_not_subscribed_for_other_user(self):
        Subscription.objects.create(user=self.other_user, course=self.course)
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/lms/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['results'][0]['is_subscribed'])


class PaginationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@test.com',
            password='testpass123'
        )
        for i in range(5):
            Course.objects.create(title=f'Course {i}')

    def test_course_list_has_pagination(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/lms/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('next', response.data)
        self.assertIn('results', response.data)
