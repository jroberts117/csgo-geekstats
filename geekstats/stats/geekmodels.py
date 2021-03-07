# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Action(models.Model):
    action_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100)
    player_points = models.IntegerField(blank=True, null=True)
    team_points = models.IntegerField(blank=True, null=True)
    team = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'action'
        app_label = 'geek'


class Assist(models.Model):
    assist_id = models.AutoField(primary_key=True)
    round = models.ForeignKey('MatchRound', models.DO_NOTHING)
    geek = models.ForeignKey('Geek', models.DO_NOTHING)
    killing_player = models.ForeignKey('Geek', models.DO_NOTHING, blank=True, null=True)
    is_tk_assist = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'assist'
        app_label = 'geek'


class Blind(models.Model):
    blind_id = models.AutoField(primary_key=True)
    round = models.ForeignKey('MatchRound', models.DO_NOTHING)
    blinding_player = models.ForeignKey('Geek', models.DO_NOTHING)
    blinded_player = models.ForeignKey('Geek', models.DO_NOTHING)
    is_team_blind = models.IntegerField()
    duration = models.DecimalField(max_digits=12, decimal_places=4)

    class Meta:
        managed = False
        db_table = 'blind'
        app_label = 'geek'


class Buy(models.Model):
    buy_id = models.AutoField(primary_key=True)
    round = models.ForeignKey('MatchRound', models.DO_NOTHING)
    geek = models.ForeignKey('Geek', models.DO_NOTHING)
    item = models.ForeignKey('Item', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'buy'
        app_label = 'geek'


class Death(models.Model):
    death_id = models.AutoField(primary_key=True)
    geek = models.ForeignKey('Geek', models.DO_NOTHING)
    round = models.ForeignKey('MatchRound', models.DO_NOTHING)
    killer = models.ForeignKey('Geek', models.DO_NOTHING, blank=True, null=True)
    pos_x = models.DecimalField(max_digits=12, decimal_places=4)
    pos_y = models.DecimalField(max_digits=12, decimal_places=4)
    pos_z = models.DecimalField(max_digits=12, decimal_places=4)
    pos_killer_x = models.DecimalField(max_digits=12, decimal_places=4)
    pos_killer_y = models.DecimalField(max_digits=12, decimal_places=4)
    pos_killer_z = models.DecimalField(max_digits=12, decimal_places=4)
    distance = models.DecimalField(max_digits=12, decimal_places=4)
    is_headshot = models.IntegerField()
    is_penetration = models.IntegerField()
    is_teamkill = models.IntegerField()
    item = models.ForeignKey('Item', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'death'
        app_label = 'geek'


class Frag(models.Model):
    frag_id = models.AutoField(primary_key=True)
    geek = models.ForeignKey('Geek', models.DO_NOTHING)
    round = models.ForeignKey('MatchRound', models.DO_NOTHING)
    victim = models.ForeignKey('Geek', models.DO_NOTHING)
    pos_x = models.DecimalField(max_digits=12, decimal_places=4)
    pos_y = models.DecimalField(max_digits=12, decimal_places=4)
    pos_z = models.DecimalField(max_digits=12, decimal_places=4)
    pos_victim_x = models.DecimalField(max_digits=12, decimal_places=4)
    pos_victim_y = models.DecimalField(max_digits=12, decimal_places=4)
    pos_victim_z = models.DecimalField(max_digits=12, decimal_places=4)
    distance = models.DecimalField(max_digits=12, decimal_places=4)
    is_headshot = models.IntegerField()
    is_penetration = models.IntegerField()
    is_teamkill = models.IntegerField()
    item = models.ForeignKey('Item', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'frag'
        app_label = 'geek'


class Geek(models.Model):
    geek_id = models.AutoField(primary_key=True)
    csgo_id = models.CharField(max_length=100)
    handle = models.CharField(max_length=250, blank=True, null=True)
    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    location = models.CharField(max_length=20, blank=True, null=True)
    occupation = models.CharField(max_length=250, blank=True, null=True)
    member_since = models.DateField(blank=True, null=True)
    tier = models.ForeignKey('Tier', models.DO_NOTHING, blank=True, null=True)
    generation = models.ForeignKey('Generation', models.DO_NOTHING, blank=True, null=True)
    is_member = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geek'
        app_label = 'geek'


class Generation(models.Model):
    generation_id = models.AutoField(primary_key=True)
    generation_name = models.CharField(max_length=250)
    gen_description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'generation'
        app_label = 'geek'


class GrenadeToss(models.Model):
    grenade_toss_id = models.AutoField(primary_key=True)
    round = models.ForeignKey('MatchRound', models.DO_NOTHING)
    geek = models.ForeignKey(Geek, models.DO_NOTHING)
    item = models.ForeignKey('Item', models.DO_NOTHING)
    pos_x = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    pos_y = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    pos_z = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grenade_toss'
        app_label = 'geek'


class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    decscription = models.CharField(max_length=1000)
    cost = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    sub_category = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'item'
        app_label = 'geek'


class MatchAward(models.Model):
    match_award_id = models.AutoField(primary_key=True)
    match = models.ForeignKey('SeasonMatch', models.DO_NOTHING)
    geek = models.ForeignKey(Geek, models.DO_NOTHING)
    award_name = models.CharField(max_length=1000)
    award_value = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    award_position = models.IntegerField(blank=True, null=True)
    score = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'match_award'
        app_label = 'geek'


class MatchRound(models.Model):
    round_id = models.AutoField(primary_key=True)
    match = models.ForeignKey('SeasonMatch', models.DO_NOTHING)
    ct_team = models.ForeignKey('Team', models.DO_NOTHING, blank=True, null=True)
    t_team = models.ForeignKey('Team', models.DO_NOTHING, blank=True, null=True)
    win_side = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'match_round'
        app_label = 'geek'


class PlayerEventAction(models.Model):
    player_event_action_id = models.AutoField(primary_key=True)
    event_time = models.DateTimeField(blank=True, null=True)
    round = models.ForeignKey(MatchRound, models.DO_NOTHING)
    geek = models.ForeignKey(Geek, models.DO_NOTHING)
    action = models.ForeignKey(Action, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'player_event_action'
        app_label = 'geek'


class Season(models.Model):
    season_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'season'
        app_label = 'geek'


class SeasonMatch(models.Model):
    match_id = models.AutoField(primary_key=True)
    match_date = models.DateTimeField()
    season = models.ForeignKey(Season, models.DO_NOTHING, blank=True, null=True)
    map = models.CharField(max_length=200)
    team_winner = models.ForeignKey('Team', models.DO_NOTHING, db_column='team_winner', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'season_match'
        app_label = 'geek'


class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    season = models.ForeignKey(Season, models.DO_NOTHING)
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=5000, blank=True, null=True)
    captain = models.ForeignKey(Geek, models.DO_NOTHING)
    co_captain = models.ForeignKey(Geek, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'team'
        app_label = 'geek'


class TeamEventAction(models.Model):
    team_event_action_id = models.AutoField(primary_key=True)
    event_time = models.DateTimeField(blank=True, null=True)
    round = models.ForeignKey(MatchRound, models.DO_NOTHING)
    team = models.ForeignKey(Team, models.DO_NOTHING, blank=True, null=True)
    action = models.ForeignKey(Action, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'team_event_action'
        app_label = 'geek'


class TeamGeek(models.Model):
    geek = models.OneToOneField(Geek, models.DO_NOTHING, primary_key=True)
    team = models.ForeignKey(Team, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'team_geek'
        unique_together = (('geek', 'team'),)
        app_label = 'geek'


class Tier(models.Model):
    tier_id = models.AutoField(primary_key=True)
    tier_name = models.CharField(max_length=250)
    tier_description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tier'
        app_label = 'geek'

class TiersData(models.Model):
    player = models.CharField(max_length=250)
    tier = models.CharField(max_length=250)
    matchdate = models.DateField()
    kills = models.IntegerField()
    deaths = models.IntegerField() 
    assists = models.IntegerField()
    kdr = models.DecimalField(max_digits=8, decimal_places=2)
    akdr = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'tiers_data'
        app_label = 'geek'
    

