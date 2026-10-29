from django.core.management.base import BaseCommand
from portal.models import Company, Job, Announcement, AptitudeTest


class Command(BaseCommand):
    help = "Seed the database with demo companies, jobs, announcements and aptitude tests."

    def handle(self, *args, **options):
        companies_data = [
            ("Google", "PRODUCT", "Bangalore, India", 4.8, True, 1998, "1,80,000+", "https://google.com"),
            ("Microsoft", "PRODUCT", "Hyderabad, India", 4.6, True, 1975, "1,81,000+", "https://microsoft.com"),
            ("Infosys", "IT", "Pune, India", 4.3, True, 1981, "3,40,000+", "https://infosys.com"),
            ("TCS", "IT", "Chennai, India", 4.4, True, 1968, "6,00,000+", "https://tcs.com"),
            ("Wipro", "IT", "Bangalore, India", 4.2, True, 1945, "2,50,000+", "https://wipro.com"),
            ("Zoho", "PRODUCT", "Chennai, India", 4.1, True, 1996, "18,000+", "https://zoho.com"),
        ]

        companies = {}
        for name, industry, location, rating, featured, founded, employees, website in companies_data:
            company, _ = Company.objects.get_or_create(
                name=name,
                defaults=dict(
                    industry=industry, location=location, rating=rating,
                    is_featured=featured, founded_year=founded,
                    employee_count=employees, website=website,
                    about=f"{name} is a leading organization known for innovation, strong engineering culture, and excellent growth opportunities for fresh graduates and experienced professionals alike."
                )
            )
            companies[name] = company

        jobs_data = [
            ("Software Engineer", "Google", "Bangalore, India", "FULL_TIME", "2-4 Yrs", 12, 18, "Python, DSA, System Design"),
            ("Data Analyst", "Microsoft", "Hyderabad, India", "FULL_TIME", "1-3 Yrs", 8, 12, "SQL, Excel, Power BI"),
            ("Web Developer", "Infosys", "Pune, India", "FULL_TIME", "1-2 Yrs", 4, 7, "HTML, CSS, JavaScript, Django"),
            ("System Engineer", "TCS", "Chennai, India", "FULL_TIME", "2-3 Yrs", 6, 9, "Java, Linux, Networking"),
            ("Frontend Developer", "Zoho", "Chennai, India", "FULL_TIME", "1-3 Yrs", 6, 10, "React, JavaScript, CSS"),
            ("Cloud Support Associate", "Wipro", "Bangalore, India", "FULL_TIME", "0-2 Yrs", 4, 6, "AWS, Linux, Networking"),
        ]

        for title, company_name, location, job_type, exp, smin, smax, skills in jobs_data:
            Job.objects.get_or_create(
                title=title, company=companies[company_name],
                defaults=dict(
                    location=location, job_type=job_type, experience=exp,
                    salary_min=smin, salary_max=smax, skills=skills,
                    description=f"We are looking for a talented {title} to join our team and contribute to impactful projects.",
                )
            )

        announcements_data = [
            ("TCS Campus Drive 2026", "TCS is conducting a campus drive for the 2026 batch. Eligible students can apply.", True),
            ("Aptitude Test Schedule Released", "All aptitude tests for this month have been published. Check your dashboard.", False),
            ("Microsoft Hiring Challenge", "Participate in Microsoft Hiring Challenge and win exciting prizes.", False),
        ]
        for title, desc, important in announcements_data:
            Announcement.objects.get_or_create(title=title, defaults=dict(description=desc, is_important=important))

        tests_data = [
            ("Quantitative Aptitude", "QUANT", "MEDIUM", 20, 30),
            ("Verbal Ability", "VERBAL", "EASY", 20, 25),
            ("Logical Reasoning", "LOGICAL", "MEDIUM", 20, 30),
            ("Programming Basics", "CODING", "HARD", 20, 30),
        ]
        for title, category, difficulty, questions, duration in tests_data:
            AptitudeTest.objects.get_or_create(
                title=title, defaults=dict(category=category, difficulty=difficulty,
                                            total_questions=questions, duration_minutes=duration)
            )

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully!"))
