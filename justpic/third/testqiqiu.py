import os,sys
libpath=os.path.join(os.path.dirname(os.path.abspath(__file__)),'qiqiu')
sys.path.append(libpath)
import qiniu.conf

qiniu.conf.ACCESS_KEY="LJSr_luxoWc_USn_iDX41bSJZ1cAmoe36Drfcpv0"
qiniu.conf.SECRET_KEY="JA-WnQmkI_rpEXlyvBdyaliZ-RD8OUbq86QdYJ4u"

#import qiniu.rs
#ret,err=qiniu.rs.Client().stat('justpic',key)
#if err is not None:
#    print err
#    error(err)

