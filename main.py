
import json
import bcrypt 
import RPi.GPIO as GPIO
import time
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
    GPIO.setmode(GPIO.BCM)
    datapin = 4
    GPIO.setup(datapin, GPIO.OUT)
    GPIO.output(datapin, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(datapin, GPIO.LOW)
    print("door unlocked")
    #Add logic to open door when part is provided 

if __name__ == "__main__":
    control_loop()