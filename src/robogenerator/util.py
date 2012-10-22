import os

def scan_and_remove(path,postfix):
#    print "hello"
    lenth=len(postfix)
    for root ,dirs,files in os.walk(path):  

        for filepath in files:
            if filepath[-lenth:]==postfix:
                print filepath
                os.remove(os.path.join(root,filepath)) 
                print '%s'%filepath+"  has  been deleted"
                pass
                
if __name__=='__main__':
    scan_and_remove('.','pyc')