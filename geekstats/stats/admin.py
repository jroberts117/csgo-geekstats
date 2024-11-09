from django.contrib import admin
from .geekmodels import Season, TeamGeek, Geek, Maps, Team
import sys

class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name','start_date','end_date','master_win')

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True

class TeamGeekModelAdmin(admin.ModelAdmin):
    list_display = ('geek', 'team', 'tier', 'event_date')
    list_filter = ('team', 'geek')  # Using default filter options

class TeamGeekInline(admin.TabularInline):
    model = TeamGeek
    extra = 1

class TeamModelAdmin(admin.ModelAdmin):
    list_display = ('team_id', 'season', 'name', 'description', 'captain', 'co_captain')
    list_filter = ('season', 'captain')  # Using default filter options
    inlines = [TeamGeekInline]

# Register your models here.
admin.site.register(Season)
admin.site.register(TeamGeek)
admin.site.register(Team, TeamModelAdmin)
admin.site.register(Geek)
admin.site.register(Maps)
