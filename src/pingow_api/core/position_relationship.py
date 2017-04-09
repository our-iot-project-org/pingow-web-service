from . import constants


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


movement_status_dict = {'trans_id': 'status_outside_enter_exit'}
def update_position_status(trans_id, currentPos, targetPos):
    global movement_status_dict
    print('Before IF',movement_status_dict)
    if (trans_id in movement_status_dict):
        print('After IF',movement_status_dict)
        if (currentPos == targetPos):
            print('Compare = ',movement_status_dict)
            # When reach shop, update to enter.
            movement_status_dict[trans_id] = constants.POSITION_STATUS_ENTER
        elif (movement_status_dict[trans_id]== constants.POSITION_STATUS_ENTER):
            print('Mark Enter',movement_status_dict)
            # if current status is enter, update to exit. else ignore.
            movement_status_dict[trans_id] = constants.POSITION_STATUS_EXIT
    else:
        print('Else',movement_status_dict)
        movement_status_dict[trans_id] = constants.POSITION_STATUS_OUTSIDE

def get_position_status(trans_id):
    global movement_status_dict
    if (trans_id in movement_status_dict):
        return movement_status_dict[trans_id]
    else:
        return constants.POSITION_STATUS_OUTSIDE
