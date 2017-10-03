from slackclient import SlackClient
import time

slack_token = "xoxb-250060359537-getPupq0kpkpkeB9EKLT33oO"
#slack_token = "xoxp-149305494882-149342893540-250577962082-070c2e7a3ae2751237d5382bd9ce5036"
sc = SlackClient(slack_token)

if sc.rtm_connect(with_team_state=False):
    while True:
        print sc.rtm_read()
        time.sleep(0.2)
        #sc.rtm_send_message("#general", "test")
        sc.api_call("chat.postMessage", channel="D7DDN4CUE", text="Cmon", username="holmerbot")
else:
    print "Connection Failed"