import random
import time
import hashlib
from django.core.mail import send_mail

 

def send_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        'mfrelyon@gmail.com',
        recipient_list,
        fail_silently=False,
    )
    try:
        send_mail(
            subject=subject,
            message=message, 
            from_email="service@richbook.net",
            recipient_list=recipient_list, 
            fail_silently=False,
        )
        return True
    except Exception as e:
        # Optionnel : logger l'erreur
        print(f"Erreur envoi email : {e}")
       
        raise
        # return False


def generate_code(string):
    return "".join( random.sample(string,len(string)) )+str(int(time.time()));
    
def compute_duration(start, end):
    start = start.split(":")
    start = (int(start[0])* 3600 ) + (int(start[1]) * 60 ) + int(start[2])
    end = end.split(":")
    end = (int(end[0]) * 3600 ) + (int(end[1]) * 60 ) + int(end[2])
    
    return int( end - start );

def compute_sha1(string):
    return hashlib.sha256(bytes(string,"utf-8")).hexdigest()
  