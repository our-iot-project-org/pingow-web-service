import datetime
from pingow_api  import models as m
from pingow_api.core  import constants as c
# trans_id = 0
def create_trans_id(cusId, shopId, productCatId):
    # global trans_id
    last_trans = m.CustomerTransaction.objects.all().order_by('-TRANSACTION_ID')
    if len(last_trans) == 0:
        new_trans_id = 1
    else:
        new_trans_id = last_trans[0].TRANSACTION_ID + 1
    #create new record
    new_trans = m.CustomerTransaction(
        TRANSACTION_ID = new_trans_id,
        CUSTOMER_ID = cusId,
        SHOP_ID = shopId,
        SUB_CAT_ID = productCatId,
        CREATION_DATE =  datetime.datetime.now().strftime(c.DATE_FMT)
        )
    new_trans.save()
    # trans_id = next_trans_id + 1
    return new_trans_id

def update_trans (trxId, cusId, shopId, shopStar, shopAsstStar, reviewText):
    new_trans = m.CustomerTransaction.objects.get(TRANSACTION_ID = trxId)
    new_trans.CUSTOMER_ID = cusId
    new_trans.SHOP_ID = shopId
    new_trans.OVERALL_RATE = shopStar
    new_trans.ASST_SVC_RATE = shopAsstStar
    new_trans.COMMENTS =  reviewText
    new_trans.save()
    return True
