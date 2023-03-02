
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
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



def query(email):           #function to get users OTP from db document 
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


if __name__ == "__main__":
    query('ios@test.com')