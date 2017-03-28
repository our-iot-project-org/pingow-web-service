from rest_framework.serializers import ModelSerializer

from pingow_api import models as m

class CustomerSerializer(ModelSerializer):
    class Meta:
        model = m.Customer
        fields = [
            'CUSTOMER_ID',
            'CUSTOMER_NAME' ,
            'DATE_OF_BIRTH' ,
            'AGE_GROUP',
            'GENDER' ,
            'PREF_LANG_1',
            'PREF_LANG_2',
            'USER_TYPE',
            'DATE_REG' ,
        ]

class ShopSerializer(ModelSerializer):
    class Meta:
        model = m.Shop
        fields = [
            'SHOP_ID',
            'SHOP_NAME',
            'DATE_REG',
            'DATE_DEREG',
            'W_FRIENDLY',
            'ASSIST_AVAIL',
            'AVG_RATING',
            'VISITS',
        ]

class BeaconSerializer(ModelSerializer):
    class Meta:
        model = m.Beacon
        fields = [
            'BEACON_ID',
            'SHOP_ID' ,
        ]

class BeaconRelationshipSerializer(ModelSerializer):
    class Meta:
        model = m.BeaconRelationship
        fields = [
            'RELATIONSHIP_ID',
            'BEACON_ID',
            'BEACON_ID_SEC',
            'RELATIONSHIP_TYPE',
        ]

class AssistanceSerializer(ModelSerializer):
    class Meta:
        model = m.Assistance
        fields = [
            'ASST_ID',
            'SHOP_ID',
            'ASST_NAME',
            'DATE_OF_BIRTH',
            'AGE_GROUP',
            'GENDER',
            'PREF_LANG_1',
            'PREF_LANG_2',
            'TRAINED_SKILL',
            'TRAINED_LEVEL',
            'PRODUCT_SKILL',
            'PHOTO_URL',
        ]

class CrowdSerializer(ModelSerializer):
    class Meta:
        model = m.Crowd
        fields = [
            'CROWD_ID',
            'SHOP_ID',
            'CROWD_LEVEL'
        ]

class AssistanceAvailSerializer(ModelSerializer):
    class Meta:
        model = m.AssistanceAvail
        fields = [
            'ASST_ID',
            'TIME_IN',
            'TIME_OUT',
            'AVAILABILITY',
        ]

class ShopSubCatReferenceSerializer(ModelSerializer):
    class Meta:
        model = m.ShopSubCatReference
        fields = [
            'REF_ID',
            'SHOP_ID',
            'SUB_CAT_ID'
        ]

class SubCategorySerializer(ModelSerializer):
    class Meta:
        model = m.SubCategory
        fields = [
            'SUB_CAT_ID',
            'SUB_CAT_NAME',
        ]

class CustomerTransactionSerializer(ModelSerializer):
    class Meta:
        model = m.CustomerTransaction
        fields = [
            'TRANSACTION_ID',
            'CUSTOMER_ID',
            'SUB_CAT_ID',
            'SHOP_ID',
            'ASST_ID',
            'CREATION_DATE',
            'TIME_OF_ENTER',
            'TIME_OF_EXIT',
            'ASST_SVC_RATE',
            'OVERALL_RATE',
            'COMMENTS',
        ]
