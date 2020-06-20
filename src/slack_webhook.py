import os
import json
import requests

# https://gist.github.com/devStepsize/b1b795309a217d24566dcc0ad136f784

webhook_url = os.environ['WEBHOOK_URL']
slack_data = {
    'username': 'securitybot',
    'icon_emoji': 'ghost',
    'text': "This is a security message :warning:"
}

response = requests.post(
    webhook_url, data=json.dumps(slack_data),
    headers={'Content-Type': 'application/json'}
)
if response.status_code != 200:
    raise ValueError(
        'Request to slack returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )