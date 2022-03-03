from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import Team
from .models import Member


class MemberInline(admin.TabularInline):
    model = Member
    extra = 1
    exclude = ['date_joined']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['date_joined']
        else:
            return []


class TeamAdmin(admin.ModelAdmin):
    inlines = (MemberInline,)


class UserAdmin(admin.ModelAdmin):
    inlines = (MemberInline,)


admin.site.register(Team, TeamAdmin)
admin.site.register(User, UserAdmin)
