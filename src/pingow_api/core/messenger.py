from . import slack
from . import console_print
from pingow_api.core import constants as c
from pingow_api import models as m

def send(reciver_id, content_string):
    msg = content_string
    console_print.debug_print(msg)
    print('send>>>', msg)
    slack.send_msg(msg)

#Sending message to assistance
def notify_assistance(location_relationship, customerId, current, target):
    customer_obj = m.Customer.objects.get(CUSTOMER_ID = customerId)
    customer_name = customer_obj.CUSTOMER_NAME
    gender = customer_obj.GENDER
    language = customer_obj.PREF_LANG_1

    textContent = "Shop:" + target + " Current Position:" + current + " | Position: " + location_relationship + "\n"
    print('notify_assistance>>',textContent)
    if location_relationship == c.POSITION_REL_NEARBY:
        textContent = "======= Alert #01 Reaching Soon =======\n"
        textContent += "Customer Name: " + customer_name + "\n"
        textContent += "Type: " + "Wheelchair" + "\n"
        textContent += "Gender: " + gender + "\n"
        textContent += "Language: " + language + "\n"
        send(target, textContent)
    elif location_relationship == c.POSITION_REL_TARGET:
        textContent = "======= Alert #02 Customer is here. =======\n"
        textContent += "Customer Name: " + customer_name + "\n"
        textContent += "Type: " + "Wheelchair" + "\n"
        textContent += "Gender: " + gender + "\n"
        textContent += "Language: " + language + "\n"
        send(target, textContent)
