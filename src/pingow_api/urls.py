from django.conf.urls import url
from django.contrib import admin

from .views import (
	position_update,
	send_review,
	get_recommendation_for_shop,
	get_recommendation_for_product,
	init_trip_with_shop,
	init_trip_with_shop_and_product,
	get_shop_asst,
	api_post,
	)

urlpatterns = [
	url(r'^position/$', position_update),
	url(r'^send_review/$', send_review),
	url(r'^get_recommendation_for_shop/$', get_recommendation_for_shop),
	url(r'^get_recommendation_for_product/$', get_recommendation_for_product),
	url(r'^init_trip_with_shop/$', init_trip_with_shop),
	url(r'^init_trip_with_shop_and_product/$', init_trip_with_shop_and_product),
	url(r'^get_shop_asst/$', get_shop_asst),
	url(r'^api_post/$', api_post),
    #url(r'^posts/$', "<appname>.views.<function_name>"),

]
