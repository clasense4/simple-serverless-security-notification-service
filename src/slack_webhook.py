import os
import json
import requests
import jmespath

events = {
    1 : 'events/ssh-open-to-world.json',
    2 : 'events/port-8080-open-to-world.json',
    3 : 'events/root-console-login.json',
    4 : 'events/user-add-to-admin-group.json'
}

with open(events[4]) as f:
    event = json.load(f)
# print(event)

queries = {
    'ssh-open-to-world':'requestParameters.ipPermissions.items[?ipProtocol == `tcp` && fromPort == `22` && toPort == `22` && ipRanges.items[?cidrIp==`0.0.0.0/0`]]',
    'non-standard-port-is-open-to-world':'requestParameters.ipPermissions.items[?ipProtocol == `tcp` && ((fromPort != `22` && toPort != `22`) && (fromPort != `80` && toPort != `80`) && (fromPort != `443` && toPort != `443`)) && ipRanges.items[?cidrIp==`0.0.0.0/0`]]',
    'root-console-login':'eventName == `ConsoleLogin` && userIdentity.type == `Root`',
    'new-user-added-to-administrator-group':'eventName == `AddUserToGroup` && requestParameters.groupName == `administrator`',
}

for query in queries:
    path = jmespath.search(queries[query], event)
    if path:
        print(query + " is found!")

# https://gist.github.com/devStepsize/b1b795309a217d24566dcc0ad136f784
# webhook_url = os.environ['WEBHOOK_URL']
# slack_data = {
#     'username': 'securitybot',
#     'icon_emoji': 'ghost',
#     'text': "This is a security message :warning: <!here>"
# }

# response = requests.post(
#     webhook_url, data=json.dumps(slack_data),
#     headers={'Content-Type': 'application/json'}
# )
# if response.status_code != 200:
#     raise ValueError(
#         'Request to slack returned an error %s, the response is:\n%s'
#         % (response.status_code, response.text)
#     )