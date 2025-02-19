from django.contrib import admin

from embed_video.admin import AdminVideoMixin

from .models import ProjectsM, RanksM, ReviewM

class AdminVideo(AdminVideoMixin, admin.ModelAdmin):
    pass


admin.site.register(ProjectsM, AdminVideo)
admin.site.register(ReviewM)
admin.site.register(RanksM)