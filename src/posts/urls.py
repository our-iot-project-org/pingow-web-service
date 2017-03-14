from django.conf.urls import url
from django.contrib import admin

from .views import (
	post_list,
	post_create,
	post_detail,
	post_update,
	post_delete,
	position_update,
	send_review,
	get_recommendation_for_shop,
	get_recommendation_for_product,
	init_trip,
	get_shop_asst_for_shop,
	get_shop_asst_for_shop_and_product
	)

urlpatterns = [
	url(r'^$', post_list, name='list'),
	url(r'^position/$', position_update),
	url(r'^send_review/$', send_review),
	url(r'^get_recommendation_for_shop/$', get_recommendation_for_shop),
	url(r'^get_recommendation_for_product/$', get_recommendation_for_product),
	url(r'^init_trip/$', init_trip),
	url(r'^get_shop_asst_for_shop/$', get_shop_asst_for_shop),
	url(r'^get_shop_asst_for_shop_and_product/$', get_shop_asst_for_shop_and_product),
    url(r'^create/$', post_create),
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
    #url(r'^posts/$', "<appname>.views.<function_name>"),

]
