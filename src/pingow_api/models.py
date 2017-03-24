from django.db import models
import django_tables2 as tables
from .core import constants as c

# Create your models here.


class Customer(models.Model):
    CUSTOMER_ID= models.AutoField(primary_key=True)
    CUSTOMER_NAME = models.CharField(max_length = 250)
    DATE_OF_BIRTH = models.DateField()
    AGE_GROUP = models.IntegerField(choices = c.AGE_GROUP_CHOICES)
    GENDER = models.CharField(max_length = 10, choices = c.GENDER_CHOICES)
    PREF_LANG_1 = models.CharField(max_length = 25)
    PREF_LANG_2 = models.CharField(max_length = 25)
    USER_TYPE = models.CharField(max_length = 25)
    DATE_REG = models.DateField()
    def get_absolute_url(self):
        return '#'
    class Meta:
        db_table = 'pg_customer'

class CustomerTable(tables.Table):
    class Meta:
        model = Customer
        attrs = {'class': 'table table-hover'}

class Shop(models.Model):
    YN_CHOICES = (
        ('Y','Yes'),
        ('N','No')
    )
    SHOP_ID =  models.AutoField(primary_key=True)
    SHOP_NAME = models.CharField(max_length =250)
    DATE_REG = models.DateField()
    DATE_DEREG = models.DateField()
    W_FRIENDLY = models.CharField(max_length = 1,choices =YN_CHOICES, default = 'N')
    ASSIST_AVAIL = models.CharField(max_length = 1,choices =YN_CHOICES, default = 'N')
    AVG_RATING = models.IntegerField()
    VISITS = models.IntegerField()

    class Meta:
        db_table = 'pg_shop'

class Beacon(models.Model):
    BEACON_ID =  models.AutoField(primary_key=True)
    SHOP_ID = models.ForeignKey(Shop, on_delete=models.CASCADE, db_column = 'SHOP_ID')
    class Meta:
        db_table = 'pg_beacon'

class BeaconRelationship(models.Model):
    RELATHIPSHIP_TYPE_CHOICES = (
        (c.POSITION_REL_NEARBY,c.POSITION_REL_NEARBY),
        (c.POSITION_REL_TARGET,c.POSITION_REL_TARGET),
        (c.POSITION_REL_NO,c.POSITION_REL_NO)
    )
    RELATIONSHIP_ID =  models.AutoField(primary_key=True)
    BEACON_ID =  models.ForeignKey(Beacon, on_delete=models.CASCADE, db_column = 'BEACON_ID')
    BEACON_ID_SEC = models.IntegerField()
    RELATIONSHIP_TYPE = models.CharField(max_length = 25, choices=RELATHIPSHIP_TYPE_CHOICES, default=c.POSITION_REL_NO)
    class Meta:
        db_table = 'pg_beacon_relationship'

class Assistance(models.Model):
    ASST_ID =  models.AutoField(primary_key=True)
    SHOP_ID = models.ForeignKey(Shop, on_delete=models.CASCADE, db_column = 'SHOP_ID')
    ASST_NAME = models.CharField(max_length = 250)
    DATE_OF_BIRTH = models.DateField()
    AGE_GROUP = models.IntegerField(choices = c.AGE_GROUP_CHOICES)
    GENDER = models.CharField(max_length = 10, choices = c.GENDER_CHOICES)
    PREF_LANG_1 = models.CharField(max_length = 25)
    PREF_LANG_2 = models.CharField(max_length = 25)
    TRAINED_SKILL = models.CharField(max_length = 25)
    TRAINED_LEVEL = models.CharField(max_length = 25)
    PRODUCT_SKILL = models.CharField(max_length = 250)
    class Meta:
        db_table = 'pg_assistance'

class Crowd(models.Model):
    CROWD_LEVEL_CHOICES = (
        (1, 'Green'),
        (2, 'Orange'),
        (3, 'Red'),
    )
    CROWD_ID =  models.AutoField(primary_key=True)
    SHOP_ID = models.ForeignKey(Shop, on_delete=models.CASCADE, db_column = 'SHOP_ID')
    CROWD_LEVEL = models.IntegerField(choices=CROWD_LEVEL_CHOICES, default=1)
    class Meta:
        db_table = 'pg_crowd'

class AssistanceAvail(models.Model):
    ASST_ID = models.ForeignKey(Assistance, on_delete=models.CASCADE, db_column = 'ASST_ID')
    TIME_IN  = models.DateField()
    TIME_OUT = models.DateField()
    AVAILABILITY = models.BooleanField()
    class Meta:
        db_table = 'pg_assistance_avail'

class ShopSubCatReference(models.Model):
    REF_ID =  models.AutoField(primary_key=True)
    SHOP_ID = models.ForeignKey(Shop, on_delete=models.CASCADE, db_column = 'SHOP_ID')
    SUB_CAT_ID = models.IntegerField()
    class Meta:
        db_table = 'pg_shop_subcat_ref'

class SubCategory(models.Model):
    SUB_CAT_ID = models.AutoField(primary_key=True)
    SUB_CAT_NAME  = models.CharField(max_length = 250)
    class Meta:
        db_table = 'pg_sub_cat'


class CustomerTransaction(models.Model):
    TRANSACTION_ID = models.AutoField(primary_key=True)
    CUSTOMER_ID = models.IntegerField()
    SUB_CAT_ID = models.IntegerField()
    SHOP_ID = models.IntegerField()
    ASST_ID = models.IntegerField()
    CREATION_DATE  = models.DateField()
    TIME_OF_ENTER  = models.DateField(null=True)
    TIME_OF_EXIT  = models.DateField(null=True)
    ASST_SVC_RATE = models.IntegerField()
    OVERALL_RATE = models.IntegerField()
    COMMENTS = models.TextField(blank=True)
    class Meta:
        db_table = 'pg_customer_trans'
