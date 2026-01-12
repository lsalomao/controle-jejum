from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Avg, Count
from datetime import datetime, timedelta
from .models import CustomUser, FastingRecord, WeightRecord
from .forms import CustomUserCreationForm, CustomAuthenticationForm, FastingRecordForm, WeightRecordForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()

    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {user.name}!')
                return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu da sua conta.')
    return redirect('login')


@login_required
def dashboard_view(request):
    import json

    active_fasting = FastingRecord.objects.filter(user=request.user, end_time__isnull=True).first()

    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_fastings = FastingRecord.objects.filter(
        user=request.user,
        start_time__gte=seven_days_ago,
        end_time__isnull=False
    )

    avg_duration = recent_fastings.aggregate(Avg('duration_hours'))['duration_hours__avg'] or 0

    goal_hours = request.user.fasting_goal_hours
    days_above_goal = recent_fastings.filter(duration_hours__gte=goal_hours).count()

    streak = calculate_streak(request.user)

    chart_data = []
    for i in range(6, -1, -1):
        day = timezone.now() - timedelta(days=i)
        day_fastings = FastingRecord.objects.filter(
            user=request.user,
            start_time__date=day.date(),
            end_time__isnull=False
        )
        total_hours = sum([f.duration_hours for f in day_fastings])
        chart_data.append({
            'date': day.strftime('%d/%m'),
            'hours': round(total_hours, 2)
        })

    context = {
        'active_fasting': active_fasting,
        'avg_duration': round(avg_duration, 2),
        'days_above_goal': days_above_goal,
        'streak': streak,
        'goal_hours': goal_hours,
        'chart_data': json.dumps(chart_data),
    }

    return render(request, 'dashboard/dashboard.html', context)


@login_required
def start_fasting_view(request):
    if request.method == 'POST':
        active_fasting = FastingRecord.objects.filter(user=request.user, end_time__isnull=True).first()
        if active_fasting:
            messages.error(request, 'Você já tem um jejum ativo. Encerre-o antes de iniciar um novo.')
            return redirect('dashboard')

        try:
            fasting = FastingRecord.objects.create(
                user=request.user,
                start_time=timezone.now(),
                fasting_type='intermittent'
            )
            messages.success(request, 'Jejum iniciado com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao iniciar jejum: {str(e)}')

    return redirect('dashboard')


@login_required
def end_fasting_view(request):
    active_fasting = FastingRecord.objects.filter(user=request.user, end_time__isnull=True).first()

    if not active_fasting:
        messages.error(request, 'Não há jejum ativo para encerrar.')
        return redirect('dashboard')

    if request.method == 'POST':
        energy_level = request.POST.get('energy_level')
        focus_level = request.POST.get('focus_level')
        mood_level = request.POST.get('mood_level')
        notes = request.POST.get('notes', '')

        try:
            active_fasting.end_time = timezone.now()
            if energy_level:
                active_fasting.energy_level = int(energy_level)
            if focus_level:
                active_fasting.focus_level = int(focus_level)
            if mood_level:
                active_fasting.mood_level = int(mood_level)
            if notes:
                active_fasting.notes = notes
            active_fasting.save()
            messages.success(request, f'Jejum encerrado! Duração: {active_fasting.duration_hours:.2f} horas')
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f'Erro ao encerrar jejum: {str(e)}')

    return render(request, 'fasting/end_fasting.html', {'active_fasting': active_fasting})


@login_required
def history_view(request):
    fastings = FastingRecord.objects.filter(user=request.user, end_time__isnull=False).order_by('-start_time')
    return render(request, 'fasting/history.html', {'fastings': fastings})


@login_required
def edit_fasting_view(request, pk):
    fasting = get_object_or_404(FastingRecord, pk=pk, user=request.user)

    if request.method == 'POST':
        form = FastingRecordForm(request.POST, instance=fasting)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Jejum atualizado com sucesso!')
                return redirect('history')
            except Exception as e:
                messages.error(request, f'Erro ao atualizar jejum: {str(e)}')
    else:
        form = FastingRecordForm(instance=fasting)

    return render(request, 'fasting/edit.html', {'form': form, 'fasting': fasting})


@login_required
def weight_view(request):
    if request.method == 'POST':
        form = WeightRecordForm(request.POST)
        if form.is_valid():
            weight_record = form.save(commit=False)
            weight_record.user = request.user
            try:
                weight_record.save()
                messages.success(request, 'Peso registrado com sucesso!')
                return redirect('weight')
            except Exception as e:
                messages.error(request, f'Erro ao registrar peso: {str(e)}')
    else:
        current_month = timezone.now().strftime('%Y-%m')
        form = WeightRecordForm(initial={'reference_month': current_month})

    weights = WeightRecord.objects.filter(user=request.user).order_by('-reference_month')
    return render(request, 'weight/weight.html', {'form': form, 'weights': weights})


def calculate_streak(user):
    today = timezone.now().date()
    streak = 0
    current_date = today

    while True:
        day_fastings = FastingRecord.objects.filter(
            user=user,
            start_time__date=current_date,
            end_time__isnull=False
        )

        total_hours = sum([f.duration_hours for f in day_fastings])

        if total_hours >= user.fasting_goal_hours:
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break

        if streak > 365:
            break

    return streak
