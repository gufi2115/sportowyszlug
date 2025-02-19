from django.shortcuts import render
from .models import ProjectsM, RanksM

def projects(request):
    projects_video = ProjectsM.objects.all()
    ranks = RanksM.objects.all()
    context = {'Videos': projects_video, 'ranks': ranks}
    return render(request, 'projects.html', context)
