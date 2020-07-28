import requests
import json
import config
import create_db
def UpdateTicket(df):
    flag=True
    for i in range(len(df)):
        x = df.iloc[i]['Incident ID']
        header = {"Token":"46284d7a-7d20-4fd1-8701-91ca8f1ff1aa"}
        URL = "http://103.251.216.101/dat/Complain/ComplainAssignemt"
        data = {
          "Id": 0,
          "AssignmentId": 1,
          "ComplainId": x,
          "UserId": "87a0c901-a950-4704-84a0-72cccb2690e0",
          "ComplainPendingComments": "Resolved By Aforesight",
          "ComplainCloseComments": "Resolved By Aforesight",
          "Observation": df['Status'],
          "ActionTaken": df["Solution"],
          "ComplainStatusId": 6,
          "ComplainClosedBy": "Aforesight",
          "ComplainClosureId": ""
        }
        r1 = requests.post(url = URL, headers = header, data = data)
        try:
            b = r1.json()
        except:
            return False
    return flag

def updatetickets(ticket_id,status,solution):
    config.logger.exception("In update ticket part")
    query = "select * from tickets where `Incident ID` = '"+ticket_id+"';"
    df=create_db.fetchquery(query)
    df.loc[df["Incident ID"]==ticket_id , 'Status'] = status
    df.loc[df["Incident ID"]==ticket_id , 'Solution'] = solution
    print(df)
    ret = create_db.update(df)
    config.logger.exception('data updated in db')

    UpdateTicket(df.loc[df.Status =="Resolved"]) 
    config.logger.exception('ticket updated in itsm')
