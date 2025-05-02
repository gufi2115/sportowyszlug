from types import NoneType

from django.contrib.auth.decorators import login_required
from django.db.transaction import commit
from django.shortcuts import render, redirect

from users.models import ProfileM
from .models import ProjectM, RanksM, ReviewM
from .forms import ProjectForm, ReviewForm
from django.views.decorators.csrf import csrf_protect
from users.models import ProfileM
from .utils import ranksystem
from django.urls import reverse
from django.core.paginator import Paginator


def projects(request):
    projects = ProjectM.objects.all()
    p = Paginator(projects, 6)
    page_number = request.GET.get("page")
    if isinstance(page_number, NoneType):
        return redirect('/projects/?page=1')
    page_obj = p.get_page(page_number)
    page_list = []
    p_n = int(page_number)

    if p_n > p.num_pages:
        return redirect('/projects/?page=1')

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

    context = {'projects': projects, 'page_obj': page_obj, 'page_list': page_list}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = ProjectM.objects.get(id=str(pk))
    form = ReviewForm()
    owner_project = projectObj.owner_id
    profileObj = ProfileM.objects.get(id=owner_project)
    rankObj, created = RanksM.objects.get_or_create(owner_id=owner_project)

    if request.user.is_authenticated:
        review_owner = ProfileM.objects.get(user=request.user)
    else:
        review_owner = None
    review = ReviewM.objects.filter(project_id=pk).count()
    new_user_rank= ranksystem(owner_project)

    if review >= 3 and len(new_user_rank) > 0:
        new_user_rank = new_user_rank[0].split('_')
        user_rank_image = new_user_rank[0]
        user_rank_name = new_user_rank[1]
        RanksM.objects.filter(owner_id=owner_project).update(rank_image=user_rank_image, rank=user_rank_name)


    if request.method == 'POST':
        form= ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project_id = str(pk)
        review.owner = review_owner
        review.save()
        return redirect(f"/project/{pk}/")

    votes = ReviewM.objects.filter(project_id=pk).select_related('owner').order_by('-created_at')

    value = request.GET.get('filters')
    if value == 'up':
        votes = ReviewM.objects.filter(project_id=pk, value=value)

    elif value == 'down':
        votes = ReviewM.objects.filter(project_id=pk, value=value)



    context = {'project': projectObj, 'rankObj': rankObj, 'votes': votes, 'form': form, 'owner': profileObj}
    return render(request, 'projects/project.html', context)


@login_required
@csrf_protect
def create_project(request):
    form = ProjectForm()
    profile = ProfileM.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner_id = profile.id
            project.save()
            form.save_m2m()
            return redirect('/projects/?page=1')
        else:
            project_error = form.errors
            return render(request, 'projects/project_form.html', {'errors': project_error})

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required
def updateproject(request, pk):
    project = ProjectM.objects.get(id=pk)
    form = ProjectForm(instance=project)
    if not request.user.id == project.owner_id:
        return redirect(f'/project/{pk}/')

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect(f'/project/{pk}/')
        else:
            project_error = form.errors
            return render(request, 'projects/project_form.html', {'errors': project_error})
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required
def deleteproject(request, pk):
    project = ProjectM.objects.get(id=pk)

    if not request.user.id == project.owner_id:
        return redirect(f'/project/{pk}/')

    if request.method == 'POST':
        project.delete()
        return redirect('/projects/?page=1')

    context = {'project': project}
    return render(request, 'projects/delete-project.html', context)

