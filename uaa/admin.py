from django.contrib import admin
from . models import REgisterdMember,User,DailyTip

from django.contrib.auth.models import Group,Permission
from django.utils.translation import gettext_lazy as _

# Register your models here.
admin.site.register(REgisterdMember)
admin.site.register(User)
admin.site.register(DailyTip)
admin.site.register(Permission)

admin.site.site_url = "/login_url"