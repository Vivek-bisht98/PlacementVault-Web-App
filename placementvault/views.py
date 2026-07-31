from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ExperienceForm, RegisterForm, ROLE_CHOICES, ScheduleForm
from .models import Experience, Schedule


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created. Welcome to PlacementVault.")
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    today = timezone.localdate()
    context = {
        'schedule_count': Schedule.objects.filter(user=request.user).count(),
        'experience_count': Experience.objects.filter(user=request.user).count(),
        'upcoming_schedules': Schedule.objects.filter(user=request.user, date__gte=today)[:5],
    }
    return render(request, 'dashboard.html', context)


# ---------------------------------------------------------------------------
# Schedule CRUD
# Every lookup below filters by user=request.user, not just pk. That means a
# user can never view, edit, or delete another user's row even if they guess
# or manually edit the URL - the ownership check happens at the query level,
# not just via the login_required decorator.
# ---------------------------------------------------------------------------

@login_required
def schedule_list(request):
    schedules = Schedule.objects.filter(user=request.user)
    return render(request, 'schedule_list.html', {'schedules': schedules})


@login_required
def schedule_add(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.user = request.user
            schedule.save()
            messages.success(request, "Interview scheduled.")
            return redirect('schedule_list')
    else:
        form = ScheduleForm()
    return render(request, 'schedule_form.html', {
        'form': form, 'role_choices': ROLE_CHOICES, 'page_title': 'Add Schedule',
    })


@login_required
def schedule_edit(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request, "Schedule updated.")
            return redirect('schedule_list')
    else:
        form = ScheduleForm(instance=schedule)
    return render(request, 'schedule_form.html', {
        'form': form, 'role_choices': ROLE_CHOICES, 'page_title': 'Edit Schedule',
    })


@login_required
def schedule_delete(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk, user=request.user)
    if request.method == 'POST':
        schedule.delete()
        messages.success(request, "Schedule deleted.")
        return redirect('schedule_list')
    return render(request, 'confirm_delete.html', {
        'object_label': str(schedule), 'cancel_url_name': 'schedule_list',
    })


# ---------------------------------------------------------------------------
# Experience CRUD (same ownership-check pattern as Schedule above)
# ---------------------------------------------------------------------------

@login_required
def experience_list(request):
    experiences = Experience.objects.filter(user=request.user)
    return render(request, 'experience_list.html', {'experiences': experiences})


@login_required
def experience_add(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            experience.save()
            messages.success(request, "Experience published.")
            return redirect('experience_list')
    else:
        form = ExperienceForm()
    return render(request, 'experience_form.html', {
        'form': form, 'role_choices': ROLE_CHOICES, 'page_title': 'Publish Experience',
    })


@login_required
def experience_edit(request, pk):
    experience = get_object_or_404(Experience, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            messages.success(request, "Experience updated.")
            return redirect('experience_list')
    else:
        form = ExperienceForm(instance=experience)
    return render(request, 'experience_form.html', {
        'form': form, 'role_choices': ROLE_CHOICES, 'page_title': 'Edit Experience',
    })


@login_required
def experience_delete(request, pk):
    experience = get_object_or_404(Experience, pk=pk, user=request.user)
    if request.method == 'POST':
        experience.delete()
        messages.success(request, "Experience deleted.")
        return redirect('experience_list')
    return render(request, 'confirm_delete.html', {
        'object_label': str(experience), 'cancel_url_name': 'experience_list',
    })


# ---------------------------------------------------------------------------
# Search flow: Company -> Role -> Round -> Experiences.
# Each step reads the previous step's choice from the query string and
# narrows the next list of distinct values. Experiences are visible to
# every logged-in user here (not filtered by owner) since the whole point
# of this screen is reading what OTHER students shared.
# ---------------------------------------------------------------------------

@login_required
def search_company(request):
    companies = (
        Experience.objects.order_by('company_name')
        .values_list('company_name', flat=True).distinct()
    )
    return render(request, 'search_company.html', {'companies': companies})


@login_required
def search_roles(request):
    company = request.GET.get('company', '')
    roles = (
        Experience.objects.filter(company_name=company)
        .order_by('role').values_list('role', flat=True).distinct()
    )
    return render(request, 'search_roles.html', {'company': company, 'roles': roles})


@login_required
def search_rounds(request):
    company = request.GET.get('company', '')
    role = request.GET.get('role', '')
    rounds = (
        Experience.objects.filter(company_name=company, role=role)
        .order_by('interview_round').values_list('interview_round', flat=True).distinct()
    )
    return render(request, 'search_rounds.html', {
        'company': company, 'role': role, 'rounds': rounds,
    })


@login_required
def search_experiences(request):
    company = request.GET.get('company', '')
    role = request.GET.get('role', '')
    interview_round = request.GET.get('round', '')
    experiences = (
        Experience.objects
        .filter(company_name=company, role=role, interview_round=interview_round)
        .select_related('user')
    )
    return render(request, 'search_experiences.html', {
        'company': company, 'role': role, 'round': interview_round,
        'experiences': experiences,
    })
