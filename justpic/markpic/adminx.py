from markpic.models import Student,Picture5K,Log5k,UserProfile,PrivatePicture
import xadmin
xadmin.site.register(UserProfile)
xadmin.site.register(PrivatePicture)
# xadmin.site.register(Student)
xadmin.site.register(Log5k)
xadmin.site.register(Picture5K)

