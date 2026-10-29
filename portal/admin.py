from django.contrib import admin
from .models import (
    Company, Job, Application, Announcement,
    AptitudeTest, ContactMessage,Profile,
    AptitudeQuestion, AptitudeAttempt
)


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


@admin.register(AptitudeTest)
class AptitudeTestAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'total_questions', 'duration_minutes', 'is_active')
    list_filter = ('category', 'difficulty', 'is_active')
    search_fields = ('title',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'sent_on')
    list_filter = ('is_read', 'sent_on')
    search_fields = ('name', 'email', 'subject')
    list_editable = ('is_read',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'college', 'course', 'graduation_year')
    search_fields = ('user__username', 'college')

class AptitudeQuestionInline(admin.TabularInline):
    model = AptitudeQuestion
    extra = 1


class AptitudeTestAdminWithQuestions(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'difficulty',
        'total_questions', 'duration_minutes', 'is_active'
    )
    inlines = [AptitudeQuestionInline]


# Replace the existing AptitudeTest admin registration
admin.site.unregister(AptitudeTest)
admin.site.register(AptitudeTest, AptitudeTestAdminWithQuestions)


@admin.register(AptitudeAttempt)
class AptitudeAttemptAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'test', 'score', 'total_marks', 'attempted_on'
    )
    list_filter = ('test', 'attempted_on')
    search_fields = ('student__username', 'test__title')
    readonly_fields = (
        'student', 'test', 'score', 'total_marks',
        'answers', 'attempted_on'
    )
