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
@require_http_methods(["GET", "POST"])
@ratelimit(key='ip', rate='5/m', method='POST', block=False)
@ratelimit(key='ip', rate='20/h', method='POST', block=False)
def portfolio_view(request):
    was_limited = getattr(request, 'limited', False)

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
        if was_limited:
            logger.warning(f"Rate limit exceeded from IP: {request.META.get('REMOTE_ADDR')}")
            messages.error(request, "You are sending messages too quickly. Please try again later.")
            return redirect('portfolio_home')

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


from django.http import JsonResponse

@csrf_protect
@require_http_methods(["POST"])
def update_profile_view(request):
    profile = Profile.objects.first()
    if not profile:
        profile = Profile.objects.create(name="Yash Khurana")
        
    profile.name = escape(request.POST.get('name', profile.name))
    profile.available_badge_text = escape(request.POST.get('available_badge_text', profile.available_badge_text))
    profile.typewriter_words = escape(request.POST.get('typewriter_words', profile.typewriter_words))
    profile.card_1_title = escape(request.POST.get('card_1_title', profile.card_1_title))
    profile.card_1_text = escape(request.POST.get('card_1_text', profile.card_1_text))
    profile.card_2_title = escape(request.POST.get('card_2_title', profile.card_2_title))
    profile.card_2_text = escape(request.POST.get('card_2_text', profile.card_2_text))
    profile.card_3_title = escape(request.POST.get('card_3_title', profile.card_3_title))
    profile.card_3_text = escape(request.POST.get('card_3_text', profile.card_3_text))
    profile.save()
    
    return JsonResponse({
        'status': 'success',
        'name': profile.name,
        'available_badge_text': profile.available_badge_text,
        'typewriter_words': profile.typewriter_words,
        'card_1_title': profile.card_1_title,
        'card_1_text': profile.card_1_text,
        'card_2_title': profile.card_2_title,
        'card_2_text': profile.card_2_text,
        'card_3_title': profile.card_3_title,
        'card_3_text': profile.card_3_text,
    })
