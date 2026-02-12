from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile

# Create your views here.
#@login_required
def edit_profile(request):
    #profile, created = Profile.objects.get_or_create(user=request.user)
    profile = Profile.objects.first()
    
    if not profile:
        profile = Profile.objects.create(headline="My New Profile")

    if request.method == 'POST':
        profile.headline = request.POST.get('headline')
        profile.skills = request.POST.get('skills')
        profile.education = request.POST.get('education')
        profile.work_experience = request.POST.get('work_experience')
        profile.linkedin_link = request.POST.get('linkedin_link')
        profile.portfolio_link = request.POST.get('portfolio_link')
        profile.save()

        return redirect('edit_profile')

    return render(request, 'accounts/profile.html', {'profile': profile})