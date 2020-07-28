from sqlalchemy import create_engine
import pandas as pd
engine = create_engine("mysql+pymysql://root:Dev@1234@@127.0.0.1/non_itsm?host=localhost?tickets=3306")


def get_data():
    df = pd.read_sql('SELECT * FROM tickets', engine)
    return df

def getuser_Data():
    df = pd.read_sql('SELECT * FROM userdetails', engine)
    return df

def before_pred(df):
    df.to_sql(con=engine, name='tickets',if_exists = 'append',index=False)   
    return "updated"

def update(df):
    for i in range(0,len(df)):
        query = "update tickets set Solution='"+str(df['Solution'][i])+"', Status='"+str(df['Status'][i])+"' where `Incident ID` = '"+str(df['Incident ID'][i])+"';"
        print(query)
        with engine.begin() as conn:     # TRANSACTION
            conn.execute(query)
    return 'Updated'

def updatenew(tid):
    query = "update tickets set Status='Resolved' where `Incident ID` = '"+tid+"';"
    print(query)
    with engine.begin() as conn:     # TRANSACTION
        conn.execute(query)
    return 'Updated'

def adduser_details(Hostname, IP_Address, MAC_ID, Serial_Number, OS_Version, Laptop_Desktop, IN_SERVER, OUT_SERVER, Direct_Printers, User_Name):
    query = "INSERT INTO userdetails VALUES ('"+Hostname+"','"+IP_Address+"','"+MAC_ID+"','"+Serial_Number+"','"+OS_Version+"','"+Laptop_Desktop+"','"+IN_SERVER+"','"+OUT_SERVER+"','"+Direct_Printers+"','"+User_Name+"')"
    with engine.begin() as conn:     # TRANSACTION
            conn.execute(query)

def adduser_update(Hostname, IP_Address, MAC_ID, Serial_Number, OS_Version, Laptop_Desktop, IN_SERVER, OUT_SERVER, Direct_Printers, User_Name):
    query = "update userdetails set Hostname='"+Hostname+"', IP_Address='"+IP_Address+"' , Serial_Number='"+Serial_Number+"' , OS_Version='"+OS_Version+"' , Laptop_Desktop='"+Laptop_Desktop+"', Direct_Printers='"+Direct_Printers+"' , User_Name='"+User_Name+"' where MAC_ID = '"+MAC_ID+"';"
    print(query)
    with engine.begin() as conn:     # TRANSACTION
        conn.execute(query)
    return 'Updated'

def fetchquery(query):
    df = pd.read_sql(query,engine)
    return df

def createnewuser(query):
    with engine.begin() as conn:     # TRANSACTION
        conn.execute(query)
    return 'Created'