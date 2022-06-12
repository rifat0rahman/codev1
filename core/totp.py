import pyotp
from time import sleep

while (True): 

    totp = pyotp.TOTP("JBSWY3DPEHPK3PXP")
    print("Current OTP:", totp.now())
    sleep(2)

