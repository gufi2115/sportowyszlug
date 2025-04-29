from django.contrib import admin

from embed_video.admin import AdminVideoMixin

from .models import ProjectM, RanksM, ReviewM

class AdminVideo(AdminVideoMixin, admin.ModelAdmin):
    pass


admin.site.register(ProjectM, AdminVideo)
admin.site.register(ReviewM)
admin.site.register(RanksM)