def get_position_relationship(positionA, positionB):
    relationship = "no"
    #shopnames
    shop01 = "1 KFC"
    shop02 = "2 SONY"
    shop03 = "3 APPLE"
    shop04 = "4 BATA"
    shop05 = "5 SAMSUNG"
    #mocking data for position relationship
    if ((positionB == "") | (positionB == "")):
        return "nill"
    if ((positionA == shop01) & ((positionB == shop03) | (positionB == shop05)) ):
        return "neighbour"
    if ((positionA == shop02) & (positionB == shop04)):
        return "neighbour"
    if ((positionA == shop03) & (positionB == shop05)):
        return "neighbour"
    if ((positionA == shop04) & (positionB == shop05)):
        return "neighbour"
    if ((positionA == shop05) & (positionB == shop04)):
        return "neighbour"
    if ((positionA == shop05) & (positionB == shop04)):
        return "neighbour"
    if (positionA == positionB):
        return "self" 
