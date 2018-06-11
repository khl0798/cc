# -*-coding: utf-8-*-

from datetime import timedelta
from query_project import *
from flask_cors import CORS
import urllib
from flask import Flask, request, make_response, render_template, redirect, url_for,current_app
from functools import update_wrapper
import json, re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
app.debug=True
CORS(app)

#用户授权 获取用户code；根据用户code获取用户的access_token信息;
basic_url = "https://open.weixin.qq.com/connect/oauth2/"
token_url = "https://api.weixin.qq.com/sns/oauth2/"
APPID = "wxf57ad60fca7e5305"
APPSECRET = "e4eb280eba281b3bf39460b67c85ca8f"
REDIRECT_URL = "http://wechat.gloriagene.cn/identification"
api = {"code":basic_url + "authorize?appid={APPID}&redirect_uri={REDIRECT_URL}&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect",
       "token": token_url + "access_token?appid={APPID}&secret={SECRET}&code={CODE}&grant_type=authorization_code",}

def getCode(code):
    # url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (APPID, APPSECRET)
    url = api["token"].format(APPID=APPID,CODE=code,SECRET=APPSECRET)
    print("getcode_url",url)
    r = urllib.request.urlopen(url).read()
    print('getcode_r',r)
    openid = json.loads(r).get('openid')
    return openid


@app.route('/identification',methods=["GET","POST"])
def Identification():
    if request.method == 'POST':
        id = []
        data = request.form
        username = data.get('userName',"")
        useridcard = data.get("userIdCard","")
        usertel = data.get("userTel","")
        OPENID = data.get('openid',"")
        if not OPENID:
            openid = None
        else:
            openid = OPENID.replace('/#/','')
        query_wechat = Mysql(table_name="WECHAT_MYSQL")
        sql = """select * from identification where openid=\"%s\" and userName=\"%s\" order by datetime desc limit 1;""" % (openid,username)
        query_wechat_data = query_wechat.fetch_one(sql)
        if query_wechat_data:
            return_info = '{"success":true, "info": "Identification success!" }'
            return return_info
        else:
            db = Mysql(table_name="GLORIA_MYSQL")
            sql1 = """select * from sample_mx where SUBJECT_NAME=\"%s\";""" % username
            sql2 = """select * from sample_mx where SUBJECT_SFZ=\"%s\" or SUBJECT_NAME=\"%s\" or S_TEL=\"%s\";""" % (useridcard, username, usertel)
            data1 = db.fetch_all(sql1)
            data2 = db.fetch_all(sql2)
            if data1 and data2:
                db_identification = Mysql(table_name="WECHAT_MYSQL")
                username_decode = username.encode('raw_unicode_escape')
                username_encode = username_decode.decode('unicode_escape')

                #sql = """select * from identification where userName=\"%s\" and userIdCard=\"%s\" and userTel=\"%s\";""" % (username, useridcard, usertel)
                #out = db_identification.fetch_one(sql)
                #if not out:
                sql = """ insert into identification values(UUID(), \"%s\", \"%s\",\"%s\", now(),\"%s\"); """ % (username_encode, useridcard, usertel, openid)
                db_identification.execute(sql)
                db_identification.commit()
                return_info = {"success":True, "info": "Identification success!" }
            else:
                return_info = {"success":False, "info": "FALSE!" }

            return json.dumps(return_info, ensure_ascii=False)

    if request.method == 'GET':
         url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=http://wechat.gloriagene.cn/identification/&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect "%APPID
         params=request.args
         code=params.get("code","")
         openid = getCode(code)
         return_url = "http://wechat.gloriagene.cn/?openid=%s/"  % openid
         return redirect(return_url)

@app.route('/report', methods=['GET','POST'])
def Report():
    import json
    data = json.loads(json.dumps(request.form))
    print(data)
    data_copy=data["userName"]
    username = data_copy[0]
    print(username)
    useridcard = data["userIdCard"][0]
    usertel = data["userTel"][0]
    #print(data.get("size"))
    print("size", data['size'][0])
    print('page',data['page'][0])
    size = int(data["size"][0])
    page = int(data["page"][0])     
    response = make_response(json.dumps(data, ensure_ascii=False))
    #print(response)
    # 设置允许跨域请求
    #response.headers['Access-Control-Allow-Origin'] = '*'
    #response.headers['Content-Type'] = 'application/json'
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    #print(username,useridcard,usertel)
    queryinfo, ret = QUERY(username=username, useridcard=useridcard, usertel=usertel)
    print("11111111111111111111111111111111111")
    if ret:
        obj = []
        for keys, values in queryinfo.items():
            range_tmp = range(len(values))
            mod = len(values) % size  # 取余
            reminder = int(len(values) / size)
            if mod != 0:
                if page == 0:
                    range_id = range_tmp[0:size]
                elif page == (reminder - 1):
                    range_id = range_tmp[(size * page):(len(values) + 1)]
                else:
                    range_id = range_tmp[(size * page):(size * (page + 1))]
            else:
                range_id = range_tmp[(size * page):(size * (page + 1))]
            print("2222222222222222222222222222222222222222222")
            #print(range_id)
            for index in range_id:
                values_info = values[index]
                values1 = values_info["info"]
                step = {}
                step["stepData"] = []
                "type为True表示pipeline有5个步骤, type为False表示pipeline有4个步骤"
                if re.search('NGS', values_info["type"]):
                    step["type"] = True
                else:
                    step["type"] = False
                step["reportName"] = values_info["project"]
                step["reportId"] = values_info["reportId"]
                step_num = None
                if step["type"]:
                    if values1["report"]["ret"]:
                        step_num = 4
                        tmp_report = {"text": "报告解读", "time": values1["report"]["time"]}
                    else:
                        tmp_report = {"text": "报告解读", "time": values1["report"]["time"]}

                    tmp_analysis = {"text": "生信分析", "time": values1["analysis"]["time"]}
                    tmp_time_null = [values1["outmanager"]["time"], values1["datapcr"]["time"], values1["ngs"]["time"], values1["pcr"]["time"]]
                    tmp_time = []
                    for i in tmp_time_null:
                        if i:
                            tmp_time.append(i)
                    #print("测序实验", tmp_time)
                    try:
                        tmp_sequence = {"text": "测序实验", "time": min(tmp_time)}
                    except Exception as e:
                        tmp_sequence = {"text": "测序实验", "time": ""}
                    tmp_pcr = {"text": "样本质控", "time": values1["extractrqc"]["time"]}
                    tmp_library = {"text": "样本到达", "time": values1["library"]["time"]}
                    if values1["analysis"]["ret"]:
                        if not step_num:
                            step_num = 3
                    elif (values1["outmanager"]["ret"] or values1["datapcr"]["ret"] or values1["ngs"]["ret"] or values1["pcr"]["ret"]):
                        if not step_num:
                            step_num = 2
                    elif values1["extractrqc"]["ret"]:
                        if not step_num:
                            step_num = 1
                    elif not step_num:
                        step_num = 0
                    step["stepData"].extend([tmp_library,tmp_pcr,tmp_sequence, tmp_analysis,tmp_report])
                else:
                    if values1["report"]["ret"]:
                        if not step_num:
                            step_num = 3
                        tmp_report = {"text": "报告解读", "time": values1["report"]["time"]}
                    else:
                        tmp_report = {"text": "报告解读", "time": values1["report"]["time"]}
                    tmp_time_null = [values1["outmanager"]["time"], values1["datapcr"]["time"], values1["pcr"]["time"]]
                    tmp_time = []
                    for i in tmp_time_null:
                        if i:
                            tmp_time.append(i)
                    try:
                        tmp_sequence = {"text": "分子检测", "time": min(tmp_time)}
                    except Exception as e:
                        tmp_sequence = {"text": "分子检测", "time": ""}
                    tmp_pcr = {"text": "样本质控", "time": values1["extractrqc"]["time"]}
                    tmp_library = {"text": "样本到达", "time": values1["library"]["time"]} 
                    if values1["outmanager"]["ret"] or values1["datapcr"]["ret"] or values1["pcr"]["ret"]:
                        if not step_num:
                            step_num = 2
                    if values1["extractrqc"]["ret"]:
                        if not step_num:
                            step_num = 1
                    elif not step_num:
                        step_num = 0
                    step["stepData"].extend([tmp_library,tmp_pcr,tmp_sequence,tmp_report])
                step["step"] = step_num
                if step["type"]:
                    if step["step"] == 4:
                        step["end"] = True
                    else:
                        step["end"] = False
                else:
                    if step["step"] == 3:
                        step['end'] = True
                    else:
                        step["end"] = False
                obj.append(step)
        if obj:
            length = len(obj)
            # 暂时先把参数end改成这个样子,此处是有一个bug存在的
            return_info = {"success": True, "obj": obj, "length": str(length)}
        else:
            return_info = {"success": False, "obj": "wrong!"}
    else:
            return_info = {"success": False, "obj": "wrong!"}
    return json.dumps(return_info, ensure_ascii=False)

@app.route('/getreport', methods=['GET','POST'])
def GetReport():
        data = request.form
        project_id = data.get("reportId","")
        db = Mysql(table_name="GLORIA_MYSQL")
        response = make_response(json.dumps(data, ensure_ascii=False))
        #print(response)
        # 设置允许跨域请求
        #response.headers['Access-Control-Allow-Origin'] = '*'
        #response.headers['Content-Type'] = 'application/json'
        # select * from sample_qc qc，sample_mx mx where qc.old_sample_mx_id=mx.id and mx.S_MCODE='YHT1730028';
        sql = "select RP_FILE from report_info where ID=\"%s\";" % project_id
        db_out_tmp = db.fetch_all(sql)
        if db_out_tmp:
            for db_out in db_out_tmp:
                print("heiheiheiheihiehieh")
                #print(db_out)
                if db_out:
                    path = "E:/nginx/wechat_data"
                    new_path = "http://wechat.gloriagene.cn:8097"
                    from collections import defaultdict
                    import urllib
                    #print('db_out', db_out)
                    png_list = []
                    if db_out:
                        report_name = db_out[0]
                        if report_name and 'pdf' in report_name:
                            png_path = path + "/" + report_name.split(".pdf")[0]
                            if os.path.exists(png_path):
                                png_report_name_list = os.listdir(png_path)
                                if png_report_name_list:
                                    png_num = len(os.listdir(png_path))
                                    # png_tmp_list = glob.glob("%s/%s*.png" % (png_path, report_name.split(".pdf")[0]))
                                    for i in range(png_num):
                                        png_tmp = os.path.join(png_path, "%s-%s.png" % (report_name.split(".pdf")[0], str(i)))
                                        png_list.append({"url": png_tmp.replace(path, new_path)})
                                        #print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
                                        #print('png_list', png_list)
                                        return_info = {"success": True, "obj": png_list}
                                else:
                                    return_info = {"success": False, "obj": "报告正在生成中!"}
                            else:
                                return_info = {"success": False, "obj": "报告正在生成中!"}
                        else:
                            return_info = {"success": False, "obj": "报告正在生成中!"}
                    else:
                        return_info = {"success": False, "obj": "报告正在生成中!"}
        else:
            return_info = {"success": False, "obj": "报告正在生成中!"}
        return json.dumps(return_info, ensure_ascii=False)

# def createMenu()
# app.add_route("/identification", Identification())
# app.add_route("/report", Report())
# app.add_route("/getreport", GetReport())
"convert -verbose -density 300 YHB1721364-于萍-普瑞逸（Pre-HC）-遗传性肿瘤基因检测-20180126\(1\)_20180126054813421.pdf -quality 100 -depth 24 YHB1721364-于萍-普瑞逸（Pre-HC）-遗传性肿瘤基因检测-20180126\(1\)_20180126054813421.png"

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8093)
    #getCode()
    # httpd = simple_server.make_server("0.0.0.0", 8093, app)
    # httpd.serve_forever()

