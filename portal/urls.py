from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('aptitude-tests/', views.aptitude_tests, name='aptitude_tests'),
    path('aptitude-tests/<int:test_id>/take/', views.take_test, name='take_test'),
    path('aptitude-tests/result/<int:attempt_id>/', views.test_result, name='test_result'), 
    path('about/', views.about, name='about'),
    path('companies/', views.companies, name='companies'),
    path('companies/<slug:slug>/', views.company_detail, name='company_detail'),
    path('opportunities/', views.opportunities, name='opportunities'),
    path('apply/<slug:slug>/', views.apply_job, name='apply_job'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('contact/', views.contact, name='contact'),
    path('announcements/', views.announcements, name='announcements'),
    path('aptitude-tests/', views.aptitude_tests, name='aptitude_tests'),
]
