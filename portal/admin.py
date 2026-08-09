from django.contrib import admin
from .models import (
    Company, Job, Application, Announcement,
    AptitudeTest, ContactMessage, StudentProfile,Testimonial,Question, TestAttempt
)
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ('order', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option')


@admin.register(AptitudeTest)
class AptitudeTestAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'total_questions', 'duration_minutes', 'is_active')
    list_filter = ('category', 'difficulty', 'is_active')
    search_fields = ('title',)
    inlines = [QuestionInline]


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'score', 'total_questions', 'taken_on')
    list_filter = ('test',)
    search_fields = ('user__username', 'test__title')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'location', 'rating', 'is_featured', 'open_jobs_count')
    list_filter = ('industry', 'is_featured', 'location')
    search_fields = ('name', 'location')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_featured',)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'job_type', 'salary_min', 'salary_max', 'is_active', 'posted_on')
    list_filter = ('job_type', 'is_active', 'location')
    search_fields = ('title', 'company__name', 'skills')
    list_editable = ('is_active',)
    autocomplete_fields = ('company',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'role', 'company_name', 'is_active', 'display_order')
    list_filter = ('is_active',)
    search_fields = ('student_name', 'company_name')
    list_editable = ('is_active', 'display_order')
    
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'job', 'status', 'applied_on')
    list_filter = ('status', 'applied_on')
    search_fields = ('full_name', 'email', 'job__title')
    list_editable = ('status',)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_important', 'posted_on')
    list_filter = ('is_important',)
    search_fields = ('title',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'sent_on')
    list_filter = ('is_read', 'sent_on')
    search_fields = ('name', 'email', 'subject')
    list_editable = ('is_read',)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'college', 'course', 'graduation_year')
    search_fields = ('user__username', 'college')
