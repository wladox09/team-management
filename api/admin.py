import base64
from django.utils.html import format_html
from django import forms
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


class TeamForm(forms.ModelForm):
    image = forms.FileField(required=False)

    def save(self, commit=True):
        if self.cleaned_data.get('image') is not None:
            data = base64.b64encode(self.cleaned_data['image'].file.read())
            self.instance.image = data
        return self.instance

    def save_m2m(self):
        pass

    class Meta:
        model = Team
        fields = ['name', 'image', ]


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_team']

    def image_team(self, obj):
        imageb64 = obj.image
        if type(imageb64) is bytes:
            return format_html('<img src="data:image/jpeg;base64,{}" width="100" height="100"/>'.format(imageb64.decode()))
        return "-"

    image_team.short_description = 'Image'

    form = TeamForm
    inlines = (MemberInline,)


class UserAdmin(admin.ModelAdmin):
    inlines = (MemberInline,)


admin.site.register(Team, TeamAdmin)
admin.site.register(User, UserAdmin)
