from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone

from .models import (
    Company, Job, Application, Announcement,
    AptitudeTest, ContactMessage, StudentProfile,Testimonial,Question, TestAttempt
)
from .forms import RegisterForm, ApplicationForm, ContactForm, StudentProfileForm


# ---------------------------------------------------------------------------
# HOME
# ---------------------------------------------------------------------------
def home(request):
    context = {
        'testimonials': Testimonial.objects.filter(is_active=True)[:6],
        'total_companies': Company.objects.count(),
        'total_jobs': Job.objects.filter(is_active=True).count(),
        'placed_students': Application.objects.filter(status='SELECTED').count() or 850,
        'placement_rate': 95,
        'featured_companies': Company.objects.filter(is_featured=True)[:6] or Company.objects.all()[:6],
        'latest_jobs': Job.objects.filter(is_active=True).select_related('company')[:4],
        'announcements': Announcement.objects.all()[:3],
    }
    return render(request, 'portal/home.html', context)


# ---------------------------------------------------------------------------
# ABOUT
# ---------------------------------------------------------------------------
def about(request):
    context = {
        'total_companies': Company.objects.count(),
        'total_jobs': Job.objects.filter(is_active=True).count(),
        'placed_students': Application.objects.filter(status='SELECTED').count() or 850,
        'placement_rate': 95,
    }
    return render(request, 'portal/about.html', context)


# ---------------------------------------------------------------------------
# COMPANIES (list, search, filter)
# ---------------------------------------------------------------------------
def companies(request):
    qs = Company.objects.all()
    query = request.GET.get('q', '').strip()
    industry = request.GET.get('industry', '').strip()

    if query:
        qs = qs.filter(Q(name__icontains=query) | Q(location__icontains=query))
    if industry:
        qs = qs.filter(industry=industry)

    paginator = Paginator(qs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'industries': Company.INDUSTRY_CHOICES,
        'query': query,
        'selected_industry': industry,
    }
    return render(request, 'portal/companies.html', context)


def company_detail(request, slug):
    company = get_object_or_404(Company, slug=slug)
    jobs = company.jobs.filter(is_active=True)
    return render(request, 'portal/company_detail.html', {'company': company, 'jobs': jobs})


# ---------------------------------------------------------------------------
# JOB OPPORTUNITIES (search, filter, pagination)
# ---------------------------------------------------------------------------
def opportunities(request):
    qs = Job.objects.filter(is_active=True).select_related('company')

    query = request.GET.get('q', '').strip()
    location = request.GET.get('location', '').strip()
    job_type = request.GET.get('job_type', '').strip()
    experience = request.GET.get('experience', '').strip()

    if query:
        qs = qs.filter(Q(title__icontains=query) | Q(skills__icontains=query) | Q(company__name__icontains=query))
    if location:
        qs = qs.filter(location__icontains=location)
    if job_type:
        qs = qs.filter(job_type=job_type)
    if experience:
        qs = qs.filter(experience__icontains=experience)

    paginator = Paginator(qs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'job_types': Job.JOB_TYPE_CHOICES,
        'query': query,
        'location': location,
        'job_type': job_type,
    }
    return render(request, 'portal/opportunities.html', context)


# ---------------------------------------------------------------------------
# APPLY JOB
# ---------------------------------------------------------------------------
@login_required
def apply_job(request, slug):
    job = get_object_or_404(Job, slug=slug, is_active=True)
    already_applied = Application.objects.filter(applicant=request.user, job=job).exists()

    if request.method == 'POST' and not already_applied:
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.job = job
            application.save()
            messages.success(request, "Your application has been submitted successfully!")
            return redirect('apply_job', slug=slug)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        initial = {
            'full_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        }
        form = ApplicationForm(initial=initial)

    context = {'job': job, 'form': form, 'already_applied': already_applied}
    return render(request, 'portal/apply_job.html', context)


# ---------------------------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------------------------
@login_required
def dashboard(request):
    applications = Application.objects.filter(applicant=request.user).select_related('job', 'job__company')
    context = {
        'applications': applications[:5],
        'total_applications': applications.count(),
        'shortlisted_count': applications.filter(status='SHORTLISTED').count(),
        'selected_count': applications.filter(status='SELECTED').count(),
        'upcoming_tests': AptitudeTest.objects.filter(is_active=True)[:3],
        'announcements': Announcement.objects.all()[:4],
        'latest_jobs': Job.objects.filter(is_active=True)[:4],
    }
    return render(request, 'portal/dashboard.html', context)


# ---------------------------------------------------------------------------
# AUTH: LOGIN / LOGOUT / REGISTER
# ---------------------------------------------------------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'portal/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            StudentProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Account created successfully! Welcome to PlacePro.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'portal/register.html', {'form': form})


# ---------------------------------------------------------------------------
# CONTACT
# ---------------------------------------------------------------------------
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks for reaching out! We'll get back to you soon.")
            return redirect('contact')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()
    return render(request, 'portal/contact.html', {'form': form})


# ---------------------------------------------------------------------------
# ANNOUNCEMENTS
# ---------------------------------------------------------------------------
def announcements(request):
    all_announcements = Announcement.objects.all()
    return render(request, 'portal/announcements.html', {'announcements': all_announcements})


# ---------------------------------------------------------------------------
# APTITUDE TESTS
# ---------------------------------------------------------------------------
def aptitude_tests(request):
    tests = AptitudeTest.objects.filter(is_active=True)
    return render(request, 'portal/aptitude_tests.html', {'tests': tests})


# ---------------------------------------------------------------------------
# PROFILE
# ---------------------------------------------------------------------------
@login_required
def profile_view(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = StudentProfileForm(instance=profile)
    return render(request, 'portal/profile.html', {'form': form, 'profile': profile})


# ---------------------------------------------------------------------------
# CUSTOM 404
# ---------------------------------------------------------------------------
def custom_404(request, exception=None):
    return render(request, 'portal/404.html', status=404)
@login_required
def take_test(request, test_id):
    test = get_object_or_404(AptitudeTest, id=test_id, is_active=True)
    questions = test.questions.all()

    if request.method == 'POST':
        score = 0
        for question in questions:
            selected = request.POST.get(f'question_{question.id}')
            if selected == question.correct_option:
                score += 1

        attempt = TestAttempt.objects.create(
            user=request.user,
            test=test,
            score=score,
            total_questions=questions.count(),
        )
        messages.success(request, "Test submitted successfully!")
        return redirect('test_result', attempt_id=attempt.id)

    context = {'test': test, 'questions': questions}
    return render(request, 'portal/take_test.html', context)


@login_required
def test_result(request, attempt_id):
    attempt = get_object_or_404(TestAttempt, id=attempt_id, user=request.user)
    return render(request, 'portal/test_result.html', {'attempt': attempt})
