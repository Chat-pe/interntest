from asyncore import loop
from api.database import otp
import random
import requests
import os
import logging

def send_otp_with_fast2sms(phone_number,otp_code,signature):
    params = {
        "authorization": os.environ["FAST2SMS_API_KEY"],
        "sender_id": os.environ["FAST2SMS_SENDER_ID"],
        "message": f"Your%20OTP%20is%20C-{otp_code}%20for%20registering%20with%20ChatPe.%0A{signature}",
        "numbers": phone_number[3:],
        "langugae": "english",
        "flash": "0",
        "route": "v3"
    }
    response = requests.get("https://www.fast2sms.com/dev/bulkV2", params=params)
    if response.status_code == 200:
        logging.log(logging.DEBUG, "OTP sent successfully")
        print(response.json())
        return True
    return False



def send_otp(phone_number, signature):
    otp_code = random.randint(1000, 9999)

    ## Developer only
    otp.insert_one({"phone_number": phone_number, "otp_code": 1567})
    return True

    ##Production version
    if send_otp_with_fast2sms(phone_number,otp_code, signature):
        otp.insert_one({"phone_number": phone_number, "otp_code": otp_code})
        return True
    return False


def verify_otp(phone_number, otp_code):
    otp_code_db = otp.find({"phone_number": phone_number}).sort("_id", -1).limit(1)
    otp_code_db = [op for op in otp_code_db][0]
    print(otp_code_db)
    if otp_code_db:
        if otp_code_db.get("otp_code") == int(otp_code):
            print("good")
            res = otp.delete_one({"phone_number": phone_number})
            return True
        else:
            return False
    else:
        return False

