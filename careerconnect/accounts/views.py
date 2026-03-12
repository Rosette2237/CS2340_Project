from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CustomUserCreationForm, CustomErrorList, ProfileForm
from jobs.models import Job
from jobs.utils import calculate_match
from .models import Profile, SavedSearch
from message.models import Conversation, Message
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.
@login_required
def edit_profile(request):
    from jobs.geocoding import geocode_job
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            if profile.city or profile.state:
                lat, lng = geocode_job(profile.address, profile.city, profile.state)
                profile.location_lat = lat
                profile.location_long = lng
            else:
                profile.location_lat = None
                profile.location_long = None
            profile.save()
            if (not profile.is_recruiter) and profile.is_public and (not profile.notif_check):
                system = get_sys()

                for search in SavedSearch.objects.filter(is_applicable=True):
                    recruiter_profile = search.recruiter.profile

                    if profile_match(profile, search):
                        conversation, _ = Conversation.objects.get_or_create(
                            recruiter = recruiter_profile,
                            applicant = system
                        )

                        Message.objects.create(
                            conversation=conversation,
                            sender=system,
                            body=f'Hello, new candidate match found: {profile.display_name}. '
                        )

                Profile.objects.filter(id=profile.id).update(notif_check=True)
            return redirect('profile.edit')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})

def logout(request):
    auth_logout(request)
    return redirect('home.index')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            user = form.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.is_recruiter = form.cleaned_data.get('is_recruiter', False)
            profile.save()
            auth_login(request, user)
            if profile.is_recruiter:
                return redirect('jobs:create')
            return redirect('profile.edit')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html',  {'template_data': template_data})


@login_required
def search_candidates(request):
    if not getattr(request.user.profile, 'is_recruiter', False):
        return HttpResponseForbidden("Only recruiters can search for candidates.")

    candidates = Profile.objects.filter(is_recruiter=False, is_public=True)

    user_query = request.GET.get('user')
    skills_query = request.GET.get('skills')
    city_query = request.GET.get('city')
    state_query = request.GET.get('state')

    if user_query:
        candidates = candidates.filter(
            Q(user__username__icontains=user_query)
            | Q(user__first_name__icontains=user_query)
            | Q(user__last_name__icontains=user_query)
        )
    if skills_query:
        skills = [skill.strip() for skill in skills_query.split(",") if skill.strip()]
        for skill in skills:
            candidates = candidates.filter(skills__icontains=skill)
    if city_query:
        candidates = candidates.filter(city__icontains=city_query)
    if state_query:
        candidates = candidates.filter(state__icontains=state_query)

    recruiter_jobs = Job.objects.filter(recruiter=request.user)
    candidates_list = list(candidates)

    for candidate in candidates_list:
        candidate.recommendations = []
        if candidate.skills:
            for job in recruiter_jobs:
                percent_match = calculate_match(job.skills_required, candidate.skills)
                if percent_match >= 70:
                    candidate.recommendations.append({
                        'title': job.title,
                        'percent': percent_match,
                        'type': job.id
                    })

    candidates_list.sort(key=lambda x: len(x.recommendations), reverse=True)

    context = {
        'candidates': candidates_list,
        'values': request.GET
    }

    return render(request, 'accounts/candidate_search.html', context)

@login_required
def save_search(request):
    if request.method == 'POST':
        SavedSearch.objects.create(
            recruiter = request.user,
            skills = request.POST.get('skills', ''),
            city = request.POST.get('city', ''),
            state = request.POST.get('state', '')
        )
        return redirect('my_searches')

@login_required
def search_list(request):
    if not getattr(request.user.profile, 'is_recruiter', False):
        return HttpResponseForbidden("Only recruiters can search for candidates.")

    searches = SavedSearch.objects.filter(recruiter=request.user).order_by('-creation_date')


    context = {
        'searches': searches
    }

    return render(request, 'accounts/search_list.html', context)

@login_required
def delete_search(request, search_id):
    if request.method == 'POST':
        search = SavedSearch.objects.get(id=search_id, recruiter=request.user)
        search.delete()
        return redirect('my_searches')

@login_required
def applied_search(request, search_id):
    if request.method == 'POST':
        search = SavedSearch.objects.get(id=search_id, recruiter=request.user)
        search.is_applicable = not search.is_applicable
        search.save()
        return redirect('my_searches')

def get_sys():
    user, _ = User.objects.get_or_create(
        username="System",
        defaults={
            "email": "system@careerconnect.com",
            "is_staff": False,
            "is_superuser": False,
            "is_active": True,
        }
    )

    profile, _ = Profile.objects.get_or_create(
        user=user,
        defaults={
            "is_recruiter": True,
            "is_public": False,
        }
    )

    return profile

def profile_match(candidate, searches):
    candidate_skills = [skill.strip().lower() for skill in (candidate.skills or "").split(",") if skill.strip()]
    search_skills = [skill.strip().lower() for skill in (searches.skills or "").split(",") if skill.strip()]

    if search_skills:
        if not any(skill in candidate_skills for skill in search_skills):
            return False;

    if searches.city:
        if (candidate.city or "").strip().lower() != searches.city.strip().lower():
            return False

    if searches.state:
        if (candidate.state or "").strip().lower() != searches.state.strip().lower():
            return False

    return True
