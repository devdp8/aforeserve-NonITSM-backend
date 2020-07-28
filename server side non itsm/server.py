from flask import Flask, request, render_template, jsonify
import random
from apscheduler.schedulers.background import BackgroundScheduler
import Non_ITSM_ticket_raising
from predict import *
import pandas as pd
import create_db
import mail_send
import Non_ITSM_ticket_updation

app = Flask(__name__)

@app.route('/newt/<subject>/<description>/<requester_name>/<macid>', methods = ['GET','POST'])
def newt(subject, description, requester_name, macid):
    print(subject, description, requester_name, macid)
    r_json = Non_ITSM_ticket_raising.raiseTicket("sunny singh","hardik.seth@prithvi.ai","9911750445",description)
    print(r_json)
    t_id = r_json['Id']
#     t_id = "456"
    print(t_id)
    predict(macid)
    mail_send.raiseticket('hardik.seth@prithvi.ai','issue',str(t_id))
    return str(t_id)

@app.route('/inoutserver/<macid>')
def inoutserver(macid):
    df = create_db.getuser_Data()
    df = df.loc[df['MAC_ID']==macid]
    print(df)
    ins = df['IN_SERVER'].values[0]
    outs = df['OUT_SERVER'].values[0]
    print(ins,outs)
    data = {
        'inserver':str(ins),
        'outserver':str(outs)
    }
    return jsonify({'inserver':str(ins),'outserver':str(outs)})

@app.route('/userdetails/<key>/<Hostname>/<IP_Address>/<MAC_ID>/<Serial_Number>/<OS_Version>/<Laptop_Desktop>/<IN_SERVER>/<OUT_SERVER>/<Direct_Printers>/<User_Name>', methods=['GET', 'POST'])
def userdetail(key,Hostname, IP_Address, MAC_ID, Serial_Number, OS_Version, Laptop_Desktop, IN_SERVER, OUT_SERVER, Direct_Printers, User_Name):
    if key == 'old':
        print(Hostname, IP_Address, MAC_ID, Serial_Number, OS_Version, Laptop_Desktop, IN_SERVER, OUT_SERVER, Direct_Printers, User_Name)
        df = create_db.getuser_Data()
        if len(df.loc[df["MAC_ID"] == MAC_ID])>0:
            create_db.adduser_update(Hostname, IP_Address, MAC_ID, Serial_Number, OS_Version, Laptop_Desktop, IN_SERVER, OUT_SERVER, Direct_Printers, User_Name)
        else:
            create_db.adduser_details(Hostname, IP_Address, MAC_ID, Serial_Number, OS_Version, Laptop_Desktop, IN_SERVER, OUT_SERVER, Direct_Printers, User_Name)
        return "done"
    elif key == 'new':
        query = "insert into userdetails values('1','1','"+str(MAC_ID)+"','1','1','1','outlook.office365.com','smtp.office365.com','1','1');"
        res = create_db.createnewuser(query)
        return 'done'

@app.route('/oldt/<tid>', methods = ['GET', 'POST'])
def oldt(tid):
    query = "select * from tickets where `Incident ID` = '"+str(tid)+"';"
    df = create_db.fetchquery(query)
    text = 'You had '+str(df.loc[df["Incident ID"] == str(tid)].Description.values[0])+' issue and status is '+str(df.loc[df["Incident ID"] == str(tid)].Status.values[0])
    return text

@app.route('/upt/<tid>', methods = ['GET','POST'])
def upt(tid):
    outp = create_db.updatenew(tid)
#     df = create_db.get_data()
    query = "select * from tickets where `Incident ID` ='"+str(tid)+"';"
    print(query)
    df = create_db.fetchquery(query)
    print(df["Issue_Class"][0])
    Non_ITSM_ticket_updation.updatetickets(str(tid),'Resolved','Issue has been successfully resolved')
    mail_send.updateticket("hardik.seth@prithvi.ai",df["Issue_Class"][0],str(tid))
    if outp == 'Updated':
        return 'Ticket resolved successfully'
    else:
        return 'Some Error While Resolving Issue'
    return 'Ticket resolved successfully'


@app.route('/know/<macid>',methods = ['GET','POST'])
def know(macid):
    query = "select * from tickets where MAC_ID = '"+macid+"';"
    df = create_db.fetchquery(query)
    df = df.to_json()
    return df

@app.route('/getalluniqueid', methods = ['GET','POST'])
def getall():
    query = 'select MAC_ID from userdetails'
    df = create_db.fetchquery(query)
    df = df.to_json()
    return df
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 7006)