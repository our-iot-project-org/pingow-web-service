from . import slack


def send(reciver_id, content_string):
    msg = "______ SENDING TEXT - START _________\n"
    msg += "\t To:"
    msg += "\t "+reciver_id + "\n"
    msg += "\t Message:\n"
    msg += "\t" + content_string + "\n"
    msg += "______ SENDING TEXT - END _________"
    print(msg)
    slack.send_msg(msg)
