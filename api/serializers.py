from dataclasses import fields
from rest_framework import serializers
from api.models import User
from api.models import Team
from api.models import Member


class UserSerializers(serializers.ModelSerializer):
    teams = serializers.SerializerMethodField()

    def get_teams(self, instance):
        rows = []
        a = instance.teams.get_queryset()
        for i in a:
            date_joined = i.member_set.get(
                team=i.id, user=instance.id).date_joined
            rows.append({'id': i.id, 'name': i.name,
                        'image': i.image, 'date_joined': date_joined})
        return rows

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'username', 'email', 'teams')


class MemberSerializers(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('team', 'user', 'date_joined')


class TeamSerializers(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    image = serializers.CharField()

    def get_members(self, instance):
        rows = []
        a = instance.members.get_queryset()
        for i in a:
            rows.append({'id': i.id, 'first_name': i.first_name,
                        'last_name': i.last_name, 'email': i.email, 'date_joined': i.date_joined})
        return rows

    class Meta:
        model = Team
        fields = ('id', 'name', 'image', 'members',)


class TeamInputSerializers(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'image',)
