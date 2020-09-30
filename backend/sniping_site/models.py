from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class Customer(models.Model):
    email = models.CharField(primary_key=True, max_length=50)
    play_name = models.CharField(max_length=100)
    max_price = models.FloatField(blank=True, null=True)
    section = models.CharField(max_length=30, blank=True, null=True)
    lower_date = models.DateTimeField(blank=True, null=True)
    higher_date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer'

class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Play(models.Model):
    date_time = models.DateTimeField()
    theatre_name = models.ForeignKey('Theatre', models.DO_NOTHING, db_column='theatre_name', blank=True, null=True)
    name = models.CharField(primary_key=True, max_length=100)
    latest_scrape_date_time = models.DateTimeField(blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    sections = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'play'
        unique_together = (('name', 'date_time'),)


class Price(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    value = models.FloatField()
    seat_column = models.CharField(max_length=5)
    seat_row = models.CharField(max_length=5)
    vendor = models.CharField(max_length=30, blank=True, null=True)
    seat_section = models.CharField(max_length=30)
    scraping_date_time = models.DateTimeField()
    play_date_time = models.DateTimeField()
    theatre_name = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'price'
        unique_together = (('seat_section', 'seat_row', 'seat_column', 'play_date_time', 'theatre_name', 'scraping_date_time'),)


class Seat(models.Model):
    seat_row = models.CharField(max_length=5)
    seat_column = models.CharField(max_length=5)
    theatre_name = models.ForeignKey('Theatre', models.DO_NOTHING, db_column='theatre_name')
    play_date_time = models.DateTimeField()
    section = models.CharField(primary_key=True, max_length=30)
    play_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'seat'
        unique_together = (('section', 'seat_row', 'seat_column', 'play_date_time', 'theatre_name'),)


class Theatre(models.Model):
    name = models.CharField(primary_key=True, max_length=60)
    location = models.CharField(max_length=30, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'theatre'


class TheatrePlay(models.Model):
    theatre_name = models.OneToOneField(Theatre, models.DO_NOTHING, db_column='theatre_name', primary_key=True)
    play_name = models.ForeignKey(Play, models.DO_NOTHING, db_column='play_name')
    play_date_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'theatre_play'
        unique_together = (('theatre_name', 'play_name', 'play_date_time'),)



