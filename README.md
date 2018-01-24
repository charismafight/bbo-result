This is a tool for export [bbo results](http://www.bridgebase.com/myhands/index.php?&from_login=0)(lin files)

[lin file structure](http://www.bridgebase.com/help/v2help/handviewer.html)



Dependencies
- [pywin32](https://sourceforge.net/projects/pywin32/files/pywin32/]): choose the corresponding version
- requests: pip or pip3 install requests



## Quick Start
* 保证template文件夹下有相应模板，命名规则为form_[桌数]_[牌副数].docx
* 检查bbo_id文件中的bbo帐号确保正确，换行分隔
* 确认上一节中的依赖库已经正确安装
* 运行word_generator.py并根据提示提供参数信息
* 运行效率问题，因为bbo的gethannds页面做了访问限制，多次访问的请求间隔小于5秒会拒绝，所以每副牌的获取时间固定为5秒


```
# 桌数
Please input table count:2
# 牌副数
Please input boards count:20
# 开始日期
Please input when the game start(eg:20180101):20180121
# 结束日期，如果确定是开始日期当天可以直接回车
Please input when the game end(eg:20180101,default:start_time 23:59:59):
# 比赛名称关键字，用于查找比赛，注意大小写
Please input the keyword of the game(default:Orange):Untitled
```

* 如果没有异常会输出Finished!Press Enter to close window.
* 产生的结果文件在程序根目录下的results文件夹中以Result年月日时分.docx的形式命名
* 获取的数据在files文件夹中以年月日时分的形式创建目录以做备份