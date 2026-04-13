from django.shortcuts import render
from .models import Profile, Skill, Project, Certificate, Experience, Achievement


def home(request):
    """Portfolio homepage view"""
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    projects = Project.objects.all()
    experiences = Experience.objects.all()
    achievements = Achievement.objects.all()
    certificates = Certificate.objects.all()
    
    # Define custom category order (not alphabetical)
    category_order = ['Frontend', 'Backend', 'Database', 'Data', 'Tools']
    
    # Group skills by category
    skills_by_category = {}
    for skill in skills:
        skills_by_category.setdefault(skill.category, []).append(skill)
    
    # Sort by custom order
    sorted_skills = {}
    for category in category_order:
        if category in skills_by_category:
            sorted_skills[category] = skills_by_category[category]
    
    # Parse tech_stack for each project
    projects_with_tech = []
    for project in projects:
        project.tech_list = [tech.strip() for tech in project.tech_stack.split(',')]
        projects_with_tech.append(project)
    
    context = {
        'profile': profile,
        'skills_by_category': sorted_skills,
        'projects': projects_with_tech,
        'experiences': experiences,
        'achievements': achievements,
        'certificates': certificates,
    }
    return render(request, 'home.html', context)
