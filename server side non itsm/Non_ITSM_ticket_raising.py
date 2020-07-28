import requests
import json
def raiseTicket(name,email,phno,description):
    header = {"Token":"46284d7a-7d20-4fd1-8701-91ca8f1ff1aa"}
    URL = "http://103.251.216.101/dat/Complain/RegisterComplain"

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