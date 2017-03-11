import requests
##import paho.mqtt.client as mqtt
import datetime
import sys
import json

from slackclient import SlackClient

##########################################################
##########################################################
##########################################################

# globals

_slack_sysmon_channel = '#general'
_slack_bot_api_token = 'xoxp-149767781813-148973185344-149005408977-5cc74114fa3cf27f134edabcb958f804'
_slack_client = SlackClient(_slack_bot_api_token)

##########################################################
##########################################################
##########################################################

def usage():

	print ('Usage: python mq_demux.py <config_filename>')
	sys.exit(1)

##########################################################
##########################################################
##########################################################

def send_slack_msg(sc, channel, text):

	bot_name = '7bot'
	bot_icon_emoji = ':dizzy:' # ':sparkles:'

	res = sc.api_call("chat.postMessage", channel=channel, text=text, username=bot_name, icon_emoji=bot_icon_emoji)
	if (str(res['ok']).lower() == 'true'):
		return 0

	# not doing sys exit cos other mqtt processes can continue even if slack fails
	print ('!!! ERROR: Sending slack msg failed; check token API?')
	return 1

##########################################################
##########################################################
##########################################################

def send_msg (text):
	send_slack_msg(_slack_client, _slack_sysmon_channel, text)

# if __name__ == '__main__':
#
# 	print 'starting main...'
#
# 	send_slack_msg(_slack_client, _slack_sysmon_channel, 'hello world! :)')
