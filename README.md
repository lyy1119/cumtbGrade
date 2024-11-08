# cumtbGrade

## 说明

这个仓库仅是个留存，不保证有维护。  

## 功能

1. 展示考试成绩、绩点、成绩明细（平时、期末分什么的）
2. 发送邮件提醒出成绩了

## 使用

你需要修改如下内容：  
1. `config/cfg.json`中的`account`中的id和pwd，id即学号，pwd即密码。
2. `config/email.json`中的email配置。具体内容自行搜索学习。
3. 查看`main.py`你会发现有几处报错，那是用来接收邮件的邮箱名，你需要填写你自己的邮箱地址。
4. 暂时就上述内容，如有遗漏，日后再加

## 其他事项

本程序依赖x-id-token，所以请部署 [这个程序(用于获取token)](https://github.com/lyy1119/cumtb_token_api)  

建议使用make将本程序构建成docker，由于构建成docker后不好修改账户密码，故不给出二进制release文件。
