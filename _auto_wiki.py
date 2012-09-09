# coding=gbk
import urllib2
import cookielib
from urllib import urlencode

import gzip,StringIO,re,time,random

class MakeText():
    def __init__(self):
        self.__text=''

        # Start time is a week earlier than end time.
        self.__end_time=time.time()
        self.__start_time=self.__end_time-6*24*60*60

        self.__tab=' '*4

    def __make_Time(self):
        start=time.strftime('%Y-%m-%d',time.localtime(self.__start_time))
        end=time.strftime('%Y-%m-%d',time.localtime(self.__end_time))
        return start+'~'+end

    def __make_Work(self,num=3):
        works=["写数据挖掘作业"
               ,"调研VMFS"
               ,"实现协同过滤算法"
               ,"看vsched代码"
               ,"考虑工程实践项目细节"
               ,"读论文"
               ,"学习Clojure"]
        
        if len(works)<num:
            num=len(works)
        work_set=set()
        start=0
        end=len(works)-1
        while len(work_set)!=num:
            work_set.add(random.randint(start,end))
            
        work_list=[]
        for i in work_set:
            work_list.append(works[i])
            
        return work_list

    def __make_Text(self):
        str_time=self.__make_Time()
        work_list=self.__make_Work()
        text=self.__tab+'* '+str_time+':\n'
        for work in work_list:
            text+=self.__tab*2+'* '+work+'\n'
        self.__text=text
        return self.__text 

    def make_Text(self):
        return self.__make_Text()

class AutoWiki:
    def __init__(self):
        self.opener=None
        
        self.__uri='http://dev.ivic.org.cn/ivic/'
        self.__login_url='http://dev.ivic.org.cn/ivic/login'
        self.__submit_url='http://dev.ivic.org.cn/ivic/wiki/AnQi/NewTerm1'
        self.__edit_url=self.__submit_url+'?action=edit'
        self.__referer=self.__edit_url
        
        self.__auth={'user':'anqi','passwd':'407714'}
        
        self.__text=None
        self.__form_token=''
        self.__version=''

    # Deal with username and password. PasswordManager?
    def __get_HTTPBasicAuthHandler(self):
        auth_handler=urllib2.HTTPBasicAuthHandler()
        auth_handler.add_password(realm=None,
                                  uri=self.__uri,
                                  user=self.__auth['user'],
                                  passwd=self.__auth['passwd'])
        return auth_handler

    # Deal with cookie
    def __get_CookieHandler(self):
        cookie=cookielib.LWPCookieJar()
        return urllib2.HTTPCookieProcessor(cookie)

    # Build and install urlopener
    def __get_Opener(self):
        auth_handler=self.__get_HTTPBasicAuthHandler()
        cookie_handler=self.__get_CookieHandler()
        opener=urllib2.build_opener(auth_handler,cookie_handler)
        return opener
    
    ###########################
    # Deal with header and data
    def __get_Header(self):
        header={
                'Host':'dev.ivic.org.cn',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
                'Connection':'keep-alive',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                'Referer':self.__referer,
                'Content-Type':'application/x-www-form-urlencoded',
                'Authorization':'Basic YW5xaTo0MDc3MTQ='    # My login
                }
        return header

    def __get_DataPara(self,url):
        if url.headers.has_key('Content-Encoding'):
            raw_data=self.__deal_Gzip(url)
        else:
            raw_data=url.read()

        # __FORM_TOKEN
        m=re.search('name="__FORM_TOKEN" value="(\w*)"',raw_data)
        if m is not None:
            self.__form_token=m.group(1)
        else:
            return False
        # version
        m=re.search('name="version" value="(\d*)"',raw_data)
        if m is not None:
            self.__version=str(int(m.group(1)))
        else:
            return False
            
        return True

    def __get_Data(self,text='What\'s the weather today?'):
        if self.__form_token=='' or self.__version=='':
            return False
        values={'__FORM_TOKEN':self.__form_token
                ,'action':'edit'
                ,'version':self.__version
                ,'scroll_bar_pos':'0'
                ,'editrows':'20'
                ,'text':text
                ,'comment':''
                ,'save':'Submit changes'}
        data=urlencode(values)
        return data

    # To make urllib2.Request
    def __get_Request(self,url='',GET=False):
        # url=url
        if GET:
            data=None
        else:
            data=self.__get_Data(self.__get_Edit())
        headers=self.__get_Header()
        #origin_req_host=?
        request=urllib2.Request(url,data,headers)
        return request

    def __deal_Gzip(self,url):
        fobj=StringIO.StringIO()
        fobj.write(url.read())
        fobj.seek(0)
        gzip_file=gzip.GzipFile(fileobj=fobj)
        context=gzip_file.read()
        return context

    # login
    def __login(self):
        if self.opener==None:
            return False
        else:
            req=self.__get_Request(self.__login_url,True)
            r=urllib2.urlopen(req)
            if not self.__get_DataPara(r):
                return False
            return True

    def __get_Response(self,url,GET=False):
        req=self.__get_Request(url,GET)
        r=urllib2.urlopen(req)
        if r.headers.has_key('Content-Encoding'):
            res=self.__deal_Gzip(r)
        else:
            res=r.read()
        return res

    def __get_Edit(self):
        # Code...
        add_on=MakeText().make_Text().decode('gb2312').encode('utf-8')
        self.__text=add_on+self.__get_Text()
        return self.__text

    def __get_Text(self):
        res=self.__get_Response(self.__edit_url,True)
        self.__text=res.split("<textarea")[-1].split("</textarea>")[0].split(">")[1][1:]
        #m=re.search("<textarea.*>(\s|.)*",res)
        #if m is not None:
        #    self.__text=m.group()
        return self.__text

    # Play~
    def submit(self):
        self.opener=self.__get_Opener()
        urllib2.install_opener(self.opener)
        # login
        if not self.__login():
            print 'Error'
            return
        
        res=self.__get_Response(self.__submit_url)
        print res

if __name__=='__main__':
    AutoWiki().submit()
    #print [MakeText().make_Text()]
    
