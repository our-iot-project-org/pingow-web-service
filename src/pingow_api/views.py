from .core import position_relationship
from .core import messenger
from .core import console_print
from .core import query_exec
from .core import constants
from .core import transaction_factory
from .forms import CustomerCreationForm
from .models import Customer, CustomerTransaction
from .models import CustomerTable, CustomerTransactionTable
from .intel import recommender as r
from .intel import recommender_test as rt

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
from django.utils import timezone
#
# /position?
# cusId=bob&
# targetPos=6&
# currentPos=6&
# trxId=1&
# asst=True
# Response:
# [exit: False,
# nearby: True]
@csrf_exempt
def position_update(request):
    if request.method == 'GET':
        target = request.GET.get('targetPos', None)
        current = request.GET.get('currentPos', None)
        cusId = get_cusId( request.GET.get('cusId', None))
        trxId = request.GET.get('trxId', None)
        is_asst_needed = request.GET.get('asst', None)
        if (target is None) | (current is None) | (cusId is None) | (trxId is None) | (is_asst_needed is None):
            response = JsonResponse({'status': constants.VALUE_NULL})
        else:
            #check position between current position with shop
            rel = position_relationship.get_position_relationship(target, current)
            isNearBy = (rel==constants.POSITION_REL_NEARBY)
            isTarget = (rel==constants.POSITION_REL_TARGET)
            #check if exit or not
            position_relationship.update_position_status(trxId, current, target)
            is_exit = (position_relationship.get_position_status(trxId) == constants.POSITION_STATUS_EXIT)
            is_notify = is_asst_needed and (not is_exit) and (isNearBy | isTarget)
            if is_exit:
                isNearBy = False
            if is_notify:
                messenger.notify_assistance(rel, cusId, current, target)
                # print('Message Sent')
            else:
                print('NO Messages')
            print('trxId=',trxId,'\t current=',current,'\t target=',target,'\t is_exit=',is_exit,'\t STATUS=',position_relationship.get_position_status(trxId))
            response = JsonResponse({'exit': is_exit, 'nearby': isNearBy })
        return response
    elif request.method == 'POST':
        response = JsonResponse({'requesting': 'POST REQUEST' })
        return response
    else:
        raise Http404()

# cusId, shopId, shopStar, shopAsstStar, trxId=1
# reviewText="this place is nice"
# Response: # [success:True]
def send_review(request):
    if request.method == 'GET':
        cusId = get_cusId( request.GET.get('cusId', None))
        shopId = request.GET.get('shopId', None)
        shopStar = request.GET.get('shopStar', None)
        shopAsstStar = request.GET.get('shopAsstStar', None)
        trxId = request.GET.get('trxId', None)
        reviewText = request.GET.get('reviewText', '')
        if (cusId is None) | (shopId is None) | (shopStar is None) | (shopAsstStar is None) |  (trxId is None):
            response = JsonResponse({'success': False})
        else:
            #Commit review to DB
            status = transaction_factory.update_trans(trxId, cusId, shopId, shopStar, shopAsstStar, reviewText)
            response = JsonResponse({'success': status})
        return response
    else:
        raise Http404()

#/get_recommendation_for_shop?
# cusId=bob&
# shopId=1
# Response:
# [shops: [2,3,5]]
def get_recommendation_for_shop(request):
    if request.method == 'GET':
        cusId = get_cusId( request.GET.get('cusId', None))
        shopId = request.GET.get('shopId', None)
        if (cusId is None) | (shopId is None):
            response = JsonResponse({'status': constants.VALUE_NULL})
        else:
            rec_shops = r.recommendation_by_shop_names(int(shopId))
            rec_shopx = list(rec_shops)
            response = JsonResponse({'shops': rec_shops})
            print(rec_shops)
        return response
    else:
        raise Http404()

#/get_recommendation_for_shop?
# cusId=bob&
# productCatId=1
# Response:
# [shops: [2,3,5]]
def get_recommendation_for_product(request):
    if request.method == 'GET':
        cusId = get_cusId( request.GET.get('cusId', None))
        productCatId = request.GET.get('productCatId', None)
        if (cusId is None) | (productCatId is None):
            response = JsonResponse({'status': constants.VALUE_NULL})
        else:
            rec_shops = r.recommendation_by_pdt_cat(int(cusId),int(productCatId))
            response = JsonResponse({'shops': rec_shops})
        return response
    else:
        raise Http404()

# /init_trip_with_shop?
# cusId=bob&
# shopId=1
# Response:
# [transactionId: 1]
def init_trip_with_shop(request):
    if request.method == 'GET':
        cusId = get_cusId( request.GET.get('cusId', None))
        shopId = request.GET.get('shopId', None)
        if (cusId is None) | (shopId is None):
            response = JsonResponse({'status': constants.VALUE_NULL})
        else:
            trans_id = transaction_factory.create_trans_id(cusId, shopId, None)
            response = JsonResponse({'transactionId': trans_id})
        return response
    else:
        raise Http404()

# /init_trip_with_shop_and_product?
# cusId=bob&
# shopId=1&
# productCatId=1
# Response:
# [transactionId: 1]
def init_trip_with_shop_and_product(request):
    if request.method == 'GET':
        cusId = get_cusId( request.GET.get('cusId', None))
        shopId = request.GET.get('shopId', None)
        productCatId = request.GET.get('productCatId', None)
        if (cusId is None) | (shopId is None) | (productCatId is None) :
            response = JsonResponse({'status': constants.VALUE_NULL})
        else:
            trans_id = transaction_factory.create_trans_id(cusId, shopId, productCatId)
            response = JsonResponse({'transactionId': trans_id})
        return response
    else:
        raise Http404()



#
# /get_shop_asst?
# cusId=bob&
# trxId=1
# Response:
# [shopAsstName: "Tracy",
# shopAsstDesc:"Tracy sells shoes"]
# shopAsstId:1
def get_shop_asst(request):
    if request.method == 'GET':
        cusId = get_cusId( request.GET.get('cusId', None))
        trxId = request.GET.get('trxId', None)
        if (cusId is None) | (trxId is None):
            response = JsonResponse({'status': constants.VALUE_NULL})
        else:
            #Commit review to DB
            #data  = query_exec.test_custom_sql()
            #json_data = serializers.serialize('json', data)
            #response = JsonResponse({json_data})
                response = JsonResponse({'shopAsstId':1,'shopAsstName': "Tracy", 'shopAsstDesc':"Tracy sells shoes"})
        return response
    else:
        raise Http404()

body_text = ""
@csrf_exempt
def api_post(request):
    global body_text
    if request.method == 'POST':
        body_text = str(request.body)
        response = JsonResponse({'request.body':body_text})
        return response
    elif request.method == 'GET':
        response = JsonResponse({'request.body':body_text})
        return response
    else:
        raise Http404()

def customer_profile_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise PermissionDenied("Please login as Admin/Staff role to access this page.")

    form = CustomerCreationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # message success
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
        "title" : "Create Customer Profile"
    }
    return render(request, "form.html", context)


def db_view_customer(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise PermissionDenied("Please login as Admin/Staff role to access this page.")

    queryset = Customer.objects.all()
    data_table = CustomerTable(queryset)

    context = {
        "table" : data_table,
        "title" : "CUSTOMER TABLE"
    }
    return render(request, "db_view.html", context)

def db_view_customer_trans(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise PermissionDenied("Please login as Admin/Staff role to access this page.")

    queryset = CustomerTransaction.objects.all()
    data_table = CustomerTransactionTable(queryset)

    context = {
        "table" : data_table,
        "title" : "CUSTOMER TRANSACTION TABLE"
    }
    return render(request, "db_view.html", context)

def test (request):
    module_name = request.GET.get('module', None)
    if (module_name is None):
        return JsonResponse({'Result':'NULL module parameter. Add ?module=some_name to URL to test'})
    else:
        result = rt.test(module_name)
        response = JsonResponse({'Result':result})
    return response
def get_cusId(cusId):
    if cusId=='bob':
        return 2
    elif cusId=='alice':
        return 1
    else:
        return 3
