from django.db import models
from django.dispatch import receiver
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Team(TimeStampedModel):
    name = models.CharField(max_length=50, null=False, blank=True)
    image = models.CharField(max_length=9000, null=False, blank=True)
    date_published = models.DateTimeField(
        auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(
        auto_now=True, verbose_name="date updated")
    members = models.ManyToManyField(
        User, through='Member', related_name='teams')

    def __str__(self):
        return self.name

class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date_joined = models.DateField()


@receiver(post_save, sender=Team)
def send_mail(sender, instance, created, **kwargs):
    if created:
        #Busar admins y notificar por email
        print(instance)
