# 商品推荐

数据库
Mysql数据库5.7
参数如下：
MySQLdb.connect(host='localhost', port=3306, user='root', passwd='123456', db='newsrecommend', charset='utf8')
表
User表
建表语句和数据

CREATE TABLE `user`  (
  `user_name` varchar(255) ,
  `password` varchar(255) ,
  `history` varchar(5000) ,
  PRIMARY KEY (`user_name`) USING BTREE
) ;

INSERT INTO `user` VALUES ('1', '1', '{}');
INSERT INTO `user` VALUES ('123', '123', '{}');
Python库
Python3.6   
anaconda3
MySQLdb         https://pypi.org/project/mysqlclient/
Tkinter         anaconda3自带
Jieba           https://pypi.org/project/jieba/
文件结构
login.py       主程序（三个界面：登录、注册、商品推荐）
zhua.py       商品爬虫
shangpin.txt   商品列表（手机类商品）
