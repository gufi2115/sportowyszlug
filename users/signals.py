from django.core.mail import send_mail
from django.contrib.auth.models import User
from random import randint
import string

from sportowyszlug.settings import EMAIL_HOST_USER


def verificationCode():
    code = [""]
    code_lenght = 0
    alphabet = list(string.ascii_letters)
    numbers = [n for n in range(10)]

    while code_lenght < 6:
        l_or_n = randint(1,2)
        r_l = randint(0, 51)
        r_n = randint(0, 9)
        if l_or_n == 1:
            code[0] += alphabet[r_l]
        else:
            code[0] += str(numbers[r_n])
        code_lenght += 1

    return code

verification_code = verificationCode()

def verifyEmail(user_email):

    subject = "Verify profile"

    message = f"""
                This is your verification code
                    {verification_code[0]} 
                paste it on page
    """

    sender = EMAIL_HOST_USER

    receiver = [user_email]

    return subject, message, sender, receiver