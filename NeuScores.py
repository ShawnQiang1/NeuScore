# -*- encoding: utf-8 -*-
#@作者：枭强
#@日期：2021—1—25 22：40
#@备注：东北大学成绩更新自动通知脚本
import urllib.request
from lxml import etree
import http.cookiejar
import requests
import time
user="2019xxxx"#你的学号
passwd="abaaba" #你的智慧东大密码
key="xxxxxxxxxxxxxxxxxxx" #此处填写server酱的key
timeout=10#间隔多少秒上检查一遍（默认10s可以不用改）

###################以下为代码内容###################################

#定义UA标识
header = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
        }
#登录智慧东大的url
url_login = "https://pass.neu.edu.cn/tpass/login?service=http%3A%2F%2F219.216.96.4%2Feams%2FhomeExt.action"
print("脚本已运行！！")
while True:
    try:
    #创建储存cookie对象
        cookie = http.cookiejar.CookieJar()
        headler = urllib.request.HTTPCookieProcessor(cookie)
        opener =urllib.request.build_opener(headler)
        #获取登录智慧东大时所需流水号，创建正确的提交表单
        first_get=opener.open(url_login)
        first_get_text=first_get.read().decode("utf-8")
        tree = etree.HTML(first_get_text)
        #获取流水号
        lt_value=tree.xpath('//*[@id="lt"]/@value')[0]
        data={
                "rsa": user+passwd+lt_value,
                "ul": str(len(user)),
                "pl": str(len(passwd)),
                "lt": lt_value,
                "execution": 'e1s1',
                "_eventId": 'submit'
        }
        #将所需提交的表单（data）类型转换为bytes类型！！！
        postdata = urllib.parse.urlencode(data).encode("utf-8")
        #构造访问请求,此时保存cookie至opener
        request =urllib.request.Request(url_login,headers=header,data=postdata)
        upme=opener.open(request)

        #全都成绩的链接
        query="http://219.216.96.4/eams/teach/grade/course/person!historyCourseGrade.action?projectType=MAJOR"
        note_request= urllib.request.Request(query)
        up_note=opener.open(note_request).read().decode()
        tree1=etree.HTML(up_note)
        grade=tree1.xpath("//*[@id='grid21344342991_data']//tr")
        list=[]
        #对最开始的成绩进行第一次遍历
        for tr in grade:
            course_first = tr.xpath("./td[4]/text()")[0].split()[0]
            list.append(course_first)
        for i in range(0,60):#进行60次请求后重新登录智慧东大
            #重新发送请求遍历成绩
            up_note2 = opener.open(note_request).read().decode()
            tree2 = etree.HTML(up_note2)
            grade2 = tree2.xpath("//*[@id='grid21344342991_data']//tr")
            for items in grade2:
                course_later=items.xpath("./td[4]/text()")[0].split()[0]
                #检查是否有新科目成绩
                if course_later not in list:
                    score=items.xpath("./td[14]/text()")[0].split()[0]
                    key = "http://sc.ftqq.com/"+key+".send?"+"text="+course_later+"&desp="+str(score)
                    send=requests.get(key)#利用server酱进行微信通知
                    print("科目:",course_later,"分数：",score," 已发送!")
                    #发送后添加进列表，防止反复通知
                    list.append(course_later)
            time.sleep(timeout)
    except:#抛出异常
        print("出错了！重新发送请求！")