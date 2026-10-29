from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# ---------------------------------------------------------------------------
# COMPANY
# ---------------------------------------------------------------------------
class Company(models.Model):
    INDUSTRY_CHOICES = [
        ('IT', 'IT Services'),
        ('PRODUCT', 'Product Based'),
        ('FINANCE', 'Finance'),
        ('CONSULTING', 'Consulting'),
        ('CORE', 'Core Engineering'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    industry = models.CharField(max_length=20, choices=INDUSTRY_CHOICES, default='IT')
    location = models.CharField(max_length=150, default='India')
    website = models.URLField(blank=True)
    founded_year = models.PositiveIntegerField(blank=True, null=True)
    employee_count = models.CharField(max_length=50, blank=True, help_text="e.g. 1,81,000+")
    about = models.TextField(blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', 'name']
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('company_detail', kwargs={'slug': self.slug})

    @property
    def open_jobs_count(self):
        return self.jobs.filter(is_active=True).count()


# ---------------------------------------------------------------------------
# JOB
# ---------------------------------------------------------------------------
class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('FULL_TIME', 'Full Time'),
        ('PART_TIME', 'Part Time'),
        ('INTERNSHIP', 'Internship'),
        ('CONTRACT', 'Contract'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    location = models.CharField(max_length=150)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='FULL_TIME')
    experience = models.CharField(max_length=50, help_text="e.g. 2-4 Yrs")
    salary_min = models.PositiveIntegerField(help_text="LPA, e.g. 6")
    salary_max = models.PositiveIntegerField(help_text="LPA, e.g. 12")
    skills = models.CharField(max_length=300, help_text="Comma separated, e.g. Python, Django, SQL")
    eligibility = models.CharField(max_length=300, default="B.Tech / B.E graduates, 60% and above")
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    posted_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-posted_on']

    def __str__(self):
        return f"{self.title} - {self.company.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(f"{self.title}-{self.company.name}-{Job.objects.count()+1}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('apply_job', kwargs={'slug': self.slug})

    @property
    def skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]

    @property
    def package_display(self):
        return f"₹ {self.salary_min} - {self.salary_max} LPA"


# ---------------------------------------------------------------------------
# APPLICATION
# ---------------------------------------------------------------------------
class Application(models.Model):
    STATUS_CHOICES = [
        ('APPLIED', 'Applied'),
        ('SHORTLISTED', 'Shortlisted'),
        ('INTERVIEW', 'Interview Scheduled'),
        ('SELECTED', 'Selected'),
        ('REJECTED', 'Rejected'),
    ]

    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPLIED')
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-applied_on']
        unique_together = ('applicant', 'job')

    def __str__(self):
        return f"{self.full_name} -> {self.job.title}"


# ---------------------------------------------------------------------------
# ANNOUNCEMENT
# ---------------------------------------------------------------------------
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_important = models.BooleanField(default=False)
    posted_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-posted_on']

    def __str__(self):
        return self.title


# ---------------------------------------------------------------------------
# APTITUDE TEST
# ---------------------------------------------------------------------------
class AptitudeTest(models.Model):
    CATEGORY_CHOICES = [
        ('QUANT', 'Quantitative Aptitude'),
        ('VERBAL', 'Verbal Ability'),
        ('LOGICAL', 'Logical Reasoning'),
        ('CODING', 'Programming Basics'),
    ]
    DIFFICULTY_CHOICES = [
        ('EASY', 'Easy'),
        ('MEDIUM', 'Medium'),
        ('HARD', 'Hard'),
    ]

    title = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='MEDIUM')
    total_questions = models.PositiveIntegerField(default=20)
    duration_minutes = models.PositiveIntegerField(default=30)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category']

    def __str__(self):
        return self.title


# APTITUDE QUESTIONS
class AptitudeQuestion(models.Model):
    OPTION_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]

    test = models.ForeignKey(
        AptitudeTest,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(
        max_length=1,
        choices=OPTION_CHOICES
    )

    def __str__(self):
        return self.question_text[:70]


# STUDENT TEST RESULTS
class AptitudeAttempt(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='aptitude_attempts'
    )
    test = models.ForeignKey(
        AptitudeTest,
        on_delete=models.CASCADE,
        related_name='attempts'
    )
    score = models.PositiveIntegerField(default=0)
    total_marks = models.PositiveIntegerField(default=0)
    answers = models.JSONField(default=dict, blank=True)
    attempted_on = models.DateTimeField(auto_now_add=True)

    @property
    def percentage(self):
        if self.total_marks == 0:
            return 0
        return round((self.score / self.total_marks) * 100, 2)

    def __str__(self):
        return f"{self.student.username} - {self.test.title}"

# ---------------------------------------------------------------------------
# CONTACT MESSAGE
# ---------------------------------------------------------------------------
class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    sent_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent_on']

    def __str__(self):
        return f"{self.name} - {self.subject}"


# ---------------------------------------------------------------------------
# STUDENT PROFILE (extends User for dashboard info)
# ---------------------------------------------------------------------------
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    phone = models.CharField(max_length=15, blank=True)
    graduation_year = models.PositiveIntegerField(
        null=True, blank=True
    )
    college = models.CharField(max_length=200, blank=True)
    course = models.CharField(max_length=100, blank=True)
    resume = models.FileField(
        upload_to="resumes/", blank=True, null=True
    )
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )

    def __str__(self):
        return self.user.username