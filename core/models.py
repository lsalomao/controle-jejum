from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Email')
    name = models.CharField(max_length=150, verbose_name='Nome')
    fasting_goal_hours = models.FloatField(default=16.0, verbose_name='Meta de Jejum (horas)')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.email


class FastingRecord(models.Model):
    FASTING_TYPE_CHOICES = [
        ('intermittent', 'Jejum Intermitente'),
        ('extended', 'Jejum Prolongado'),
        ('other', 'Outro'),
    ]

    LEVEL_CHOICES = [
        (1, 'Baixo'),
        (2, 'Médio'),
        (3, 'Alto'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='fasting_records', verbose_name='Usuário')
    start_time = models.DateTimeField(verbose_name='Início')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='Fim')
    duration_hours = models.FloatField(null=True, blank=True, verbose_name='Duração (horas)')
    fasting_type = models.CharField(max_length=20, choices=FASTING_TYPE_CHOICES, default='intermittent', verbose_name='Tipo de Jejum')
    energy_level = models.IntegerField(choices=LEVEL_CHOICES, null=True, blank=True, verbose_name='Nível de Energia')
    focus_level = models.IntegerField(choices=LEVEL_CHOICES, null=True, blank=True, verbose_name='Nível de Foco')
    mood_level = models.IntegerField(choices=LEVEL_CHOICES, null=True, blank=True, verbose_name='Nível de Humor')
    notes = models.CharField(max_length=255, blank=True, verbose_name='Observações')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        verbose_name = 'Registro de Jejum'
        verbose_name_plural = 'Registros de Jejum'
        ordering = ['-start_time']

    def __str__(self):
        return f"{self.user.email} - {self.start_time.strftime('%d/%m/%Y %H:%M')}"

    def clean(self):
        super().clean()
        
        if self.end_time and self.start_time >= self.end_time:
            raise ValidationError('O horário de término deve ser posterior ao horário de início.')
        
        overlapping = FastingRecord.objects.filter(user=self.user).exclude(pk=self.pk)
        
        for record in overlapping:
            if record.end_time is None:
                if self.start_time <= record.start_time:
                    raise ValidationError('Já existe um jejum ativo. Encerre-o antes de iniciar um novo.')
                if self.end_time and self.end_time > record.start_time:
                    raise ValidationError('Este jejum se sobrepõe a um jejum ativo existente.')
            else:
                if self.start_time < record.end_time and (self.end_time is None or self.end_time > record.start_time):
                    raise ValidationError(f'Este jejum se sobrepõe ao jejum de {record.start_time.strftime("%d/%m/%Y %H:%M")} a {record.end_time.strftime("%d/%m/%Y %H:%M")}.')

    def save(self, *args, **kwargs):
        self.full_clean()
        
        if self.end_time and self.start_time:
            duration = self.end_time - self.start_time
            self.duration_hours = round(duration.total_seconds() / 3600, 2)
        
        super().save(*args, **kwargs)


class WeightRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='weight_records', verbose_name='Usuário')
    weight = models.FloatField(verbose_name='Peso (kg)')
    reference_month = models.CharField(max_length=7, verbose_name='Mês de Referência')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        verbose_name = 'Registro de Peso'
        verbose_name_plural = 'Registros de Peso'
        unique_together = ['user', 'reference_month']
        ordering = ['-reference_month']

    def __str__(self):
        return f"{self.user.email} - {self.reference_month}: {self.weight}kg"

    def clean(self):
        super().clean()
        
        if self.weight <= 0:
            raise ValidationError('O peso deve ser maior que zero.')
