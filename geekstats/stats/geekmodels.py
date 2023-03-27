# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models

from stats.functions import season

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
    userid = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column="user_id", blank=True, null=True) 
    alltime_kdr = models.DecimalField(max_digits=8, decimal_places=2)
    year_kdr = models.DecimalField(max_digits=8, decimal_places=2)
    geek_code = models.CharField(max_length=250, blank=True, null=True)
    last90_kdr = models.DecimalField(max_digits=8, decimal_places=2)
    avatar = models.ImageField(upload_to='stats/avatars', blank=True)
    
    class Meta:
        managed = False
        db_table = 'geek'
        db_tablespace = 'geek'

    def __str__(self):
         return self.handle + '('+str(self.geek_id)+')'

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

class GeekKDRHistory(models.Model):
    geek_id = models.IntegerField()
    handle = models.CharField(max_length=250, blank=True, null=True)
    history_date = models.DateField(blank=True, null=True)
    alltime_kdr = models.DecimalField(max_digits=8, decimal_places=2)
    year_kdr = models.DecimalField(max_digits=8, decimal_places=2)
    last90_kdr = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'geek_kdr_history'
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

class Maps(models.Model):
    idmap =  models.AutoField(primary_key=True)
    map = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    type = models.CharField(max_length=1000)
    theme = models.CharField(max_length=1000)
    workshop_link = models.CharField(max_length=1000)
    votescore = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    balance = models.CharField(max_length=1000)
    ct_wins = models.IntegerField(blank=True, null=True)
    t_wins = models.IntegerField(blank=True, null=True)    
    plays = models.IntegerField(blank=True, null=True)
    s_plays = models.IntegerField(blank=True, null=True)
    last_play = models.IntegerField(blank=True, null=True)
    hero_image = models.ImageField(upload_to='maps/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='maps/', blank=True, null=True)
    radar = models.ImageField(upload_to='maps/', blank=True, null=True)
    image2 = models.ImageField(upload_to='maps/', blank=True, null=True)
    image3 = models.ImageField(upload_to='maps/', blank=True, null=True)
    metascore = models.IntegerField(blank=True, null=True)    
    votes = models.IntegerField(blank=True, null=True)
    no_obj_rounds = models.IntegerField(blank=True, null=True)
    bomb_plant_rounds = models.IntegerField(blank=True, null=True)
    bomb_explode_rounds = models.IntegerField(blank=True, null=True)
    defuse_rounds = models.IntegerField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'map'
        db_tablespace = 'geek'

    def __str__(self):
         return self.map

class MapRating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    map = models.ForeignKey('Maps', models.DO_NOTHING)
    geek = models.ForeignKey(Geek, models.DO_NOTHING)
    rating = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'map_rating'
        db_tablespace = 'geek'

class MatchRound(models.Model):
    round_id = models.AutoField(primary_key=True)
    match = models.ForeignKey('SeasonMatch', models.DO_NOTHING, related_name='rounds')
    ct_team = models.ForeignKey('Team', models.DO_NOTHING, blank=True, null=True, related_name="ct_teams")
    t_team = models.ForeignKey('Team', models.DO_NOTHING, blank=True, null=True, related_name="t_teams")
    win_side = models.CharField(max_length=100, blank=True, null=True)
    map_id = models.ForeignKey('Maps', models.DO_NOTHING)

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
    description = models.CharField(max_length=500)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    master_win = models.ForeignKey('Geek', models.DO_NOTHING, db_column='master_win', related_name='geek_id1',null=True, blank=True)
    gold_win = models.ForeignKey('Geek', models.DO_NOTHING, db_column='gold_win', related_name='geek_id2',null=True, blank=True)
    silver_win = models.ForeignKey('Geek', models.DO_NOTHING, db_column='silver_win', related_name='geek_id3',null=True, blank=True)
    bronze_win = models.ForeignKey('Geek', models.DO_NOTHING, db_column='bronze_win', related_name='geek_id4',null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'season'
        db_tablespace = 'geek'

    def __str__(self):
         return self.name


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

    def __str__(self):
         return self.name

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




class Tier(models.Model):
    tier_id = models.AutoField(primary_key=True)
    tier_name = models.CharField(max_length=250)
    tier_description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tier'
        db_tablespace = 'geek'

    def __str__(self):
         return self.tier_name

class TeamGeek(models.Model):
    teamgeek_id = models.AutoField(primary_key=True)
    geek = models.ForeignKey(Geek, models.DO_NOTHING)
    team = models.ForeignKey(Team, models.DO_NOTHING)
    tier = models.ForeignKey(Tier, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'team_geek'
        unique_together = (('geek', 'team'),)
        db_tablespace = 'geek'    
        
    def __str__(self):
         return str(self.team) + ':  '+str(self.geek)



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

class MapData(models.Model):
    map_id = models.IntegerField()
    map = models.CharField(max_length=250, blank=True, null=True)
    match_date = models.DateField(blank=True, null=True)
    win_side = models.CharField(max_length=250, blank=True, null=True)
    type = models.CharField(max_length=250, blank=True, null=True)
    theme = models.CharField(max_length=250, blank=True, null=True)
    votescore = models.DecimalField(max_digits=8, decimal_places=2)
    thumbnail = models.ImageField(upload_to='maps/', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'map_data'
        db_tablespace = 'geek' 

class SeasonWins(models.Model):
    match_date = models.DateField(blank=True, null=True)
    match_id = models.IntegerField()
    map = models.CharField(max_length=250, blank=True, null=True)
    round_id = models.IntegerField()
    win_side = models.CharField(max_length=250)
    season = models.CharField(max_length=250)
    winner = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'season_wins'
        db_tablespace = 'geek' 

class Damage(models.Model):
    damage_id = models.AutoField(primary_key=True)
    geek = models.ForeignKey('Geek', models.DO_NOTHING)
    round = models.ForeignKey('MatchRound', models.DO_NOTHING)
    victim = models.ForeignKey('Geek', models.DO_NOTHING, related_name="d_victim")
    item = models.ForeignKey('Item', models.DO_NOTHING)
    pos_x = models.DecimalField(max_digits=12, decimal_places=4)
    pos_y = models.DecimalField(max_digits=12, decimal_places=4)
    pos_z = models.DecimalField(max_digits=12, decimal_places=4)
    pos_victim_x = models.DecimalField(max_digits=12, decimal_places=4)
    pos_victim_y = models.DecimalField(max_digits=12, decimal_places=4)
    pos_victim_z = models.DecimalField(max_digits=12, decimal_places=4)
    distance = models.DecimalField(max_digits=12, decimal_places=4)
    damage_armor = models.IntegerField()
    damage_health = models.IntegerField()
    armor_remaining = models.IntegerField()
    health_remaining = models.IntegerField()
    hitgroup = models.CharField(max_length=45)
    is_kill = models.IntegerField()
    is_team_damage = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'damage'
        db_tablespace = 'geek'
    