from . import slack
from . import console_print


def send(reciver_id, content_string):
    msg = "______ SENDING TEXT - START _________\n"
    msg += "\t To:"
    msg += "\t "+reciver_id + "\n"
    msg += "\t Message:\n"
    msg += "\t" + content_string + "\n"
    msg += "______ SENDING TEXT - END _________"
    console_print.debug_print(msg)
    #slack.send_msg(msg)

#Sending message to assistance
def notify_assistance(location_relationship, customer, current, target):
    textContent = "Shop:" + target + " Current Position:" + current + " | Position: " + location_relationship + "\n"
    if location_relationship == "self":
        textContent = "STATUS UPDATE, CUSTOMER HAS REACHED SHOP!!!!\n"
        textContent += "\t Mr/Ms Customer:" + customer
        send(target, textContent)
    elif location_relationship == "neighbour":
        textContent = "STATUS INITIALIZATION, CUSTOMER IS COMING....\n"
        textContent += "\t Mr/Ms Customer:" + customer
        send(target, textContent)
