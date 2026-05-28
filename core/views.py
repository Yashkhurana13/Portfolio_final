from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.html import escape
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile, Skill, Project, Experience, Certification, Education, ContactMessage
from .forms import ContactForm
from django_ratelimit.decorators import ratelimit
import logging

logger = logging.getLogger(__name__)

@csrf_protect
@require_http_methods(["GET", "POST","HEAD"])
@ratelimit(key='ip', rate='3/m', method='POST', block=True)
@ratelimit(key='ip', rate='20/h', method='POST', block=True)
def portfolio_view(request):

    profile = Profile.objects.first()
    all_skills = Skill.objects.all()
    skills_by_category = {}
    for skill in all_skills:
        cat = skill.category
        if cat not in skills_by_category:
            skills_by_category[cat] = []
        skills_by_category[cat].append(skill)
    
    projects = Project.objects.all()
    experiences = Experience.objects.all()
    education = Education.objects.all()
    certifications = Certification.objects.all()

    if request.method == "POST":

        form = ContactForm(request.POST)
        if form.is_valid():
            # Sanitize inputs (additional layer beyond Django's built-in protection)
            name = escape(form.cleaned_data['name'])
            email = escape(form.cleaned_data['email'])
            message = escape(form.cleaned_data['message'])
            
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message
            )
            logger.info(f"Contact message received from {email}")

            # Send email notification to admin if configured
            admin_email = getattr(settings, 'ADMIN_EMAIL', '')
            if admin_email:
                try:
                    send_mail(
                        subject=f'[Portfolio] New message from {name}',
                        message=(
                            f'Name:    {name}\n'
                            f'Email:   {email}\n'
                            f'---\n\n'
                            f'{message}'
                        ),
                        from_email=settings.EMAIL_HOST_USER or 'noreply@portfolio.local',
                        recipient_list=[admin_email],
                        fail_silently=True,
                    )
                    logger.info(f"Notification email sent to {admin_email}")
                except Exception as exc:
                    logger.error(f"Failed to send notification email: {exc}")

            messages.success(request, "Message sent successfully!")
            return redirect('portfolio_home')  # Redirect to home, will scroll to contact via JS
        else:
            logger.warning(f"Invalid contact form submission from IP: {request.META.get('REMOTE_ADDR')}")
            messages.error(request, "Failed to send message. Please check the reCAPTCHA or your inputs.")
    else:
        form = ContactForm()

    context = {
        'profile': profile,
        'skills_by_category': skills_by_category,
        'projects': projects,
        'experiences': experiences,
        'education': education,
        'certifications': certifications,
        'form': form,
    }
    return render(request, 'core/portfolio.html', context)

from django.http import HttpResponseNotFound, FileResponse

@require_http_methods(["GET"])
@ratelimit(key='ip', rate='10/h', method='GET', block=True)
def download_resume(request):
    """Secure, rate-limited endpoint for resume downloads"""
    profile = Profile.objects.first()
    if profile and profile.resume:
        logger.info(f"Resume downloaded by IP: {request.META.get('REMOTE_ADDR')}")
        # Use FileResponse to force the browser to download the file instead of opening it inline
        return FileResponse(
            profile.resume.open('rb'),
            as_attachment=True,
            filename="Yash_Khurana_Resume.pdf"
        )
    
    logger.warning(f"Resume download requested but no resume found. IP: {request.META.get('REMOTE_ADDR')}")
    return HttpResponseNotFound(
        '<div style="text-align:center;font-family:sans-serif;margin-top:20vh;">'
        '<h1>404 Not Found</h1>'
        '<p>Resume is not available at this moment. Please check back later.</p>'
        '</div>'
    )

@require_http_methods(["GET"])
def privacy_policy(request):
    profile = Profile.objects.first()
    return render(request, 'core/privacy_policy.html', {'profile': profile})

@require_http_methods(["GET"])
def terms_and_conditions(request):
    profile = Profile.objects.first()
    return render(request, 'core/terms_conditions.html', {'profile': profile})
