import json
import random
import requests
import string
import os.path
from Naked.toolshed.shell import muterun_js

referer = "https://www.tiktok.com/"
url = "https://m.tiktok.com/api/post/item_list/?aid=1988&count=30&secUid=MS4wLjABAAAAOUoQXeHglWcq4ca3MwlckxqAe-RIKQ1zlH9NkQkbLAT_h1_6SDc4zyPdAcVdTWZF&cursor=0"

def getsign():
    response = muterun_js(' '.join([os.path.abspath('node_modules/tiktok-signature/browser.js'), "\""+url+"\""]))
    print("(!) Response:")
    print(response.stdout)
    if response.exitcode == 0:
        # the command was successful, handle the standard output
        signature = json.loads(response.stdout)
        print("(!) Signature:")
        print(signature)
        

        return signature
    else:
        standard_err = response.stderr
        exit_code = response.exitcode
        print('Cannot run node script ' + str(exit_code) + ': ' + standard_err)

def gettrend(signature):
    request = requests.get(signature['data']['signed_url'], headers={"method": "GET",
                                                                        "accept-encoding": "gzip, deflate",
                                                                        "Referer": referer,
                                                                        "user-agent": signature['data']['navigator']['user_agent'],
                                                                        "x-tt-params": signature['data']['x-tt-params']
                                                                        })

    data = request.text
    return data