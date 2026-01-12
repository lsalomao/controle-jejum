from django.test import TestCase, Client
from django.utils import timezone
from datetime import timedelta
from core.models import CustomUser, FastingRecord, WeightRecord
from django.core.exceptions import ValidationError


class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User',
            fasting_goal_hours=16.0
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.name, 'Test User')
        self.assertEqual(self.user.fasting_goal_hours, 16.0)
        self.assertTrue(self.user.check_password('testpass123'))

    def test_user_string_representation(self):
        self.assertEqual(str(self.user), 'test@example.com')


class FastingRecordModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User'
        )

    def test_fasting_duration_calculation(self):
        start = timezone.now()
        end = start + timedelta(hours=16)

        fasting = FastingRecord.objects.create(
            user=self.user,
            start_time=start,
            end_time=end,
            fasting_type='intermittent'
        )

        self.assertEqual(fasting.duration_hours, 16.0)

    def test_active_fasting_no_end_time(self):
        fasting = FastingRecord.objects.create(
            user=self.user,
            start_time=timezone.now(),
            fasting_type='intermittent'
        )

        self.assertIsNone(fasting.end_time)
        self.assertIsNone(fasting.duration_hours)

    def test_overlapping_fasting_validation(self):
        start1 = timezone.now()
        end1 = start1 + timedelta(hours=16)

        FastingRecord.objects.create(
            user=self.user,
            start_time=start1,
            end_time=end1,
            fasting_type='intermittent'
        )

        start2 = start1 + timedelta(hours=8)
        end2 = start2 + timedelta(hours=16)

        fasting2 = FastingRecord(
            user=self.user,
            start_time=start2,
            end_time=end2,
            fasting_type='intermittent'
        )

        with self.assertRaises(ValidationError):
            fasting2.save()

    def test_end_time_before_start_time_validation(self):
        start = timezone.now()
        end = start - timedelta(hours=1)

        fasting = FastingRecord(
            user=self.user,
            start_time=start,
            end_time=end,
            fasting_type='intermittent'
        )

        with self.assertRaises(ValidationError):
            fasting.save()


class WeightRecordModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User'
        )

    def test_weight_record_creation(self):
        weight = WeightRecord.objects.create(
            user=self.user,
            weight=75.5,
            reference_month='2026-01'
        )

        self.assertEqual(weight.weight, 75.5)
        self.assertEqual(weight.reference_month, '2026-01')

    def test_unique_weight_per_month(self):
        WeightRecord.objects.create(
            user=self.user,
            weight=75.5,
            reference_month='2026-01'
        )

        with self.assertRaises(Exception):
            WeightRecord.objects.create(
                user=self.user,
                weight=76.0,
                reference_month='2026-01'
            )


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User',
            fasting_goal_hours=16.0
        )

    def test_login_view(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)

    def test_dashboard_with_login(self):
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_start_fasting(self):
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.post('/fasting/start/')

        self.assertEqual(response.status_code, 302)

        active_fasting = FastingRecord.objects.filter(
            user=self.user,
            end_time__isnull=True
        ).first()

        self.assertIsNotNone(active_fasting)

    def test_cannot_start_multiple_fastings(self):
        self.client.login(email='test@example.com', password='testpass123')

        self.client.post('/fasting/start/')
        response = self.client.post('/fasting/start/')

        self.assertEqual(response.status_code, 302)

        active_fastings = FastingRecord.objects.filter(
            user=self.user,
            end_time__isnull=True
        ).count()

        self.assertEqual(active_fastings, 1)

    def test_end_fasting(self):
        self.client.login(email='test@example.com', password='testpass123')

        fasting = FastingRecord.objects.create(
            user=self.user,
            start_time=timezone.now() - timedelta(hours=16),
            fasting_type='intermittent'
        )

        response = self.client.post('/fasting/end/')

        self.assertEqual(response.status_code, 302)

        fasting.refresh_from_db()
        self.assertIsNotNone(fasting.end_time)
        self.assertIsNotNone(fasting.duration_hours)


class StreakCalculationTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User',
            fasting_goal_hours=16.0
        )

    def test_streak_calculation(self):
        today = timezone.now()

        for i in range(5):
            day = today - timedelta(days=i)
            FastingRecord.objects.create(
                user=self.user,
                start_time=day.replace(hour=20, minute=0),
                end_time=day.replace(hour=12, minute=0) + timedelta(days=1),
                fasting_type='intermittent'
            )

        from core.views import calculate_streak
        streak = calculate_streak(self.user)

        self.assertEqual(streak, 5)

    def test_streak_breaks_on_missed_day(self):
        today = timezone.now()

        FastingRecord.objects.create(
            user=self.user,
            start_time=today.replace(hour=20, minute=0),
            end_time=today.replace(hour=12, minute=0) + timedelta(days=1),
            fasting_type='intermittent'
        )

        yesterday = today - timedelta(days=1)
        FastingRecord.objects.create(
            user=self.user,
            start_time=yesterday.replace(hour=20, minute=0),
            end_time=yesterday.replace(hour=23, minute=0),
            fasting_type='intermittent'
        )

        from core.views import calculate_streak
        streak = calculate_streak(self.user)

        self.assertEqual(streak, 1)
