
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
import calendar
import pytz

cred = credentials.Certificate("gymuserauth-firebase-adminsdk-gr8ty-f36ad23bf9.json")       #Firebase auth setup
firebase_admin.initialize_app(cred)


db = firestore.client()


class db_result:
    def __init__(self, email, pwd, id):     #class to hold query result data 
        self.email = email
        self.pwd = pwd
        self.id = id

def insert(response):       #function to add and delete records from documents
    data = {
        u'email': response.email,
        u'Time_entered': datetime.datetime.now(),
        u'id': response.id
    }
    db.collection(u'AuthLog').document(response.id).set(data)
    db.collection(u'generatedPasswords').document(response.id).delete()
    removeOutliers()

def removeOutliers():
    expired = datetime.datetime.now() - datetime.timedelta(minutes=1)
    oldAuths = db.collection(u'generatedPasswords').where('dateCreated', '<=', expired).stream()
    for doc in oldAuths:
        docData = doc.to_dict()
        db.collection(u'generatedPasswords').document(docData['otpID']).delete()


def checkAdmin(email):
    documents = [d for d in db.collection(u'users').where (u'email', u'==', email).stream()]
    if len(documents):
        for document in documents:
            docData = document.to_dict()
            admin = docData['admin']
    if admin == True:
        print('call query function')
    elif admin == False:
        print ('check opening times and all that')
    else:
        print('not a valid user')
    return admin

def CheckKillSwitch():
    killsSwtichState = db.collection(u'Admin').document(u'killswitch').get()
    useable = killsSwtichState.to_dict()
    if  useable['engage'] == False:
        return True
    elif    useable['engage'] == True:
        return False

def isbetweentime(begin_time, end_time, checktime = None):
    check_time = checktime or datetime.datetime.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def checkopeningHours():
    day = calendar.day_name[datetime.datetime.today().weekday()]
    openingHours = db.collection(u'Admin').document(u'openingHours').get()
    useable = openingHours.to_dict()
    todaysHours = useable[day]
    if todaysHours['open'] != 'closed':
        opening = todaysHours['open'].split(":")
        openHour = int(opening[0])
        openMin = int(opening[1])
        closeing = todaysHours['close'].split(":")
        closeHour = int(closeing[0])
        closeMin = int(closeing[1])
        res = isbetweentime(datetime.time(openHour, openMin), datetime.time(closeHour, closeMin))
    else:
        res = False
    return res

def Checkopen(email):
    adminres = checkAdmin(email)
    if adminres == True:
        return True
    else:
        openingres = checkopeningHours()
        killswitchres = CheckKillSwitch()
        if openingres == True and killswitchres == True:
            return True
        else:
            return False


def query(email):           #function to get users OTP from db document 
    openstatus = Checkopen(email)
    if openstatus == True:
    #openstatus = Checkopen(email)
    #print(openstatus)
        timeframe = datetime.datetime.now() - datetime.timedelta(minutes=1)
        documents = [d for d in db.collection(u'generatedPasswords').where (u'email', u'==', email).stream()]
        print(len(documents))
        if len(documents):
            for document in documents:
                docData = document.to_dict()
                timestamp = docData['dateCreated']
                timestamp = timestamp.replace(tzinfo=None)
                currentTime = datetime.datetime.now()
                elapsed = currentTime-timestamp         #method for getting the elapsed time between two datetime objects 
                if elapsed.total_seconds()/60 <= 5:     #change the /5 to agreed amount of time once testing is done
                    print("valid qr")
                else:
                    print("out of time range")
                currentAuthReq = db_result(docData['email'], docData['otp'], docData['otpID'])      #storing results in dbobject class 
                print(currentAuthReq.id)
                return currentAuthReq
        else:
            print("null")
            return "query is null"
    else:
        return "query is null"


if __name__ == "__main__":
    #checkAdmin('ios@test.com')
    checkopeningHours()