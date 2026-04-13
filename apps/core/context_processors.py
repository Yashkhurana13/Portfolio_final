from .models import Profile


def global_profile(request):
    """Make profile available globally in all templates (navbar, footer, etc.)"""
    profile = Profile.objects.first()
    return {
        'global_profile': profile,
    }
