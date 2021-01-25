# 东北大学教务系统成绩更新爬虫   
使用本脚本，成绩一旦更新将通过server酱公众号向你微信发送成绩信息  
# 使用方法：  
  1.安装对应模块  
   pip install requests
   pip install http
   pip install lxml
  1.进入[server酱官网](http://sc.ftqq.com/) 自行登录  
   进入 微信推送 绑定微信号  
   然后进入 发送消息 复制自己的SCKEY    
  2.修改脚本参数
   user="2019xxxx"#你的学号
   passwd="abaaba" #你的智慧东大密码
   key="xxxxxxxxxxxxxxxxxxx" #此处填写server酱的sckey
   按照自己信息修改后保存
  3.运行
   在脚本目录下打开cmd输入python NeuScores.py然后回车
