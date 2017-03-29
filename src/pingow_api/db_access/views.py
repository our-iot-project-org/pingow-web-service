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

from pingow_api import models as m
from pingow_api import serializers as s
from pingow_api.forms import CustomerCreationForm, CustomerForm, AssistanceForm, CustomerTransactionForm

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

# ------------------------- Table views

def db_view_customer(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise PermissionDenied("Please login as Admin/Staff role to access this page.")

    queryset = m.Customer.objects.all()
    data_table = m.CustomerTable(queryset)

    context = {
        "table" : data_table,
        "title" : "CUSTOMER TABLE"
    }
    return render(request, "db_view.html", context)

def db_view_customer_trans(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise PermissionDenied("Please login as Admin/Staff role to access this page.")

    queryset = m.CustomerTransaction.objects.all()
    data_table = m.CustomerTransactionTable(queryset)

    context = {
        "table" : data_table,
        "title" : "CUSTOMER TRANSACTION TABLE"
    }
    return render(request, "db_view.html", context)

def db_view_shop(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise PermissionDenied("Please login as Admin/Staff role to access this page.")

    queryset = m.Shop.objects.all()
    data_table = m.ShopTable(queryset)

    context = {
        "table" : data_table,
        "title" : "SHOP TABLE"
    }
    return render(request, "db_view.html", context)

def db_view_sub_category(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise PermissionDenied("Please login as Admin/Staff role to access this page.")

    queryset = m.SubCategory.objects.all()
    data_table = m.SubCategoryTable(queryset)

    context = {
        "table" : data_table,
        "title" : "SUB CATEGORY TABLE"
    }
    return render(request, "db_view.html", context)

def db_view_assistance_avail(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise PermissionDenied("Please login as Admin/Staff role to access this page.")

    queryset = m.AssistanceAvail.objects.all()
    data_table = m.AssistanceAvailTable(queryset)

    context = {
        "table" : data_table,
        "title" : "ASSISTANCE AVAILABILITY TABLE"
    }
    return render(request, "db_view.html", context)

def db_view_assistance(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise PermissionDenied("Please login as Admin/Staff role to access this page.")

    queryset = m.Assistance.objects.all()
    data_table = m.AssistanceTable(queryset)

    context = {
        "table" : data_table,
        "title" : "ASSISTANCE TABLE"
    }
    return render(request, "db_view.html", context)

# ------------ Table update
def customer_profile_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise PermissionDenied("Please login as Admin/Staff role to access this page.")

    form = CustomerCreationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
        "title" : "Create Customer Profile"
    }
    return render(request, "form.html", context)

def assistance_update(request, asst_id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise PermissionDenied("Please login as Admin/Staff role to access this page.")

    instance = get_object_or_404(m.Assistance, ASST_ID=asst_id)
    form = AssistanceForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        info_message = "<a href='#'>Assistance " + asst_id + " Profile</a> Saved"
        messages.success(request, info_message ,
                         extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
        "title" : "Update Assistance Profile"
    }
    return render(request, "form.html", context)

def customer_trans_update(request, trans_id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise PermissionDenied("Please login as Admin/Staff role to access this page.")

    instance = get_object_or_404(m.CustomerTransaction, TRANSACTION_ID=trans_id)
    form = CustomerTransactionForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        info_message = "<a href='#'>TRANSACTION_ID " + trans_id + "</a> Saved"
        messages.success(request, info_message ,
                         extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
        "title" : "Update Customer Transaction"
    }
    return render(request, "form.html", context)

def customer_update(request, customer_id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise PermissionDenied("Please login as Admin/Staff role to access this page.")

    instance = get_object_or_404(m.Customer, CUSTOMER_ID=customer_id)
    form = CustomerForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        info_message = "<a href='#'>TRANSACTION_ID " + customer_id + "</a> Saved"
        messages.success(request, info_message ,
                         extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
        "title" : "Update Customer Profile"
    }
    return render(request, "form.html", context)
