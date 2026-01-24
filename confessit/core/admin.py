from django.contrib import admin
from django.http import Http404
from .models import Confession,Comment
# Register your models here.
class AdminClass(admin.AdminSite):
    def has_permission(self, request):
        return request.user.is_active and request.user.is_superuser and request.user.is_authenticated

    def login(self, request, extra_context=None):
        if not request.user.is_superuser:
            raise Http404
        return super().login(request, extra_context=extra_context)
    
admin_site = AdminClass()
admin_site.register(Comment)
admin_site.register(Confession)
