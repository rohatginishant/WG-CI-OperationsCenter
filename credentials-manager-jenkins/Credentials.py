import requests
import json
from jenkins_login import data


class Credentials:

    def __init__(self, jenkins_url, auth_username, auth_token):

        self.jenkins_url = jenkins_url
        self.auth_username = auth_username
        self.auth_token = auth_token

        # try:
        #     self.jenkins_crumb = requests.get(crumb_url, auth=(self.auth_username, self.auth_token))
        #     self.crumb = self.jenkins_crumb.json()["crumb"]
        #     if jenkins_crumb is not None:
        #         print("Response received:")
        #         print(response.text)
        #     else:
        #         print("Request timed out")
        # except:
        #     print("ERROR: Failed to establish connection")

    def create_username_with_password(self, id, username, password, usernameSecret, description, crumb_url):

        jenkins_url_createfunction = self.jenkins_url + 'credentials/store/system/domain/_/createCredentials'
        jenkins_crumb = ''

        try:
            jenkins_crumb = requests.get(crumb_url, auth=(self.auth_username, self.auth_token))
            if jenkins_crumb is not None:
                print("Response received:")
            else:
                print("Request timed out")
                return 'Error'
        except:
            print("ERROR: Failed to establish connection")
            return 'Error'

        crumb = jenkins_crumb.json()["crumb"]
        # print(f"Jenkins crumb data = {jenkins_crumb.json()}")

        Head = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Jenkins_Crumb': crumb
        }

        username_set = username
        id_set = id
        password_set = password
        usernamesecret_set = usernameSecret
        description_set = description

        data = {
            "": "0",
            "credentials": {
                "scope": "GLOBAL",
                "username": username_set,
                "usernameSecret": usernamesecret_set,
                "password": password_set,
                "$redact": "password",
                "id": id_set,
                "description": description_set,
                "stapler-class": "com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl",
                "$class": "com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl"
            }
        }

        data = json.dumps(data)

        response = requests.post(jenkins_url_createfunction,
                                 auth=(self.auth_username, self.auth_token),
                                 headers=Head,
                                 data={'json': data},
                                 timeout=1)
        if response.status_code == 200:
            print("Created Credentials successfully")

        return response




    def create_ssh_with_private_key(self, id, description, username, privatekey, usernameSecret, crumb_url):
        jenkins_url_createfunction = self.jenkins_url + 'credentials/store/system/domain/_/createCredentials'

        try:
            jenkins_crumb = requests.get(crumb_url, auth=(self.auth_username, self.auth_token))
            if jenkins_crumb is not None:
                print("Response received:")
            else:
                print("Request timed out")
                return 'Error'
        except:
            print("ERROR: Failed to establish connection")
            return 'Error'

        crumb = jenkins_crumb.json()["crumb"]

        Headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Jenkins_Crumb': crumb
        }

        username_set = username
        id_set = id
        private_key_set = privatekey
        description_set = description
        usernameSecret_set = usernameSecret

        data = {
            "": "3",
            "credentials": {
                "scope": "GLOBAL",
                "id": id_set,
                "description": description_set,
                "username": username_set,
                "usernameSecret": usernameSecret_set,
                "privateKeySource":
                    {
                        "value": "0",
                        "privateKey": private_key_set,
                        "stapler-class": "com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey$DirectEntryPrivateKeySource",
                        "$class": "com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey$DirectEntryPrivateKeySource"
                    },
                "passphrase": "passphrase",
                "$redact": "passphrase",
                "stapler-class": "com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey",
                "$class": "com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey"
            },
        }

        data = json.dumps(data)

        response = requests.post(jenkins_url_createfunction,
                                 auth=(self.auth_username, self.auth_token),
                                 headers=Headers,
                                 data={'json': data})

        if response.status_code == 200:
            print("ssh Credentials created ")

        return response


    def update_username_with__password(self, id, username, password, usernameSecret, description, crumb_url):
        # id = input("Enter id : ")

        try:
            jenkins_crumb = requests.get(crumb_url, auth=(self.auth_username, self.auth_token))
            if jenkins_crumb is not None:
                print("Response received:")
            else:
                print("Request timed out")
                return 'Error'
        except:
            print("ERROR: Failed to establish connection")
            return 'Error'

        crumb = jenkins_crumb.json()["crumb"]

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Jenkins-Crumb': crumb
        }

        update_url = self.jenkins_url + f"credentials/store/system/domain/_/credential/{id}/updateSubmit"

        username_set = username
        id_set = id
        password_set = password
        usernamesecret_set = usernameSecret
        description_set = description

        data = {
            "stapler-class": "com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl",
            "scope": "GLOBAL",
            "username": username_set,
            "usernameSecret": usernamesecret_set,
            "password": password_set,
            "$redact": "password",
            "id": id_set,
            "description": description_set,
            "Submit": "",
        }

        data = json.dumps(data)

        response = requests.post(update_url, auth=(self.auth_username, self.auth_token),
                                  headers=headers,
                                  data={'json': data})

        if response.status_code == 200:
            print("Updated successfully!!")

        return response

    def update_ssh_with__privatekey(self, id, username, privatekey, usernameSecret, description, passphrase, crumb_url):
        # id = input("Enter id : ")
        try:
            jenkins_crumb = requests.get(crumb_url, auth=(self.auth_username, self.auth_token))
            if jenkins_crumb is not None:
                print("Response received:")
            else:
                print("Request timed out")
                return 'Error'
        except:
            print("ERROR: Failed to establish connection")
            return 'Error'

        crumb = jenkins_crumb.json()["crumb"]

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Jenkins-Crumb': crumb
        }

        update_url = self.jenkins_url + f"credentials/store/system/domain/_/credential/{id}/updateSubmit"

        username_set = username
        id_set = id
        privatekey_set = privatekey
        usernamesecret_set = usernameSecret
        description_set = description
        passphrase_set = passphrase

        data = {
            "stapler-class": "com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey",
            "scope": "GLOBAL",
            "id": id_set,
            "description": description_set,
            "username": username_set,
            "usernameSecret": usernamesecret_set,
            "privateKeySource": {
                "value": "0",
                "privateKey": privatekey_set,
                "stapler-class": "com.cloudbees.jenkins.plugins.sshcredentials.impl"
                                 ".BasicSSHUserPrivateKey$DirectEntryPrivateKeySource",
                "$class": "com.cloudbees.jenkins.plugins.sshcredentials.impl"
                          ".BasicSSHUserPrivateKey$DirectEntryPrivateKeySource"
            },
            "passphrase": passphrase_set,
            "$redact": "passphrase",
            "Submit": ""
        }

        data = json.dumps(data)

        response = requests.post(update_url, auth=(self.auth_username, self.auth_token),
                                  headers=headers,
                                  data={'json': data})

        if response.status_code == 200:
            print("Updated successfully!!")

        return response

    def delete(self, id, crumb_url):

        try:
            jenkins_crumb = requests.get(crumb_url, auth=(self.auth_username, self.auth_token))
            if jenkins_crumb is not None:
                print("Response received:")
            else:
                print("Request timed out")
                return 'Error'
        except:
            print("ERROR: Failed to establish connection")
            return 'Error'



        crumb = jenkins_crumb.json()["crumb"]

        Headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Jenkins-Crumb': crumb
        }

        jenkins_url_deletefunction = self.jenkins_url + f'credentials/store/system/domain/_/credential/{id}/doDelete'
        response = requests.post(jenkins_url_deletefunction, auth=(self.auth_username, self.auth_token),
                                  headers=Headers)
        print(response.status_code)
        if response.status_code == 200:
            return ' Credentials Deleted '

        return response

    def get_credentials(self, crumb_url):

        try:
            jenkins_crumb = requests.get(crumb_url, auth=(self.auth_username, self.auth_token))
            if jenkins_crumb is not None:
                print("Response received:")
            else:
                print("Request timed out")
                return 'Error'
        except:
            print("ERROR: Failed to establish connection")
            return 'Error'

        crumb = jenkins_crumb.json()["crumb"]
        Headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Jenkins-Crumb': crumb
        }

        url = self.jenkins_url + 'credentials/store/system/domain/_/api/json?tree=credentials[id,description,typeName,displayName]'
        response = requests.get(url,auth=(self.auth_username,self.auth_token), headers=Headers)
        return response

    def create_pod(self, crumb_url, name, label, timeoutSeconds):

        jenkins_url_createpod = self.jenkins_url + 'configureClouds/configure'
        try:
            jenkins_crumb = requests.get(crumb_url, auth=(self.auth_username, self.auth_token))
            if jenkins_crumb is not None:
                print("Response received:")
            else:
                print("Request timed out")
                return 'Error'
        except:
            print("ERROR: Failed to establish connection")
            return 'Error'

        crumb = jenkins_crumb.json()["crumb"]
        print(crumb)
        # print(f"Jenkins crumb data = {jenkins_crumb.json()}")

        Head = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Jenkins_Crumb': crumb
        }

        print(name)
        name_set = name,
        label_set = label,
        timeout_set = timeoutSeconds,


        data = {
   "cloud":{
      "stapler-class":"org.csanchez.jenkins.plugins.kubernetes.KubernetesCloud",
      "$class":"org.csanchez.jenkins.plugins.kubernetes.KubernetesCloud",
      "name":"kubernetes",
      "serverUrl":"",
      "useJenkinsProxy":False,
      "serverCertificate":"",
      "skipTlsVerify":False,
      "namespace":"",
      "jnlpregistry":"",
      "includeUser":"False",
      "credentialsId":"",
      "webSocket":False,
      "directConnection":False,
      "jenkinsUrl":"",
      "jenkinsTunnel":"",
      "connectTimeout":"5",
      "readTimeout":"15",
      "containerCapStr":"10",
      "podLabels":{
         "stapler-class":"org.csanchez.jenkins.plugins.kubernetes.PodLabel",
         "$class":"org.csanchez.jenkins.plugins.kubernetes.PodLabel",
         "key":"jenkins",
         "value":"slave"
      },
      "":"1",
      "podRetention":{
         "stapler-class":"org.csanchez.jenkins.plugins.kubernetes.pod.retention.Never",
         "$class":"org.csanchez.jenkins.plugins.kubernetes.pod.retention.Never"
      },
      "maxRequestsPerHostStr":"32",
      "waitForPodSec":"600",
      "retentionTimeout":"5",
      "addMasterProxyEnvVars":False,
      "usageRestricted":False,
      "defaultsProviderTemplate":"",
      "templates":{
         "id":"",
         "name":name,
         "namespace":"",
         "label":label,
         "nodeUsageMode":"EXCLUSIVE",
         "inheritFrom":"",
         "containers":{
            "stapler-class":"org.csanchez.jenkins.plugins.kubernetes.ContainerTemplate",
            "$class":"org.csanchez.jenkins.plugins.kubernetes.ContainerTemplate",
            "name":"container_name_set",
            "image":"docker_image_set",
            "alwaysPullImage":False,
            "workingDir":"working_directory_set",
            "command":"command_set",
            "args":"arguments_set",
            "ttyEnabled":"ttyset",
            "privileged":False,
            "runAsUser":"",
            "runAsGroup":"",
            "resourceRequestCpu":"",
            "resourceRequestMemory":"",
            "resourceRequestEphemeralStorage":"",
            "resourceLimitCpu":"",
            "resourceLimitMemory":"",
            "resourceLimitEphemeralStorage":"",
            "livenessProbe":{
               "execArgs":"",
               "initialDelaySeconds":"initialDelay_Set",
               "timeoutSeconds":"timeout_set",
               "failureThreshold":"failure_threshhold_set",
               "periodSeconds":"period",
               "successThreshold":"successthreshhold_set"
            }
         },
         "":[
            "",
            "1",
            "1",
            "1"
         ],
         "instanceCapStr":"",
         "podRetention":{
            "stapler-class":"org.csanchez.jenkins.plugins.kubernetes.pod.retention.Default",
            "$class":"org.csanchez.jenkins.plugins.kubernetes.pod.retention.Default"
         },
         "idleMinutesStr":"",
         "activeDeadlineSecondsStr":"",
         "slaveConnectTimeoutStr": timeoutSeconds,
         "yaml":"",
         "yamlMergeStrategy":{
            "stapler-class":"org.csanchez.jenkins.plugins.kubernetes.pod.yaml.Overrides",
            "$class":"org.csanchez.jenkins.plugins.kubernetes.pod.yaml.Overrides"
         },
         "showRawYaml":True,
         "serviceAccount":"",
         "runAsUser":"",
         "runAsGroup":"",
         "supplementalGroups":"",
         "hostNetwork":False,
         "nodeSelector":"node_selector_set",
         "workspaceVolume":{
            "memory":False,
            "stapler-class":"org.csanchez.jenkins.plugins.kubernetes.volumes.workspace.EmptyDirWorkspaceVolume",
            "$class":"org.csanchez.jenkins.plugins.kubernetes.volumes.workspace.EmptyDirWorkspaceVolume"
         },
         "nodeProperties":{
            "stapler-class-bag":"true"
         }
      }
   },
   "Submit":"",
   "core:apply":""
}

        data = json.dumps(data)

        response = requests.post(
            jenkins_url_createpod,
            auth=(self.auth_username, self.auth_token),
            headers=Head,
            data={'json': data}
        )

        print(response.status_code)
        print(response.text)

        if response.status_code == 200:
            print("Pod created ")

        return response


# url = 'http://44.212.71.109:8080/manage/credentials/store/system/domain/_/'
#
# with open('config.xml', 'r') as file:
#     xml_data = file.read()
#
# obj1 = credentials(url, 'admin', '1187c4bb500c1cf2595c14fde4f06e0668')
# obj1.create('ppppp', 'bbbbbbbbbb', 'ccccccc')
