import os
import json
import requests
import jmespath
import gzip
import base64


def lambda_handler(event, context):
    print(event)
    base64_decoded = base64.b64decode(event['awslogs']['data'])
    plain_string  = gzip.decompress(base64_decoded).decode("utf-8")
    log_events = json.loads(plain_string)['logEvents']
    print('Event count: ' + str(len(log_events)))
    for event in log_events:
        print(event['message'])
        # rule
        queries = {
            'ssh-open-to-world':'requestParameters.ipPermissions.items[?ipProtocol == `tcp` && fromPort == `22` && toPort == `22` && ipRanges.items[?cidrIp==`0.0.0.0/0`]]',
            'non-standard-port-is-open-to-world':'requestParameters.ipPermissions.items[?ipProtocol == `tcp` && ((fromPort != `22` && toPort != `22`) && (fromPort != `80` && toPort != `80`) && (fromPort != `443` && toPort != `443`)) && ipRanges.items[?cidrIp==`0.0.0.0/0`]]',
            'root-console-login':'eventName == `ConsoleLogin` && userIdentity.type == `Root`',
            'new-user-added-to-administrator-group':'eventName == `AddUserToGroup` && requestParameters.groupName == `administrator`',
        }

        for query in queries:
            event_dict = json.loads(event['message'])
            path = jmespath.search(queries[query], event_dict)
            if path:
                print(query + " is found!")
                send_slack_message(query, json.dumps(event_dict, indent=4))


def send_slack_message(event_type, json_message):
    # https://gist.github.com/devStepsize/b1b795309a217d24566dcc0ad136f784
    webhook_url = os.environ['WEBHOOK_URL']

    slack_data = {
        "channel": "#aws-security",
        "username": "securitybot",
        "icon_emoji": "ghost",
        "text": "New security event",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "New security event detected : *" + event_type + "* :warning: @here"
                }
            },
            {
                "type": "section",
                "block_id": "section567",
                "text": {
                    "type": "mrkdwn",
                    "text": "```" + json_message + "```"
                },
            }
        ]
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
