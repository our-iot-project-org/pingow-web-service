from . import constants

def get_position_relationship(positionA, positionB):
    relationship = constants.POSITION_REL_NO
    #shopnames
    shop01 = "2"
    shop02 = "0"
    shop03 = "1"
    shop04 = "00"
    shop05 = "3"
    #mocking data for position relationship
    if ((positionA == "") | (positionB == "")):
        return constants.VALUE_NULL
    if ((positionA == shop01) & ((positionB == shop03) | (positionB == shop05)) ):
        return constants.POSITION_REL_NEARBY
    if ((positionA == shop02) & (positionB == shop04)):
        return constants.POSITION_REL_NEARBY
    if ((positionA == shop03) & (positionB == shop05)):
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
