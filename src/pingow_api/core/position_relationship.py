from . import constants
from pingow_api import models as m

def get_position_relationship(positionA, positionB):
    relationship = constants.POSITION_REL_NO
    # shopnames
    shop01 = "1"
    shop02 = "2"
    shop03 = "3"
    shop04 = "00"
    shop05 = "4"
    # mocking data for position relationship
    if ((positionA == "") | (positionB == "")):
        return constants.VALUE_NULL
    if ((positionA == shop01) & ((positionB == shop03) | (positionB == shop05))):
        return constants.POSITION_REL_NEARBY
    if ((positionA == shop02) & (positionB == shop04)):
        return constants.POSITION_REL_NEARBY
    if ((positionA == shop03) & (positionB == shop01)):
        return constants.POSITION_REL_NEARBY
    if ((positionA == shop04) & (positionB == shop05)):
        return constants.POSITION_REL_NEARBY
    if ((positionA == shop05) & (positionB == shop04)):
        return constants.POSITION_REL_NEARBY
    if ((positionA == shop05) & (positionB == shop04)):
        return constants.POSITION_REL_NEARBY
    if (positionA == positionB):
        return constants.POSITION_REL_TARGET
    return constants.VALUE_UNDEFINED

def update_position_status(trans_id, currentPos, targetPos):
    print('---------------------------------------------')

    #Position to shop status
    # POSITION_STATUS_OUTSIDE = 'outside shop'
    # POSITION_STATUS_ENTER = 'enter shop'
    # POSITION_STATUS_EXIT = 'exit shop'
    cus_trans_id_obj = m.CustomerTransactionStatus.objects.get(TRANSACTION_ID = trans_id)


    # checks if key exists
    # if trans_id not in movement_status_dict:
    #     movement_status_dict[trans_id] = 'outside shop'

    # else:
    # get current status
    status = cus_trans_id_obj.STATUS
    new_status = status
    print("original status:",status, ", new status:",new_status)
    if status == 'outside shop' and currentPos == targetPos:
        new_status = 'enter shop'
    elif status == 'enter shop' and currentPos != targetPos:
        new_status = 'exit shop'
    else:
        new_status = 'outside shop'

    print('update status: ',new_status)
    cus_trans_id_obj.STATUS = new_status
    cus_trans_id_obj.save(
        update_fields = ['STATUS']
    )

def get_position_status(trans_id):
    cus_trans_id_obj = m.CustomerTransactionStatus.objects.get(TRANSACTION_ID = trans_id)
    status = cus_trans_id_obj.STATUS
    print('get position status:', status)
    return cus_trans_id_obj.STATUS
