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
    works=["测试iscsi性能"
           ,"尝试部署iscsi卡"
           ,"调研VMFS"
           ,"维护测试集群"
           ,"测试ivic安装盘"
           ,"修改VMC文档"
           ,"读论文"
           ,"学习Clojure"]
    setYaml(works)
