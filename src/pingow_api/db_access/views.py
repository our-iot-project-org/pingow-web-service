from pingow_api import models as m
from pingow_api import serializers as s
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from django.core import serializers
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
try:
    from urllib import quote_plus  # python 2
except:
    pass

try:
    from urllib.parse import quote_plus  # python 3
except:
    pass

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType

from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

def db_customer_json (request):
    obj = m.Customer.objects.all()
    serializer =s.CustomerSerializer(obj, many = True)
    return  JsonResponse(serializer.data, safe=False)

def db_shop_json (request):
    obj = m.Shop.objects.all()
    serializer =s.ShopSerializer(obj, many = True)
    return  JsonResponse(serializer.data, safe=False)

def db_beacon_json (request):
    obj = m.Beacon.objects.all()
    serializer =s.BeaconSerializer(obj, many = True)
    return  JsonResponse(serializer.data, safe=False)

def db_beacon_relationship_json (request):
    obj = m.BeaconRelationship.objects.all()
    serializer =s.BeaconRelationshipSerializer(obj, many = True)
    return  JsonResponse(serializer.data, safe=False)

def db_assistance_json (request):
    obj = m.Assistance.objects.all()
    serializer =s.AssistanceSerializer(obj, many = True)
    return  JsonResponse(serializer.data, safe=False)

def db_crowd_json (request):
    obj = m.Crowd.objects.all()
    serializer =s.CrowdSerializer(obj, many = True)
    return  JsonResponse(serializer.data, safe=False)

def db_assistance_avail_json (request):
    obj = m.AssistanceAvail.objects.all()
    serializer =s.AssistanceAvailSerializer(obj, many = True)
    return  JsonResponse(serializer.data, safe=False)

def db_shop_subcat_reference_json (request):
    obj = m.ShopSubCatReference.objects.all()
    serializer =s.ShopSubCatReferenceSerializer(obj, many = True)
    return  JsonResponse(serializer.data, safe=False)

def db_sub_category_json (request):
    obj = m.SubCategory.objects.all()
    serializer =s.SubCategorySerializer(obj, many = True)
    return  JsonResponse(serializer.data, safe=False)

def db_customer_transaction_json (request):
    obj = m.CustomerTransaction.objects.all()
    serializer =s.CustomerTransactionSerializer(obj, many = True)
    return  JsonResponse(serializer.data, safe=False)
