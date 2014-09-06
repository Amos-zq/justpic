#!/usr/bin/env python
# encoding: utf-8
"""
y=1+0.5x
"""
import sys
#训练数据集
#自变量像x(x0,x1)
x=[(1,1.15),(1,1.9),(1,3.06),(1,4.66),(1,6.84),(1,7.95)]
#假设函数h(x)=theta0*x[0]+theta1*x[1]
#y为理想theta值下的真实函数值
y=[1.37,2.4,3.02,3.06,4.22,5.42]

#两种终止条件
loop_max=10000 #最大迭代次数
epision=0.0001 #收敛精度

alpha=0.005 #步长
diff = 0 #每一次实验时当前值与理想值的差距
error0=0 #上一次目标函数值之和
error1=0 #当前次目标函数值之和
m=len(x)  #训练数据条数
#init the parameters to zero
theta=[0,0]


count=0
finish=0
while count<loop_max:
    count+=1
    for i in range(m):
        diff=(theta[0]+theta[1]*x[i][1])-y[i]

        #求参数theta、增量梯度下降算法、每次只使用一组训练数据
        theta[0]=theta[0]-alpha*diff*x[i][0]
        theta[1]=theta[1]-alpha*diff*x[i][1]

    if abs(theta[0]-error0)<epision and abs(theta[1]-error1)<epision:
        print "theta:[%f,%f]" % (theta[0],theta[1])
        finish =1
    else:
        error0,erro1=theta
    if finish:
        break
print "FINISH count:%s"% count
