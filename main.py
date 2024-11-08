import os
import json
from send_email import send_email
import time
from grade import Grade

def loading_config():
    with open("./config/cfg.json" , "r") as f:
        config = json.load(f)
        # print(config)
        return config

def write_config(cfg):
    with open("./config/cfg.json" , "+w" , encoding="UTF-8") as f:
        f.write(json.dumps(cfg , ensure_ascii = False))

def write_error_file(errorName):
    fileName = f"./error/{errorName}"
    with open(fileName , '+w') as f:
        f.write(errorName)
        pass

def write_personal_info(id):
    with open("./info.json" , "+w") as f:
        info = {"id" : id , "update_time" : time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}
        json_info = json.dumps(info)
        f.write(json_info)
    pass

def main():
    # 初始化程序
    config = loading_config()
    id      = config["account"]["id"]
    pwd     = config["account"]["pwd"]
    api     = config["api"]
    if config["header"].get("X-Id-Token" , None) == None:
        token = Grade.get_token(api , id , pwd)
        config["header"]["X-Id-Token"] = token
        # print(config)
        write_config(config)
        pass
    header  = config["header"]
    url="https://jwxt.cumtb.edu.cn/eams-micro-server/api/v1/grade/student/grades"

    while(True):
        # 获取最新成绩数据
        gradeEntry = Grade(header=header , url=url , id=id , pwd=pwd , api=api)
        if not gradeEntry.fetch():
            # print("tokenFail!")
            config["header"]["X-Id-Token"] = Grade.get_token(api , id , pwd)
            # print(config["header"]["X-Id-Token"])
            write_config(config)
            gradeEntry = Grade(header=header , url=url , id=id , pwd=pwd , api=api)
            if not gradeEntry.fetch():
                if not os.path.exists("./error/FetchError"):
                    send_email(to_email= , subject='成绩信息python程序出现bug' , body='BUG！\ntoken无法获取数据，且再次获得的token也无效！\n')
                    write_error_file("FetchError")
                # print("fetch error")
                return None

        gradeEntry.get_useful_info()
        # 比较获取数据和保存的数据
        diff = gradeEntry.grade_diff()
        if diff: # 如果有新出的成绩
            # 准备邮件表体和正文
            if len(diff) > 1:
                emailTitle = f"{len(diff)}门考试出成绩了"
            else:
                emailTitle = f"""{diff[0]["courseNameZh"]} 出成绩了"""
            emailBody = ''
            for i in diff:
                emailBody = emailBody + f"""科目：{i["courseNameZh"]}\t绩点：{i["gp"]}\t成绩：{i["finalGrade"]}\t成绩明细：{i["gradeDetail"]}\n"""
                pass
            send_email(to_email= , subject=emailTitle , body=emailBody)
            # 发送完邮件后，将新的写入json
            gradeEntry.save_to_file("grade.json")
        # 更新 个人信息、更新时间
        write_personal_info(id)
        time.sleep(600)

if __name__ == "__main__":
    main()
