from django.db import models
import django_tables2 as tables
from .core import constants as c

# Create your models here.


class Customer(models.Model):
    CUSTOMER_ID= models.AutoField(primary_key=True)
    CUSTOMER_NAME = models.CharField(max_length = 250,null=True)
    DATE_OF_BIRTH = models.DateField(null=True)
    AGE_GROUP = models.IntegerField(choices = c.AGE_GROUP_CHOICES,null=True)
    GENDER = models.CharField(max_length = 10, choices = c.GENDER_CHOICES,null=True)
    PREF_LANG_1 = models.CharField(max_length = 25, null=True)
    PREF_LANG_2 = models.CharField(max_length = 25, null=True)
    USER_TYPE = models.CharField(max_length = 25, null=True)
    DATE_REG = models.DateField(null=True)
    def get_absolute_url(self):
        return '#'
    class Meta:
        db_table = 'pg_customer'


class Shop(models.Model):
    YN_CHOICES = (
        ('Y','Yes'),
        ('N','No')
    )
    SHOP_ID =  models.AutoField(primary_key=True)
    SHOP_NAME = models.CharField(max_length =250,null=True)
    DATE_REG = models.DateField(null=True)
    DATE_DEREG = models.DateField(null=True)
    W_FRIENDLY = models.CharField(max_length = 1,choices =YN_CHOICES, default = 'N',null=True)
    ASSIST_AVAIL = models.CharField(max_length = 1,choices =YN_CHOICES, default = 'N',null=True)
    AVG_RATING = models.IntegerField(null=True)
    VISITS = models.IntegerField(null=True)

    class Meta:
        db_table = 'pg_shop'

class Beacon(models.Model):
    BEACON_ID =  models.AutoField(primary_key=True)
    SHOP_ID = models.IntegerField()
    class Meta:
        db_table = 'pg_beacon'

class BeaconRelationship(models.Model):
    RELATHIPSHIP_TYPE_CHOICES = (
        (c.POSITION_REL_NEARBY,c.POSITION_REL_NEARBY),
        (c.POSITION_REL_TARGET,c.POSITION_REL_TARGET),
        (c.POSITION_REL_NO,c.POSITION_REL_NO)
    )
    RELATIONSHIP_ID =  models.AutoField(primary_key=True)
    BEACON_ID =  models.IntegerField(null=True)
    BEACON_ID_SEC = models.IntegerField(null=True)
    RELATIONSHIP_TYPE = models.CharField(max_length = 25, choices=RELATHIPSHIP_TYPE_CHOICES, default=c.POSITION_REL_NO,null=True)
    class Meta:
        db_table = 'pg_beacon_relationship'

class Assistance(models.Model):
    ASST_ID =  models.AutoField(primary_key=True)
    SHOP_ID = models.IntegerField(null=True)
    ASST_NAME = models.CharField(max_length = 250,null=True)
    DATE_OF_BIRTH = models.DateField(null=True)
    AGE_GROUP = models.IntegerField(choices = c.AGE_GROUP_CHOICES,null=True)
    GENDER = models.CharField(max_length = 10, choices = c.GENDER_CHOICES, null=True)
    PREF_LANG_1 = models.CharField(max_length = 25,null=True)
    PREF_LANG_2 = models.CharField(max_length = 25,null=True)
    TRAINED_SKILL = models.CharField(max_length = 25,null=True)
    TRAINED_LEVEL = models.CharField(max_length = 25,null=True)
    PRODUCT_SKILL = models.CharField(max_length = 250,null=True)
    PHOTO_URL = models.CharField(max_length = 500,null=True)
    class Meta:
        db_table = 'pg_assistance'

class Crowd(models.Model):
    CROWD_LEVEL_CHOICES = (
        (1, 'Green'),
        (2, 'Orange'),
        (3, 'Red'),
    )
    CROWD_ID =  models.AutoField(primary_key=True)
    SHOP_ID = models.IntegerField(null=True)
    CROWD_LEVEL = models.IntegerField(choices=CROWD_LEVEL_CHOICES, default=1, null=True)
    class Meta:
        db_table = 'pg_crowd'

class AssistanceAvail(models.Model):
    ASST_ID = models.IntegerField(primary_key=True)
    TIME_IN  = models.DateField(null=True)
    TIME_OUT = models.DateField(null=True)
    AVAILABILITY = models.BooleanField()
    class Meta:
        db_table = 'pg_assistance_avail'

class ShopSubCatReference(models.Model):
    REF_ID =  models.AutoField(primary_key=True)
    SHOP_ID = models.IntegerField(null=True)
    SUB_CAT_ID = models.IntegerField(null=True)
    class Meta:
        db_table = 'pg_shop_subcat_ref'

class SubCategory(models.Model):
    SUB_CAT_ID = models.AutoField(primary_key=True)
    SUB_CAT_NAME  = models.CharField(max_length = 250,null=True)
    class Meta:
        db_table = 'pg_sub_cat'


class CustomerTransaction(models.Model):
    TRANSACTION_ID = models.IntegerField(primary_key=True)
    CUSTOMER_ID = models.IntegerField(null=True)
    SUB_CAT_ID = models.IntegerField(null=True)
    SHOP_ID = models.IntegerField(null=True)
    ASST_ID = models.IntegerField(null=True)
    CREATION_DATE  = models.DateField(null=True)
    TIME_OF_ENTER  = models.DateTimeField(null=True)
    TIME_OF_EXIT  = models.DateTimeField(null=True)
    ASST_SVC_RATE = models.IntegerField(null=True)
    OVERALL_RATE = models.DecimalField(max_digits=10,decimal_places=2, null=True)
    COMMENTS = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'pg_customer_trans'

class CustomerTable(tables.Table):
    class Meta:
        model = Customer
        attrs = {'class': 'table table-hover'}

class CustomerTransactionTable(tables.Table):
    class Meta:
        model = CustomerTransaction
        attrs = {'class': 'table table-hover'}
