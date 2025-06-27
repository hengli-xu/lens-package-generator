import os
import json


cmd = """
beyond-curl -XPOST https://bizzy.stage.sqprod.co/admin/get-entity \
  -H "accept: application/json" \
  -H "content-type: application/json" \
  -d '{ "identifier": { "type": "MERCHANTEIN", "token": "M_y5cyirxh" } }'
"""


cmd1 = """
 beyond-curl -XPOST  https://toolbox.stage.sqprod.co/api/call/rewardly/GetReward \
  -H 'accept: application/json, text/plain, */*' \
  -H 'content-type: application/json;charset=UTF-8' \
  -d '{"reward_token":"CR_41ltnodoohk9qqgdqhg1xs8jz"}'
"""
result = os.popen(cmd1)
res = result.read()
json = json.loads(res)
print("-----------")
print(json)
