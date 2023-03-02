
import json
import bcrypt 
from conn import query, insert, removeOutliers



def control_loop():
    otp = ''
    while otp != 'quit':
        otp = input("otp: ")
        print(otp)
        newData = json.loads(otp)
        email = newData['email']
        pwd = newData['oTP']
        print(email)
        print(pwd)
        response = query(email)         #calls funciton in conn.py to get info from db document
        if response != "query is null":
            res = verify(response.pwd, pwd)
            if res == True:
                insert(response)
            else:
                print("QR too old")     #handled cases for invalid QR codes
                removeOutliers()
        else:
            print("err")

    else:
        print("There was some error")

def decodeQR():
    filename = "qr.png"

    image = cv2.imread(filename)

    # initialize the cv2 QRCode detector
    detector = cv2.QRCodeDetector()

    # detect and decode
    data, vertices_array, binary_qrcode = detector.detectAndDecode(image)

    # if there is a QR code
    # print the data
    if vertices_array is not None:      #gets JSON data from the QR code presented
        print("QRCode data:")
        newData = json.loads(data)
        email = newData['email']
        pwd = newData['oTP']
        print(email)
        print(pwd)
        response = query(email)         #calls funciton in conn.py to get info from db document
        if response != "query is null":
            res = verify(response.pwd, pwd)
            if res == True:
                insert(response)
            else:
                print("QR too old")     #handled cases for invalid QR codes
                removeOutliers()
        else:
            print("err")

    else:
        print("There was some error")

def verify(hashedpw, pwd):          #verifys bcrypt string held in database 
    print(hashedpw)
    print(pwd)
    bytes = pwd.encode('utf-8')
    hash = hashedpw.encode('utf-8')
    result = bcrypt.checkpw(bytes, hash)
    if result == True: 
        print(result)
        unlockDoor()
    else:
        print("Auth failed")
    return result

def unlockDoor():
    print("door unlocked")
    #Add logic to open door when part is provided 

if __name__ == "__main__":
    control_loop()