from markpic.models import Student

class MyCustomBackend:
    def authenticate(self,studentid=None,password=None):
        try:
            user=Student.objects.get(studentid=studentid)
        except Student.DoesNotExist:
            pass
        else:
            if user.check_password(password):
                return user
        return None
    def get_user(self,studentid):
        try:
            return Student.objects.get(studentid=studentid)
        except Student.DoseNotExist:
            return None
        
