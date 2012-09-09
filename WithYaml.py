# coding=gbk
import os
import yaml

YFile='work_list.yaml'

def getYaml(yfile=YFile):
    if os.path.exists(yfile):
        f=open(yfile,'r')
    else:
        print 'No such file called %s' %yfile
        return None
    return yaml.load(f)
        

def setYaml(dictionary,yfile=YFile):
    f=open(yfile,'w')
    yaml.dump(dictionary,f)
    f.close()

if __name__=='__main__':
    works=["����iscsi����"
           ,"���Բ���iscsi��"
           ,"����VMFS"
           ,"ά�����Լ�Ⱥ"
           ,"����ivic��װ��"
           ,"�޸�VMC�ĵ�"
           ,"������"
           ,"ѧϰClojure"]
    setYaml(works)
