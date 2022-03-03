from datetime import datetime
from django.db import models
from django.dispatch import receiver
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.core.mail import send_mail as sm
import threading


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
    date_joined = models.DateField(default=datetime.now, blank=True)


@receiver(post_save, sender=Team)
def send_mail(sender, instance, created, **kwargs):
    if created:
        subject = 'Creado nuevo equipo'
        message = 'Se ha creado el equipo %s' % (instance.name)
        x = threading.Thread(target=send, args=(subject, message))
        x.start()


def send(subject, message):
    try:
        users = User.objects.filter(is_superuser=True)
        res = sm(
            subject=subject,
            message=message,
            from_email='team-management@gmail.com',
            recipient_list=list(map(lambda user: user.email, users)),
            fail_silently=True,
        )
        if res == 0:
            print("Mail not send")
    except NameError:
        print(NameError)
