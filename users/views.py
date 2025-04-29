from email.policy import default
from types import NoneType
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from projects.forms import ProjectForm
from projects.models import ProjectM, RanksM
from projects.utils import time_for_verification
from projects.views import project
from .models import ProfileM
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import requires_csrf_token
from .forms import UserForms, ProfileForms
from django.core.paginator import Paginator
from .signals import verifyEmail, verification_code
from django.contrib.auth.decorators import login_required
import datetime
import pytz
# Create your views here.

@requires_csrf_token
def user_login(request):
    previous_url = request.META.get('HTTP_REFERER')
    previous_page = request.session.get('previous_page', [])

    if len(previous_page) > 1:
        previous_page.pop(0)


    if not 'login' in previous_url:
        previous_page.append(previous_url)
        request.session["previous_page"] = previous_page


    if request.user.is_authenticated:
        return redirect('/projects/?page=1')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if previous_url:
                previous_page = previous_page[-1]
                return redirect(previous_page)
            else:
                return redirect('/projects/?page=1')
        else:
            login_error = 'Username or Password are not the same'
            return render(request, 'users/sing_up.html', {'errors': login_error})
    return render(request, 'users/sing_up.html')


def user_logout(request):

    if request.method == 'POST':
        logout(request)
        return redirect('/projects/?page=1')

    return render(request, 'users/logout.html')


def create_user(request):
    form = UserForms()

    if request.user.is_authenticated:
        return redirect('/projects/?page=1')

    if request.method == 'POST':
        form = UserForms(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_created = datetime.datetime.now()
            user.username = user.username.lower()
            email = user.email
            subject, message, sender, receiver = verifyEmail(email)
            send_mail(subject,
                      message,
                      sender,
                      receiver,
                      fail_silently=False)
            user.save()
            ProfileM.objects.create(user_id=user.id, verification_code=verification_code[0], created=user_created)
            login(request, user)
            return redirect('/create-profile/')
        else:
            valid_error = form.errors
            return render(request, 'users/create-user.html', {'form':form, 'errors':valid_error})
    context = {'form': form}
    return render(request, 'users/create-user.html', context)


@login_required
def create_profile(request):
    user_id = request.user.id
    profileObj = ProfileM.objects.get(user_id=user_id)
    code = profileObj.verification_code
    code_from_user = profileObj.verification_code_from_user
    user_email = request.user.email
    form = ProfileForms(instance=profileObj)
    time = time_for_verification(profileObj)

    if time < datetime.timedelta(0) and code != code_from_user:
        user = request.user
        user.delete()




    if request.method == 'POST':
        form = ProfileForms(request.POST, request.FILES, instance=profileObj)
        user_code = request.POST.get('verification_code')
        if form.is_valid():
            profile = form.save(commit=False)
            if user_code == code:
                profile.email = user_email
                profile.verification_code_from_user = user_code
                profile.save()
                return redirect('/projects/?page=1')
            elif isinstance(user_code, NoneType):
                verification_error = "Verification code is incorrect"
                return render(request, 'users/create-profile.html', {'form': form, 'errors': verification_error})
            else:
                verification_error = "Verification code is incorrect"
                return render(request, 'users/create-profile.html', {'form': form, 'errors': verification_error})
        return redirect('/projects/?page=1')

    context = {'form': form, 'time': time}
    return render(request, 'users/create-profile.html', context)


def profiles(request):
    profiles = ProfileM.objects.all()
    p = Paginator(profiles, 6)
    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)
    page_list = []
    if isinstance(page_number, NoneType):
        return redirect('/profiles/?page=1')
    p_n = int(page_number)

    if p_n > p.num_pages:
        return redirect('/profiles/?page=1')

    if p_n == 1 and p_n + 2 <= p.num_pages:
        page_list += p_n, p_n + 1, p_n + 2
    elif p_n == 1 and p_n + 1 == p.num_pages:
        page_list += p_n, p_n + 1

    if p_n == p.num_pages and p_n - 2 >= 1:
        page_list += p_n - 2, p_n - 1, p_n

    elif p_n == p.num_pages and p_n - 1 == 1:
        page_list += p_n - 1, p_n

    if p_n > 1 and p_n + 1 <= p.num_pages:
        page_list += p_n - 1, p_n, p_n + 1

    context = {'profiles': profiles, 'page_obj': page_obj, 'page_list': page_list}
    return render(request, 'users/profiles.html', context)


def profile(request, pk):
    profile = ProfileM.objects.get(id=pk)
    projectsObj = ProjectM.objects.filter(owner_id=pk)
    rankObj, created = RanksM.objects.get_or_create(owner_id=profile.id)
    context = {'profile': profile, 'projects': projectsObj, 'rank': rankObj}
    return render(request, 'users/profile.html', context)