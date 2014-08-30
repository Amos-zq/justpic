Justpic
-------
Justpic介绍

Justpic是一个简宜的图像检索系统，目前还在开发中



[在线demo](http://lab.justpic.org)

部署教程

环境搭建
-------
1.安装 python开发环境 (*nix已自带)

  安装好后建立沙盒
    $virtualenv picenv
    $source picenv/bin/activate

2.下载源码

    $cd ../ & git clone https://github.com/matrixorz/justpic
   或者直接下载：[justpic](https://github.com/matrixorz/justpic/archive/master.zip)

3.进入到项目目录，初始化数据：

    $cd justpic/1
    $pip install -r requirements.txt

4.初始化数据:

    $python manage.py validate
    $python manage.py syncdb
    $python manage.py initdb

5.运行：

    $python manager.py

5.访问http://localhost:8080 测试



nginx+uwsgi部署

安装uwsgi

    wget http://projects.unbit.it/downloads/uwsgi-2.0.4.tar.gz
    sudo apt-get install libxml2-dev
    tar -zxvf uwsgi-2.0.4.tar.gz
    make -f Makefile.Py27
    cp uwsgi /usr/sbin/uwsgi

    server {
       listen 80;
       server_name xxx.xxx;
       access_log /var/log/nginx/xxx_access.log;
       error_log /var/log/nginx/xxx_error.log;

       location / {
          uwsgi_pass 127.0.0.1:8630;
          include uwsgi_params;
       }
    }

Nginx配置完毕


uwsgi -x  path_to_project/django.xml

代码说明参见代码文件
