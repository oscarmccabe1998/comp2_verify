import cv2
import json
import bcrypt 

filename = "Screenshot 2023-02-08 at 13.21.00.png"

image = cv2.imread(filename)

# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()

# detect and decode
data, vertices_array, binary_qrcode = detector.detectAndDecode(image)

# if there is a QR code
# print the data
if vertices_array is not None:
    print("QRCode data:")
    newData = json.loads(data)
    email = newData['email']
    pwd = newData['oTP']
    print(email)
    print(pwd)

else:
    print("There was some error")

password = 'a5c1ae8b-8ada-4e25-83fd-fa25779d784c'
bytes = password.encode('utf-8')
hash_string = '$2b$06$C6UzMDM.H6dfI/f/IKxGhu7Etvtt0hrbXYj73G4SUpw1wKGoiuTWW'
hash = hash_string.encode('utf-8')
result = bcrypt.checkpw(bytes, hash)
print(result)