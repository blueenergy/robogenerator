#!/usr/bin/env python
#coding : utf-8

from jpype import *

jvmpath = getDefaultJVMPath()
print jvmpath
jvmpath = 'C:/Program Files/Java/jdk1.7.0_06/jre/bin/server\jvm.dll'
startJVM(jvmpath, "-ea", "-Djava.class.path=.")

#TA = JPackage('test').TestJava
TA = JPackage('test').CPP
#TA = JPackage('test').TestJava
print 'we got here'
#jd = TA(4)
#print dir(jd)
G = TA(4)
print dir(G)
print 'we got here ******'
G.addArc("aa", 0, 1, 1)
#G.addArc("aa", 0, 1, 1).addArc("bb", 0, 2, 1).addArc("cc", 1, 2, 1)
#G.addArc("dd", 1, 3, 1).addArc("ee", 2, 3, 1).addArc("ff", 3, 0, 1)
G.solve()
G.printCPT(0)
print "Cost = %s"%G.cost()
#jd.printData('1234')
#s1,s2,s3 = jd.getTimeList()
#print s1
#print dir(s1)
#print s1.hour,s1.min,s1.sec
#print s
shutdownJVM();
