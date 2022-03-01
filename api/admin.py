from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import Team
from .models import Member

admin.site.register(User, UserAdmin)
admin.site.register(Team)
admin.site.register(Member)