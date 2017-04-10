import datetime
from pingow_api  import models as m
from pingow_api.core  import constants as c
# trans_id = 0
def create_trans_id(cusId, shopId, productCatId):
    # global trans_id
    # last_trans = m.CustomerTransaction.objects.all().order_by('-TRANSACTION_ID')
    # if len(last_trans) == 0:
    #     new_trans_id = 1
    # else:
    #     new_trans_id = last_trans[0].TRANSACTION_ID + 1

    #new trans id
    random = int(datetime.datetime.now().strftime("%f")) % 100
    print(random)
    timestamp = datetime.datetime.now().strftime("%d%H%M%S")
    new_trans_id = int(timestamp) + random

    #create new record
    new_trans = m.CustomerTransaction(
        TRANSACTION_ID = new_trans_id,
        CUSTOMER_ID = cusId,
        SHOP_ID = shopId,
        SUB_CAT_ID = productCatId,
        CREATION_DATE =  datetime.datetime.now().strftime(c.DATE_FMT),
        OVERALL_RATE = 0,
        ASST_SVC_RATE = 0,
        )
    new_trans_status = m.CustomerTransactionStatus(
        TRANSACTION_ID = new_trans_id,
        STATUS = 'outside shop'
        )
    new_trans.save()
    new_trans_status.save()
    # trans_id = next_trans_id + 1
    print('----- ----- returning trx ID:',new_trans_id,' | for cus :', cusId)
    return new_trans_id


def update_trans_asst_id (trxId, asst_id):
    new_trans = m.CustomerTransaction.objects.get(TRANSACTION_ID = trxId)
    new_trans.ASST_ID = asst_id
    new_trans.save(
        update_fields = ['ASST_ID']
    )
    print("update trans commit>>:", 'trxId', trxId,'asst_id',asst_id)
    return True


def update_trans (trxId, cusId, shopId, shopStar, shopAsstStar, reviewText):
    new_trans = m.CustomerTransaction.objects.get(TRANSACTION_ID = trxId)
    new_trans.CUSTOMER_ID = cusId
    new_trans.SHOP_ID = shopId
    new_trans.OVERALL_RATE = int(shopStar) - 3
    new_trans.ASST_SVC_RATE = int(shopAsstStar) -3
    new_trans.COMMENTS =  reviewText
    new_trans.save(
        update_fields = ['CUSTOMER_ID' , 'SHOP_ID', 'ASST_ID', 'OVERALL_RATE', 'ASST_SVC_RATE', 'COMMENTS']
    )
    print("update trans commit>>:", 'trxId', trxId,'cusId',cusId,'shopId',shopId,'shopStar',shopStar,"shopAsstStar",shopAsstStar,"reviewText",reviewText )
    return True
