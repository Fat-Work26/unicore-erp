from django.contrib.auth.backends import ModelBackend 
from .models import User

class EmailOrNumInscriptionBackend(ModelBackend):
    def authenticate(self,request,username=None,password=None):
        try: 

           if '@' in username:
             user=User.objects.get(email=username)
           else:
             user= User.objects.get(num_inscription=username)
           if user.check_password(password):
            return user
        except User.DoesNotExist:
            return None
       