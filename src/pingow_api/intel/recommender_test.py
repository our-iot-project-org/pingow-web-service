from . import recommender as r

def recommendation_by_pdt_cat_test():
    cust_id = 2 #avoid using cust_id = 8 (logic got issue). advise to use 1, 2, 3, 4
    cust_selected_pdt_cat = 3 #or use 9, 1, 2, 3
    r.recommendation_by_pdt_cat()
    print("testing")
    return True

#recommend_shop_asst_test()
