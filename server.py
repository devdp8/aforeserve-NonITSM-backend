from flask import Flask, request, render_template, jsonify
import random
from apscheduler.schedulers.background import BackgroundScheduler
import Non_ITSM_ticket_raising
from predict import *
import pandas as pd
import create_db
import mail_send
import Non_ITSM_ticket_updation
import assign_NON_ITSM
import configparser
from check_licensing import checklicense
import sys
import time

def run():
    config = configparser.ConfigParser()
    config.read('config_test.ini')
    
    app = Flask(__name__)
    
    # route to store fedback in the database
    @app.route('/feedback/<text>/<macid>/<tid>', methods = ['GET','POST'])
    def feedback(text,macid,tid):
        print(text,macid,tid)
        ok = create_db.feedback(text,macid,tid)
        return ok
    
    @app.route('/emailadd/<em>/<macid>',methods = ['GET','POST'])
    def emailadd(em,macid):
        print(em,macid)
        ret = create_db.emaildb(em,macid)
        return ret
    @app.route('/newt/<subject>/<description>/<macid>', methods = ['GET','POST'])
    def newt(subject, description, macid):
        print(subject, description, macid)
        query = "select emailid from userdetails where MAC_ID = '"+macid+"';"
        df = create_db.fetchquery(query)
        email = df.iloc[0]["emailid"]
        r_json = Non_ITSM_ticket_raising.raiseTicket( config["DEFAULT"]["name nonitsm"],email, config["DEFAULT"]["number nonitsm"],description)
        print(r_json)
        t_id = r_json['Id']
    #     t_id = "456"
        print(t_id)
        predict(macid)
        mail_send.raiseticket(str(email),'issue',str(t_id))
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
    
    @app.route('/configdata', methods = ['GET','POST'])
    def configdata():
        inserver = config["DEFAULT"]["incoming server"]
        outserver = config["DEFAULT"]["outgoing server"]
        it_help = config["DEFAULT"]["it helpdesk"]
        policy_url = config["DEFAULT"]["it policy url"]
        return jsonify({'inserver':str(inserver),'outserver':str(outserver),'it_help':str(it_help),'policy_url':str(policy_url)})
    
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
            query = "insert into userdetails values('1','1','"+str(MAC_ID)+"','1','1','1','outlook.office365.com','smtp.office365.com','1','1','sx@gmail.com');"
            res = create_db.createnewuser(query)
            return 'done'
    
    @app.route('/oldt/<tid>', methods = ['GET', 'POST'])
    def oldt(tid):
        query = "select * from tickets where `Incident ID` = '"+str(tid)+"';"
        df = create_db.fetchquery(query)
        text = 'You had '+str(df.loc[df["Incident ID"] == str(tid)].Description.values[0])+' issue and status is '+str(df.loc[df["Incident ID"] == str(tid)].Status.values[0])
        return text
    
    @app.route('/upt/<tid>/<macid>', methods = ['GET','POST'])
    def upt(tid,macid):
        outp = create_db.updatenew(tid)
    #     df = create_db.get_data()
        query = "select * from tickets where `Incident ID` ='"+str(tid)+"';"
        print(query)
        df = create_db.fetchquery(query)
        print(df["Issue_Class"][0])
        Non_ITSM_ticket_updation.updatetickets(str(tid),'Resolved','Issue has been successfully resolved')
        query = "select emailid from userdetails where MAC_ID = '"+macid+"';"
        df2 = create_db.fetchquery(query)
        email = df2.iloc[0]["emailid"]
        mail_send.updateticket(email,df["Issue_Class"][0],str(tid))
        if outp == 'Updated':
            return 'Ticket resolved successfully'
        else:
            return 'Some Error While Resolving Issue'
        return 'Ticket resolved successfully'
    
    @app.route('/assign/<tid>/<macid>', methods = ['GET','POST'])
    def assign(tid,macid):
        outp = create_db.updatenew(tid)
    #     df = create_db.get_data()
        query = "select * from tickets where `Incident ID` ='"+str(tid)+"';"
        print(query)
        df = create_db.fetchquery(query)
        print(df["Issue_Class"][0])
        assign_NON_ITSM.assigntickets(tid)
        query = "select emailid from userdetails where MAC_ID = '"+macid+"';"
        df2 = create_db.fetchquery(query)
        email = df2.iloc[0]["emailid"]
        mail_send.updateticket(email,"Assigned to expert",str(tid))   
        if outp == 'Updated':
            return 'Assigned to Expert.'
        else:
            return 'Some Error While Resolving Issue'
        return 'Assigned to Expert.'
    
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

if checklicense() == True:
    run()
else:
    print("Key Not Correct. Contact Aforeight.")
    time.sleep(5)
    sys.exit(1)