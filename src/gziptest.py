import os
import json
import requests
import jmespath
import gzip
import base64

event = {"awslogs": {"data": "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"}}

base64_decoded = base64.b64decode(event['awslogs']['data'])
plain_string  = gzip.decompress(base64_decoded).decode("utf-8")
log_events = json.loads(plain_string)['logEvents']
print('Event count: ' + str(len(log_events)))
for event in log_events:
    # print(event['message'])
    queries = {
        'ssh-open-to-world':'requestParameters.ipPermissions.items[?ipProtocol == `tcp` && fromPort == `22` && toPort == `22` && ipRanges.items[?cidrIp==`0.0.0.0/0`]]',
        'non-standard-port-is-open-to-world':'requestParameters.ipPermissions.items[?ipProtocol == `tcp` && ((fromPort != `22` && toPort != `22`) && (fromPort != `80` && toPort != `80`) && (fromPort != `443` && toPort != `443`)) && ipRanges.items[?cidrIp==`0.0.0.0/0`]]',
        'root-console-login':'eventName == `ConsoleLogin` && userIdentity.type == `Root`',
        'new-user-added-to-administrator-group':'eventName == `AddUserToGroup` && requestParameters.groupName == `administrator`',
    }

    for query in queries:
        # print(queries[query])
        path = jmespath.search(queries[query], json.loads(event['message']))
        # print(path)
        if path:
            print(path)
            print(query + " is found!")