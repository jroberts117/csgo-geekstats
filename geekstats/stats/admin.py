from django.contrib import admin
from .geekmodels import Season, TeamGeek, Geek, Maps
import sys

class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name','start_date','end_date','master_win')

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True

# Register your models here.
admin.site.register(Season)
admin.site.register(TeamGeek)
admin.site.register(Geek)
admin.site.register(Maps)
