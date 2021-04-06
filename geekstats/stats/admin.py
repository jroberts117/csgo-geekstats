from django.contrib import admin
from .models import Geeks, Teams, TeamGames, TeamGeeks, TeamSeasons
from .geekmodels import Season
import sys

class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name','start_date','end_date')

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True

class TeamGamesAdmin(admin.ModelAdmin):
    list_display = ('gamedate','map','teama_wins','teamb_wins')
    date_hierarchy = 'gamedate'

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True

class TeamsAdmin(admin.ModelAdmin):
    list_display = ('name','idteams','description')

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True

class GeeksAdmin(admin.ModelAdmin):
    list_display = ('handle','idgeek','playerid','firstname','tier')

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True

class TeamGeeksAdmin(admin.ModelAdmin):
    list_display = ('idgeek','playerid','get_team','start_date','end_date')
    date_hierarchy = 'start_date'

    def get_team(self,obj):
        return obj.teamid.name
    
    def active(self, obj):
        return obj.is_active == 1

    get_team.short_description = 'Team'

    active.boolean = True    
# Register your models here.
admin.site.register(Geeks, GeeksAdmin)
admin.site.register(Teams, TeamsAdmin)
admin.site.register(TeamGames, TeamGamesAdmin)
admin.site.register(TeamGeeks, TeamGeeksAdmin)
admin.site.register(TeamSeasons, SeasonAdmin)
admin.site.register(Season)

