import requests
import json
import configparser
config = configparser.ConfigParser()
config.read('config_test.ini')
def raiseTicket(name,email,phno,description):
    header = {"Token":config["DEFAULT"]["token"]}
    URL = config["DEFAULT"]["api key"]+"RegisterComplain"
    print(URL)
    data = {
      "Id": 0,
      "ComplainNo": "AFS10012381",
      "ContactPerson": name,
      "ContactPersonEmail": email,
      "ContactPersonPhoneNumber": phno,
      "ProblemDescription": description,
      "SerialNo": "123",
      "ComplainStatusId": 1,
      "LocationMasterId": 1,
      "ComplainTypeId": 1,
      "ModelTypeId": 1,
      "ProblemTypeId": 1,
      "ProblemSubTypeId": 63,
      "PriorityId": 4,

    }

    r1 = requests.post(url = URL, headers = header, data = data)
    return r1.json()