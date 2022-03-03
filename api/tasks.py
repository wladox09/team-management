from background_task import background
from api.models import Team, send


@background()
def check_size_team():
    teams = Team.objects.all()
    for team in teams:
        if len(team.members.get_queryset()) > 10:
            subject = 'Equipo excedió limite'
            message = 'El equipo %s excedió el limite de 10' % (team.name)
            send(subject, message)
