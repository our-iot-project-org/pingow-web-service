import requests
# import paho.mqtt.client as mqtt
import datetime
import sys
import json
from . import para

from slackclient import SlackClient

##########################################################
##########################################################
##########################################################

# globals

_slack_sysmon_channel = para._slack_sysmon_channel
_slack_bot_api_token = para._slack_bot_api_token
_slack_client = SlackClient(_slack_bot_api_token)
_slack_user = '@iamhanying'


##########################################################
##########################################################
##########################################################

def usage():

    print('Usage: python mq_demux.py <config_filename>')
    sys.exit(1)

##########################################################
##########################################################
##########################################################


def send_slack_msg(sc, receiver_id, text):
    bot_name = 'Pingow_Friend'
    bot_icon_emoji = ':dog:'  # ':sparkles:'

    res = sc.api_call("chat.postMessage", channel=receiver_id,
                      text=text, username=bot_name, icon_emoji=bot_icon_emoji)
    if (str(res['ok']).lower() == 'true'):
        return 0

    # not doing sys exit cos other mqtt processes can continue even if slack
    # fails
    print('!!! ERROR: Sending slack msg failed; check token API?')
    return 1

##########################################################
##########################################################
##########################################################


def send_msg(text):
	send_slack_msg(_slack_client, '#general', text)
	#send_slack_msg(_slack_client, _slack_user, text)
	send_slack_msg(_slack_client, '@zen', text)
	return
