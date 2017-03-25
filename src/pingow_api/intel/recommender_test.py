from . import recommender as r
########################## NOTE 2 ##############################################

#input from mobile interface (temp : need to replace with actual)
#note: either cust_selected_pdt_cat or #cust_selected_shop will be selected.

cust_id = 2 #avoid using cust_id = 8 (logic got issue). advise to use 1, 2, 3, 4
cust_selected_pdt_cat = 3 #or use 9, 1, 2, 3
cust_selected_shop = 17 #use electronics shop -  1,2,3,12,13,15,16 or watch - 10, 17, 18 , 19, 20
cust_destination = 17 #use electronics shop -  1,2,3,12,13,15,16 or watch - 10, 18 , 17,19, 20

def test(module_name):
    if module_name == 'recommendation_by_pdt_cat_test':
        return recommendation_by_pdt_cat_test()
    elif module_name == 'recommendation_by_shop_names':
        return recommendation_by_shop_names_test()
    return 'no matching test module name found, check recommender_test (e.g: recommendation_by_pdt_cat_test...)'

def recommendation_by_pdt_cat_test():
    cust_id = 2 #avoid using cust_id = 8 (logic got issue). advise to use 1, 2, 3, 4
    cust_selected_pdt_cat = 3 #or use 9, 1, 2, 3
    result = r.recommendation_by_pdt_cat(cust_id, cust_selected_pdt_cat)
    return result

def recommendation_by_shop_names_test():
    cust_id = 2 #avoid using cust_id = 8 (logic got issue). advise to use 1, 2, 3, 4
    cust_selected_pdt_cat = 3 #or use 9, 1, 2, 3
    result = r.recommendation_by_shop_names(cust_selected_pdt_cat)
    return result
