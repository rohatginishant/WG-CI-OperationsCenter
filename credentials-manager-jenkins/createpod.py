import requests
from Credentials import Credentials

crumb = "http://3.89.107.140:8080//crumbIssuer/api/json"
ans = requests.get(crumb,auth=("admin","113588770900e2413bceec66400c9207ba"))
a = ans.json()["crumb"]

#
obj1 = Credentials(jenkins_url="http://3.89.107.140:8080/manage/",auth_username= "admin",auth_token= "113588770900e2413bceec66400c9207ba",
                   crumb_url="http://3.89.107.140:8080//crumbIssuer/api/json")
print(obj1.create_pod("http://3.89.107.140:8080//crumbIssuer/api/json",
                      "Nishantnewpod77", "label", "2000"))