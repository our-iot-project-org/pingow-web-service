from .core import position_relationship
from .core import messenger
from .core import console_print
from .core import query_exec
from .core import constants
from django.core import serializers
from rest_framework.response import Response
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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from comments.forms import CommentForm
from comments.models import Comment
from .forms import PostForm
from .models import Post


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # message success
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)

    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    comments = instance.comments
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "comments": comments,
        "comment_form": form,
    }
    return render(request, "post_detail.html", context)


def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()  # .order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()
    paginator = Paginator(queryset_list, 8)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "title": "List",
        "page_request_var": page_request_var,
        "today": today,
    }
    return render(request, "post_list.html", context)


def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None,
                    request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved",
                         extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("posts:list")


# /position?
# cusId=bob&
# targetPos=6&
# currentPos=6&
# trxId=1
# Response:
# [exit: False,
# nearby: True]
def position_update(request):
    if request.method == 'GET':
        target = request.GET.get('targetPos', None)
        current = request.GET.get('currentPos', None)
        customer = request.GET.get('cusId', None)
        trxId = request.GET.get('trxId', None)
        if (target is None) | (current is None) | (customer is None) | (trxId is None):
            response = JsonResponse({'status': constants.VALUE_NULL})
        else:
            rel = position_relationship.get_position_relationship(target, current)
            messenger.notify_assistance(rel, customer, current, target)
            isNearBy = (rel==constants.POSITION_REL_NEARBY)
            isTarget = (rel==constants.POSITION_REL_TARGET)
            response = JsonResponse({'exit': False, 'nearby': isNearBy })
        return response
    else:
        raise Http404()

# cusId, shopId, shopStar, shopAsstStar, trxId=1
# reviewText="this place is nice"
# Response: # [success:True]
def send_review(request):
    if request.method == 'GET':
        cusId = request.GET.get('cusId', None)
        shopId = request.GET.get('shopId', None)
        shopStar = request.GET.get('shopStar', None)
        shopAsstStar = request.GET.get('shopAsstStar', None)
        trxId = request.GET.get('trxId', None)
        reviewText = request.GET.get('reviewText', '')
        if (cusId is None) | (shopId is None) | (shopStar is None) | (shopAsstStar is None) |  (trxId is None):
            response = JsonResponse({'success': False})
        else:
            #Commit review to DB
            response = JsonResponse({'success': True})
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
        cusId = request.GET.get('cusId', None)
        shopId = request.GET.get('shopId', None)
        if (cusId is None) | (shopId is None):
            response = JsonResponse({'status': constants.VALUE_NULL})
        else:
            #Commit review to DB
            response = JsonResponse({'shops': '[2,3,5]'})
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
        cusId = request.GET.get('cusId', None)
        productCatId = request.GET.get('productCatId', None)
        if (cusId is None) | (productCatId is None):
            response = JsonResponse({'status': constants.VALUE_NULL})
        else:
            #Commit review to DB
            response = JsonResponse({'shops': '[2,3,5]'})
        return response
    else:
        raise Http404()

# /init_trip?
# cusId=bob&
# shopId=1
# Response:
# [transactionId: 1]
def init_trip(request):
    if request.method == 'GET':
        cusId = request.GET.get('cusId', None)
        shopId = request.GET.get('shopId', None)
        if (cusId is None) | (shopId is None):
            response = JsonResponse({'status': constants.VALUE_NULL})
        else:
            #Commit review to DB
            response = JsonResponse({'transactionId': 1})
        return response
    else:
        raise Http404()
#
# /get_shop_asst_for_shop?
# cusId=bob&
# shopId=1&
# trxId=1
# Response:
# [shopAsstName: "Tracy",
# shopAsstDesc:"Tracy sells shoes"]
def get_shop_asst_for_shop(request):
    if request.method == 'GET':
        cusId = request.GET.get('cusId', None)
        shopId = request.GET.get('shopId', None)
        trxId = request.GET.get('trxId', None)
        if (cusId is None) | (shopId is None) | (trxId is None):
            response = JsonResponse({'status': constants.VALUE_NULL})
        else:
            #Commit review to DB
            #data  = query_exec.test_custom_sql()
            #json_data = serializers.serialize('json', data)
            #response = JsonResponse({json_data})
                response = JsonResponse({'shopAsstName': "Tracy"})
        return response
    else:
        raise Http404()

# /get_shop_asst_for_shop_and_product?
# cusId=bob&
# shopId=1&
# productId=1&
# trxId=1
# Response:
# [shopAsstName: "Tracy",
# shopAsstDesc:"Tracy sells shoes"]
def get_shop_asst_for_shop_and_product(request):
    if request.method == 'GET':
        cusId = request.GET.get('cusId', None)
        shopId = request.GET.get('shopId', None)
        productId = request.GET.get('productId', None)
        trxId = request.GET.get('trxId', None)
        if (cusId is None) | (shopId is None) | (productId is None) | (trxId is None):
            response = JsonResponse({'status': constants.VALUE_NULL})
        else:
            #Commit review to DB
            response = JsonResponse({'shopAsstName': 'Tracy', 'shopAsstDesc':'Tracy sells shoes' })
        return response
    else:
        raise Http404()
