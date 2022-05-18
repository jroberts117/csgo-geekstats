# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'

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
        db_tablespace = 'geek'


class Assist(models.Model):
    assist_id = models.AutoField(primary_key=True)
    round = models.ForeignKey('MatchRound', models.DO_NOTHING, related_name='assists')
    geek = models.ForeignKey('Geek', models.DO_NOTHING)
    killing_player = models.ForeignKey('Geek', models.DO_NOTHING, blank=True, null=True, related_name="assist_kill")
    is_tk_assist = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'assist'
        db_tablespace = 'geek'

class AwardCategory(models.Model):
    award_category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=1000)
    category_description = models.CharField(max_length=1000)
    category_color = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'award_category'
        db_tablespace = 'geek'


class Blind(models.Model):
    blind_id = models.AutoField(primary_key=True)
    round = models.ForeignKey('MatchRound', models.DO_NOTHING)
    blinding_player = models.ForeignKey('Geek', models.DO_NOTHING)
    blinded_player = models.ForeignKey('Geek', models.DO_NOTHING, related_name="blindee")
    is_team_blind = models.IntegerField()
    duration = models.DecimalField(max_digits=12, decimal_places=4)

    class Meta:
        managed = False
        db_table = 'blind'
        db_tablespace = 'geek'


class Buy(models.Model):
    buy_id = models.AutoField(primary_key=True)
    round = models.ForeignKey('MatchRound', models.DO_NOTHING, related_name='buys')
    geek = models.ForeignKey('Geek', models.DO_NOTHING)
    item = models.ForeignKey('Item', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'buy'
        db_tablespace = 'geek'


class Death(models.Model):
    death_id = models.AutoField(primary_key=True)
    geek = models.ForeignKey('Geek', models.DO_NOTHING)
    round = models.ForeignKey('MatchRound', models.DO_NOTHING, related_name='deaths')
    killer = models.ForeignKey('Geek', models.DO_NOTHING, blank=True, null=True, related_name="killer")
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
        db_tablespace = 'geek'


class Frag(models.Model):
    frag_id = models.AutoField(primary_key=True)
    geek = models.ForeignKey('Geek', models.DO_NOTHING)
    round = models.ForeignKey('MatchRound', models.DO_NOTHING, related_name='frags')
    victim = models.ForeignKey('Geek', models.DO_NOTHING, related_name="victim")
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
        db_tablespace = 'geek'


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
    valid_sent_date = models.DateField(blank=True, null=True)
    validated = models.IntegerField(blank=True, null=True)
    userid = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True) 
    geek_code = models.CharField(max_length=250, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'geek'
        db_tablespace = 'geek'

class GeekfestAward(models.Model):
    geekfest_award_id = models.AutoField(primary_key=True)
    award_name = models.CharField(max_length=1000)
    award_title = models.CharField(max_length=1000)
    award_description = models.CharField(max_length=1000, blank=True, null=True)
    award_image_path = models.CharField(max_length=1000, blank=True, null=True)
    award_category = models.ForeignKey(AwardCategory, models.DO_NOTHING)
    award_query = models.CharField(max_length=10000)
    award_query_type = models.CharField(max_length=100)
    award_value_type = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'geekfest_award'
        db_tablespace = 'geek'


class GeekfestMatchAward(models.Model):
    geekfest_match_award_id = models.AutoField(primary_key=True)
    match = models.ForeignKey('SeasonMatch', models.DO_NOTHING)
    geekfest_award = models.ForeignKey(GeekfestAward, models.DO_NOTHING)
    geek = models.ForeignKey(Geek, models.DO_NOTHING)
    award_rank = models.IntegerField()
    award_value = models.DecimalField(max_digits=12, decimal_places=4)

    class Meta:
        managed = False
        db_table = 'geekfest_match_award'
        db_tablespace = 'geek'


class Generation(models.Model):
    generation_id = models.AutoField(primary_key=True)
    generation_name = models.CharField(max_length=250)
    gen_description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'generation'
        db_tablespace = 'geek'


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
        db_tablespace = 'geek'


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
        db_tablespace = 'geek'


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
        db_tablespace = 'geek'


class MatchRound(models.Model):
    round_id = models.AutoField(primary_key=True)
    match = models.ForeignKey('SeasonMatch', models.DO_NOTHING, related_name='rounds')
    ct_team = models.ForeignKey('Team', models.DO_NOTHING, blank=True, null=True, related_name="ct_teams")
    t_team = models.ForeignKey('Team', models.DO_NOTHING, blank=True, null=True, related_name="t_teams")
    win_side = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'match_round'
        db_tablespace = 'geek'


class PlayerEventAction(models.Model):
    player_event_action_id = models.AutoField(primary_key=True)
    event_time = models.DateTimeField(blank=True, null=True)
    round = models.ForeignKey(MatchRound, models.DO_NOTHING)
    geek = models.ForeignKey(Geek, models.DO_NOTHING)
    action = models.ForeignKey(Action, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'player_event_action'
        db_tablespace = 'geek'


class Season(models.Model):
    season_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'season'
        db_tablespace = 'geek'


class SeasonMatch(models.Model):
    match_id = models.AutoField(primary_key=True)
    match_date = models.DateTimeField()
    season = models.ForeignKey(Season, models.DO_NOTHING, blank=True)
    map = models.CharField(max_length=200)
    team_winner = models.ForeignKey('Team', models.DO_NOTHING, db_column='team_winner', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'season_match'
        db_tablespace = 'geek'


class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    season = models.ForeignKey(Season, models.DO_NOTHING)
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=5000, blank=True, null=True)
    captain = models.ForeignKey(Geek, models.DO_NOTHING, related_name="captain")
    co_captain = models.ForeignKey(Geek, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'team'
        db_tablespace = 'geek'


class TeamEventAction(models.Model):
    team_event_action_id = models.AutoField(primary_key=True)
    event_time = models.DateTimeField(blank=True, null=True)
    round = models.ForeignKey(MatchRound, models.DO_NOTHING)
    team = models.ForeignKey(Team, models.DO_NOTHING, blank=True, null=True)
    action = models.ForeignKey(Action, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'team_event_action'
        db_tablespace = 'geek'


class TeamGeek(models.Model):
    geek = models.OneToOneField(Geek, models.DO_NOTHING, primary_key=True)
    team = models.ForeignKey(Team, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'team_geek'
        unique_together = (('geek', 'team'),)
        db_tablespace = 'geek'


class Tier(models.Model):
    tier_id = models.AutoField(primary_key=True)
    tier_name = models.CharField(max_length=250)
    tier_description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tier'
        db_tablespace = 'geek'

class TiersData(models.Model):
    geekid = models.IntegerField()
    player = models.CharField(max_length=250)
    tier = models.CharField(max_length=250)
    tier_id = models.IntegerField()
    generation = models.IntegerField()
    matchdate = models.DateField()
    kills = models.IntegerField()
    deaths = models.IntegerField() 
    assists = models.IntegerField()
    kdr = models.DecimalField(max_digits=8, decimal_places=2)
    akdr = models.DecimalField(max_digits=8, decimal_places=2)
    alltime_kdr = models.DecimalField(max_digits=8, decimal_places=2)
    year_kdr = models.DecimalField(max_digits=8, decimal_places=2)
    last90_kdr = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'tiers_data'
        db_tablespace = 'geek'
    
class TeamWins(models.Model):
    match_date = models.DateField()
    map = models.CharField(max_length=250)
    team_name = models.CharField(max_length=250)
    wins = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'team_wins'
        db_tablespace = 'geek'

class GeekInfo(models.Model):
    player = models.CharField(max_length=250)
    tier = models.CharField(max_length=250)
    generation = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    member_since = models.DateField()
    matches = models.IntegerField()
    kills = models.IntegerField()
    deaths = models.IntegerField()
    assists = models.IntegerField()
    kdr = models.DecimalField(max_digits=8, decimal_places=2)
    akdr = models.DecimalField(max_digits=8, decimal_places=2)
    tenure = models.DecimalField(max_digits=8, decimal_places=2)
    alltime_kdr = models.DecimalField(max_digits=8, decimal_places=2)
    year_kdr = models.DecimalField(max_digits=8, decimal_places=2)
    last90_kdr = models.DecimalField(max_digits=8, decimal_places=2)
    
    class Meta:
        managed = False
        db_table = 'geek_info'
        db_tablespace = 'geek'

class FragDetails(models.Model):
    match_date = models.DateField()
    match_datetime = models.DateField()
    killer = models.CharField(max_length=250)
    victim = models.CharField(max_length=250)
    victim_id = models.IntegerField()
    map = models.CharField(max_length=250)
    weapon = models.CharField(max_length=250)
    partner = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    
    class Meta:
        managed = False
        db_table = 'frag_details'
        db_tablespace = 'geek'

class GeekAuthUser(models.Model):
    geek_id = models.AutoField(primary_key=True)
    handle = models.CharField(max_length=250, blank=True, null=True)
    location = models.CharField(max_length=20, blank=True, null=True)
    occupation = models.CharField(max_length=250, blank=True, null=True)
    member_since = models.DateField(blank=True, null=True)
    valid_sent_date = models.DateField()
    validated = models.IntegerField()
    geek_code = models.CharField(max_length=45)
    authid = models.IntegerField()
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateField()

    class Meta:
        managed = False
        db_table = 'geek_auth_user'
        db_tablespace = 'geek'
