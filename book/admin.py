from django.contrib import admin
from . models import Category,Book,RequestedBook,MaximumBookLimit

from django.contrib.auth.models import Group,Permission
from django.utils.translation import gettext_lazy as _

# Register your models here.
admin.site.register(Category) 
admin.site.register(MaximumBookLimit)
admin.site.register(Book)
admin.site.register(RequestedBook)
