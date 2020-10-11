import os
import json
import requests
import jmespath
import gzip
import base64
from pprint import pprint

event = {"awslogs": {"data": "H4sIAFMP8V4C/+1WW2/bNhT+K4aBDS0WySRFXYNi0JImMZp0aexuS5uioEjK4SqLHiXFaQP/9x1RvqSrc0HRh24Y/GCR58rD8308N/2prCo2keOPM9lP+vvpOH1/8nw0Sg+f93f6el5KA9uYeNQPwiiGD9gu9OTQ6GYGklpW9fFqaSWj2kg23YiW651+1WQVN2pWK10eqKKWpuonb61at+y/sw6eX8mybkU3fSXAj2zXQ4HBRa0g3ZpNITKmFFFK4ihECO2sjgHqNxedxW/gHyJd9JOLPnaRf9Hfueg3lTRDAVJVfwQJ6NZwcKtzpnVtdWZGlVzNWDEUVhAFlOIYR8RDoVVgpvMK/wmbV4li0yS5rZWYlS/GuW7a7O/wxDnk/UJ+XCqko2FKR6+8g8A789+cvz7//ehXq1iBGhxmT5e1vK67zJd7w6pqpGm3FqA4l9lQHEghDWvrvM9qthKxujYqa6Denf00Z2lTX7bF4KyWXQa1aaSNyOHWlh66+hBEkIMCB8djHCQUJ5i8uegvFq1rW/AxXM4/NYmXUJKg4I31adVGujG8U4TCuWzKPukSyuhyPd1ovWRLZ6kQr+HSxtq2WFe1eXUmJ6u7bSpHsqp2cFco6314CmYG6tPdPolcHMcu8T0XU2/dCOkEAlkNrstKF3JLMkb+1UDLnTIDCbUt29Vu0iazzpGJqSpVVUPNtVm73y6eaAYxF9Z1NYO48nkhp23Hg27ZFMUm6HC/M0dZHuSEOjlisUP9DDuZwLnDMxwJlgcRJXhTuKVRhrkf55w5IfKkQyUTTsRZ6GAfBz4hWcz9bGM0XoEgnVfpTO2xolieHoCgQCG9p48XcJrPoUruhir+FlAdpidtT2xFazrcX0Po1Zich2l49OKRsG1DDnL2p1HwcSVNYTvoK2D8YgPjs19eHZ8fjQ+/bIsvAt2DpGiMaOJHCQm3I0ly8jCSAOzaqE9yJHljoKoWUcNyYtbH/AxYbOYAmoAg7kcX5OhGyCWYujjAW8AFXp1KfHAmeoBdD7uk92SisYs9N9ztFapsrnd7bCoC+rSXnr4EHdQ7YtWl2tNmZldjaQzLtZkOkIsJwLj35KfLup5VyWAwn8/deiV3lX76IGqXd1RNHOQzKgnhBEVCChrn1lbNTqWZKsutSztVy2n7+fbGio2uNddFx5e846Tc6OmpNu2JCYF1rW+vbOBqRcRqdsbKidzinCthhjPrGLn2N0DQF+86q6tgY7ewrS9zdX0MzDIU3SZo3sEsNxtW6c4fc8q4yLiDCAWC4MRzoixjDsqkL+IoE6Gg9mTvjawbC532bVh8QU+PdnSbnkTOIoARkFIUgVEYICfLpHQyP/S82JfCx/JfS0/fwyRxH5sQNEYBNGbix9vZpFKTUpUPEspe92rCjKfKr3qYH6SOE/1JFQUb+MACT/7AeLd33PJF7zoK3gd0t2eukjB00dPeoeQf9IAgDFeIcO9AATT09aAV3kkI68d2G1g+PxukMmpshbu6MiFUOxyxwg6rqynrom/1x9parChqPVxAIbuStvVcbQ8u9VT+DK1Yy2eXQHupmVQ/EO9HVTHgXq6FfLaeyU50pgp5ux1f6k5wkMKD2N38ubz9lCzxhkKPMEq542fIc2iAAW9+IB2WZxkSXEYck+14WxZiBC0xLP8fCv4fCv7rQ0EoSY5i5DF41+KQ428zFEQoQrfHguX6OxwMEMU5jWPi4DzH8DTHvpN5LHdIFAmee7nHPPGoweDRjm4TFWZIeDEWDo1i7tCYghEwl+MhHiBYyTjMv91g8G7xN7brA70BEQAA"}}

base64_decoded = base64.b64decode(event['awslogs']['data'])
plain_string  = gzip.decompress(base64_decoded).decode("utf-8")
pprint(plain_string)
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
            # print(path)
            print(query + " is found!")