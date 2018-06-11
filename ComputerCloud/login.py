# -*-coding: utf-8-*-

from query_sample_info import *
sys.getdefaultencoding()

from addinfo import templateword
from falcon_multipart.middleware import MultipartMiddleware
from server import *
from flask import Flask, request, render_template as rt

app_flask = Flask(__name__)
CORS(app_flask, supports_credentials=True)

@app_flask.route('/taskOverview', methods=['POST'])
def taskOverview():
        result = {}
        filter = request.form.get("filter")
        progress = request.form.get("progress")
        size = int(request.form.get("size"))
        page = int(request.form.get("page"))
        username = request.form.get("userName")
        db = Mysql(table_name="MYSQL")
        sql = "select * from login where userName=\"%s\"" % username
        data = db.fetch_one(sql)
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        if data:
            usernameid = data[2]
            print('usernameid',usernameid)
            mysql = Mysql(table_name="REPORT_MYSQL")
            sql = "select * from taskOverview where usernameId=\"%s\";" % usernameid
            data = mysql.fetch_all(sql)
            info = []
            if data:
                for d in data:
                    if filter and not progress:
                        if filter in d[3]:
                            tmp_status = {"key":d[8],"value":d[9],"progress":d[10]}
                            tmp_data = {"taskDes": d[2],"reportName": d[3],"author": d[4],"date": d[5],"status": tmp_status}
                            if d[8] == "doing":
                                tmp_data["result"] = True
                            else:
                                tmp_data["result"] = False
                            info.append(tmp_data)
                    if not filter and progress:
                        if progress == d[8]:
                            print('<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>')
                            tmp_status = {"key": d[8], "value": d[9], "progress": d[10]}
                            tmp_data = {"taskDes":d[2],"reportName":d[3],"status":tmp_status,"author":d[4],"date":d[5]}
                            info.append(tmp_data)
                            if d[8] == "doing":
                                tmp_data["result"] = True
                            else:
                                tmp_data["result"] = False
                    if filter and progress:
                        if filter in d[3] and progress == d[8]:
                            tmp_status = {"key": d[8], "value": d[9], "progress": d[10]}
                            tmp_data = {"taskDes":d[2],"reportName":d[3],"status":tmp_status,"author":d[4],"date":d[5]}
                            info.append(tmp_data)
                            if d[8] == "doing":
                                tmp_data["result"] = True
                            else:
                                tmp_data["result"] = False
                    if not filter and not progress:
                        tmp_status = {"key": d[8], "value": d[9], "progress": d[10]}
                        tmp_data = {"taskDes": d[2], "reportName": d[3], "status": tmp_status, "author": d[4], "date": d[5]}
                        if d[8] == "doing":
                            tmp_data["result"] = True
                        else:
                            tmp_data["result"] = False
                        info.append(tmp_data)
                range_tmp = range(len(info))
                mod = len(info) % size  # 取余
                reminder = int(len(info) / size)
                if mod != 0:
                    if page == 1:
                        range_id = range_tmp[0:size]
                    elif page == (reminder - 1):
                        range_id = range_tmp[(size * (page - 1)):len(info)]
                    else:
                        range_id = range_tmp[(size * page):mod]
                else:
                    range_id = range_tmp[0:len(info)]
                print('range_id', range_id)
                out_json = []
                # print(info)
                for index in range_id:
                    out_json.append(info[index])
                result["success"] = True
                result["info"] = out_json
            else:
                result["success"] = False
        else:
            result["success"] = False
        return json.dumps(result, ensure_ascii=False)

@app_flask.route('/login', methods=['POST'])
def Login():
        data = request.form
        result={}
        # print(data)
        #data = eval(list(data1.keys())[0])
        #print(data)
        """  firstName: '', lastName: '', passWord: '', email: '', liteLab: '', passWord2: '', email2: '', institutionName: """
        username = data.get("userName")
        password = data.get("passWord")
        db = Mysql(table_name="MYSQL")
        sql = """select * from register where email = \"%s\";""" % username
        data2 = db.fetch_one(sql)
        # print(data2)
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        if data2:
            password_sql = data2[3]
            if password == password_sql:
                result["success"]=True
                result["info"] = "Log in success!"
            else:
                result["success"]=False
                result["info"]="Wrong passWord!"
        else:
            result["success"]=False
            result["info"]="Wrong userName!"
        db.commit()
        return json.dumps(result, ensure_ascii=False)

@app_flask.route('/register', methods=['POST'])
def Register():
        data = request.form
        result={}
        #data = eval(list(data1.keys())[0])
        """  firstName: '', lastName: '', passWord: '', email: '', liteLab: '', passWord2: '', email2: '', institutionName: """
        firstName = data.get("firstName")
        lastName = data.get("lastName")
        passWord = data.get("passWord")
        email = data.get("email")
        liteLab = data.get("liteLab")
        passWord2 = data.get("passWord2")
        email2 = data.get("email2")
        institutionName = data.get("institutionName")
        db = Mysql(table_name="MYSQL")
        sql = """select * from register where email = \"%s\";""" % email
        data2 = db.fetch_one(sql)
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        if data2:
            result["success"]=False
            result["info"]="%s exists!"%email
        else:
            sql = ' insert into register values(UUID(), \"%s\", \"%s\", \"%s\",\"%s\", \"%s\", \"%s\"); ' % (firstName, lastName, passWord, email, liteLab, institutionName)
            db.execute(sql)
            sql = "select * from register where passWord=\"%s\" and email=\"%s\";" % (passWord, email)
            out = db.fetch_one(sql)
            register_id = out[0]
            try:
                sql_login = "insert into login values(\"%s\",\"%s\", UUID(), \"%s\");" % (email, passWord, register_id)
                db.execute(sql_login)
            except Exception:
                sql_login_create = "create table if not exists login (ID VARCHAR(60), REGISTER_ID VARCHAR(60), userName VARCHAR(20), passWord VARCHAR(20))DEFAULT CHARSET = UTF8;"
                db.execute(sql_login_create)
                sql_login = "insert into login values(\"%s\",\"%s\", UUID(), \"%s\");" % (email, passWord, register_id)
                db.execute(sql_login)
            result["success"]=True
            result["info"]=data
        db.commit()
        return json.dumps(result, ensure_ascii=False)

@app_flask.route('/sample', methods=['POST'])
def query_sample():
        data = request.form
        result={}
        project_info = str(data.get("panelType")) # panel类型
        sampletype = str(data.get("sampleType"))  # 样品类型
        samplename = str(data.get("sampleName"))  # 过滤字段
        username = data.get("userName")
        size = int(data.get("size"))
        page = int(data.get('page'))
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        sample_mysql = Mysql(table_name="PC_SAMPLE")
        register_mysql = Mysql(table_name="MYSQL")
        sql = "select * from login where userName=\"%s\";" %  username
        out = register_mysql.fetch_one(sql)
        login_id = out[2]
        sql = "select * from sample where login_ID=\"%s\"order by datetime desc;" % login_id
        out_data = sample_mysql.fetch_all(sql)
        data = []
        if out_data:
            id = 0
            for out1 in out_data:
                id = out1[0]
                sample_name = out1[2]
                sample_id = sample_name
                sample_detail = out1[3]
                sample_detail_1=out1[4]
                project = out1[6]
                sample_type = out1[7]
                imported_on = out1[10]
                sample_num = out1[11]
                r1_r2_data = [{"key":"R1","value":sample_detail},{"key":"R2","value":sample_detail_1}]
                if project_info and samplename and sampletype:
                    if samplename == sample_id and project_info == project and sampletype == sample_type:
                        return_json = {"sampleName": sample_id, "data": r1_r2_data, "panelType": project,
                                       "sampleType": sample_type, "importedOn": imported_on,"id":id,"sampleNum":sample_num}
                    else:
                        continue
                elif project_info and samplename and not sampletype:
                    if project_info == project and sample_id==samplename:
                        return_json = {"sampleName": sample_id, "data": r1_r2_data, "panelType": project,
                                       "sampleType": sample_type, "importedOn": imported_on, "id": id,"sampleNum":sample_num}
                    else:
                        continue
                elif project_info and not samplename and not sampletype:
                    if project_info == project:
                        return_json = {"sampleName": sample_id, "data": r1_r2_data, "panelType": project,
                                       "sampleType": sample_type, "importedOn": imported_on, "id": id,"sampleNum":sample_num}
                    else:
                        continue
                elif not project_info and samplename and sampletype:
                    if sample_id == samplename and sampletype == sample_type:
                        return_json = {"sampleName": sample_id, "data": r1_r2_data, "panelType": project,
                                       "sampleType": sample_type, "importedOn": imported_on, "id": id,"sampleNum":sample_num}
                    else:
                        continue
                elif not project_info and not samplename and sampletype:
                    if sampletype == sample_type:
                        return_json = {"sampleName": sample_id, "data": r1_r2_data, "panelType": project,
                                       "sampleType": sample_type, "importedOn": imported_on, "id": id,"sampleNum":sample_num}
                    else:
                        continue
                elif not project_info and samplename and not sampletype:
                    if sample_id == samplename:
                        return_json = {"sampleName": sample_id, "data": r1_r2_data, "panelType": project,
                                       "sampleType": sample_type, "importedOn": imported_on, "id": id,"sampleNum":sample_num}
                    else:
                        continue
                elif project_info and not samplename and sampletype:
                    if project_info == project and sampletype == sample_type:
                        return_json = {"sampleName": sample_id, "data": r1_r2_data, "panelType": project,
                                       "sampleType": sample_type, "importedOn": imported_on, "id": id,"sampleNum":sample_num}
                    else:
                        continue
                elif not project_info and not samplename and not sampletype:
                    return_json = {"sampleName": sample_id, "data": r1_r2_data, "panelType": project,
                                   "sampleType": sample_type, "importedOn": imported_on, "id": id,"sampleNum":sample_num}
                data.append(return_json)
            range_tmp = range(len(data))
            mod = len(data) % size  # 取余
            reminder = int(len(data) / size)
            if mod != 0:
                if page == (reminder+1):
                    range_id = range_tmp[(size * (page - 1)):len(data)]
                else:
                    range_id = range_tmp[(size * (page - 1)):(size * (page))]
            else:
                range_id = range_tmp[(size * (page - 1)):(size * page)]
            out_json = []
            for index in range_id:
                out_json.append(data[index])
            length = str(len(out_json))
            total = str(len(data))
            result["success"]=True
            result["info"]=json.dumps(out_json)
            result["length"]=length
            result["total"]=total
            # return_info = '{"success":true, "info": %s, "length":%s, "total":%s}' % (json.dumps(out_json), length, total)
        else:
            result["success"]=False
            result["info"]="wrong!"
            # return_info = '{"success":false, "info": "wrong!" }'
        sample_mysql.commit()
        register_mysql.commit()
        return json.dumps(result, ensure_ascii=False)
        # resp.body = return_info

@app_flask.route('/project', methods=['POST'])
def project_name():
        data = request.form
        type = data.get("type")   # ngs 和 noNgs类型判断
        version = data.get("version")   # 版本号判断
        db = Mysql(table_name="REPORT_MYSQL")
        sql = """select * from projectName;"""
        project_tmp = db.fetch_all(sql)
        data = []
        result={}
        total_version = []
        reserved_project = ["普晟惠-PD-L1及CD8蛋白表达检测", "普晟惠-MSI微卫星不稳定性检测","普晟畅-结直肠癌靶向用药12基因检测","普晟朗-肺癌靶向用药15基因检测", "普晟和-肿瘤靶向化疗用药83基因检测","普益康-肿瘤个体化诊疗620基因检测"]
        if type == "非ngs":
            filter_type = "noNgs"
        else:
            filter_type = type
        if project_tmp:
            for d in project_tmp:
                if d[1] in reserved_project and filter_type == d[5]:
                    if not version:
                        tmp = {"title": d[1], "text": "", "url": "",'type':d[5], "version":d[3]}
                        data.append(tmp)
                    elif version == d[3]:
                        tmp = {"title": d[1], "text": "", "url": "", 'type': d[5], "version": d[3]}
                        data.append(tmp)
                    if d[3] not in total_version:
                        total_version.append(d[3])
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        result["success"]=True
        result["info"]=data
        result["version"]=total_version
        return json.dumps(result, ensure_ascii=False)
        # return_info = {"success":True, "info": data, "version":total_version}

@app_flask.route('/reportinfo', methods=['POST'])
def reportInfo():
        data = request.form
        result={}
        sample_code = data.get("sampleCode")   # 样本编号
        project = data.get("title")  # 报告模板
        report_name = data.get("reportName")   # 文件名
        user_name = data.get("userName")
        workflow_name = data.get("workflowName")  # 报告结果名称
        print(sample_code,project,report_name,user_name,workflow_name)

        tumorInfiltrating = data.get("tumorInfiltrating")
        pd28Tumor = data.get("pd28Tumor")
        pd28Lymph = data.get("pd28Lymph")
        pd142Tumor = data.get("pd142Tumor")
        pd142Lymph = data.get("pd142Lymph")
        cd8 = data.get("cd8")
        tumorPercent = data.get("tumorPercent")
        tumorLevel = data.get("tumorLevel")  #msi稳定性判断

        msiStable = data.get("msiStable")  #判断稳定或者不稳定
        # uid= data['uid']
        filenameLeft = data.get('filenameLeft')
        filenameRight = data.get('filenameRight')
        uidleft = data.get('uidLeft')
        uidright = data.get('uidRight')
        db = Mysql(table_name="REPORT_MYSQL")
        if not uidleft:
            uidLeft = None
        else:
            sql = """select * from png where ID=\"%s\";""" % uidleft
            data = db.fetch_one(sql)
            uidLeft = os.path.join(data[-1], data[-2])
        if not uidright:
            uidRight = None
        else:
            sql = """select * from png where ID=\"%s\";""" % uidright
            data = db.fetch_one(sql)
            uidRight = os.path.join(data[-1], data[-2])
        msi_list = {"NR21":None,"NR24":None,"NR27":None,
                    "BAT25":None,"BAT26":None,"MONO27":None,"PentaC":None,"PentaD":None}
        print('msiStable', msiStable)
        if msiStable:
            for item in msi_list.keys():
                if item in msiStable.split("_"):
                    msi_list[item] = "不稳定"
                else:
                    msi_list[item] = "稳定"
            print('msi_list', msi_list)
        reportStable = data.get("reportStable")
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        mysql = Mysql(table_name="MYSQL")
        sql = "select * from login where userName=\"%s\";" % user_name
        data1 = mysql.fetch_one(sql)
        print('data1', data1)
        if data1:
            usernameid = data1[-1]
            print(usernameid)
            # out_path = "/home/khl/web/dist/downloads/tmp
            out_path = cc_download_path(type="dev")
            print('out_path',out_path)
            print('ahahahaha')
            # out_path = "/home/khl/web/cc_dist_test/downloads/tmp"
            if "组织版" in project:
                project_name = project.split('-组织版')[0]
                type = "组织版"
            elif "血液版" in project:
                project_name = project.split('-血液版')[0]
                type = "血液版"
            else:
                project_name = project
                type = None
            if type:
                sql = "select * from projectName where projectName=\"%s\" and type = \"%s\";" % (project_name, type)
            else:
                sql = "select * from projectName where projectName=\"%s\";" % project_name
            data = db.fetch_one(sql)
            projectname_id = data[0]
            analysis_name = data[1]
            xml_path = data[8]
            if data:
                print('xml_path', xml_path)
                if project_name == "普晟惠-PD-L1及CD8蛋白表达检测":
                    tumor_infiltrating = get_tumor_infiltrating(tumorInfiltrating, pd28Tumor, pd28Lymph,
                                            pd142Tumor,pd142Lymph, cd8,tumorPercent, tumorLevel)
                    msi_info = None
                elif project_name == "普晟惠-MSI微卫星不稳定性检测":
                    msi_info = get_msi_info(NR21=msi_list['NR21'], NR24=msi_list['NR24'],
                                            NR27=msi_list['NR27'], BAT25=msi_list['BAT25'], BAT26=msi_list['BAT26'],
                                            MONO27=msi_list['MONO27'], PentaC=msi_list['PentaC'],
                                            PentaD=msi_list['PentaD'],reportStable=reportStable)
                    print('msi_info', msi_info)
                    tumor_infiltrating = None
                else:
                    tumor_infiltrating = None
                    msi_info = None
                pdfpath, pdfurl = templateword(xml_path, out_path, report_name, sample_code, project_name, usernameid, type, tumor_infiltrating=tumor_infiltrating, msi_info=msi_info, image_left=uidLeft,image_right=uidRight)
                print('pdfpath',pdfpath,'pdfurl',pdfurl)
                ###ID,templateID,analysisName,sampleName,workflowName,DATETIME,STATUS,path,reportName,pdfPath,pdfUrl,userNameId)
                #sql_tmp = "insert into report(ID,templateID,analysisName,sampleName,workflowName,DATETIME,STATUS,path,reportName,pdfPath,pdfUrl,userNameId) values(UUID(), \"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")"
                sql_tmp = "insert into report values(UUID(), \"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")"
                cc_path_tmp = cc_path(type="dev")
                sql = sql_tmp % (
                projectname_id, analysis_name, sample_code, workflow_name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "完成", cc_path_tmp, report_name, pdfpath, pdfurl, usernameid)
                print(sql)
                db.execute(sql)
                db.commit()
                result["success"]=True
                result["info"]="Report generation success!"
            else:
                result["success"]=False
                result["info"]="Report generation failure!"
        else:
            result["success"]=False
            result["info"]="Report generation failure!"
            # resp.body = '{"success":false, "info": "Report generation failure!" }'
        return json.dumps(result, ensure_ascii=False)

@app_flask.route('/workflow', methods=['POST'])
def workflow():
        data = request.form
        user_name = data.get("userName")
        size = int(data.get("size"))
        page = int(data.get('page'))
        queryversion = data.get("version")
        filter = data.get("filter")
        i = 0
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        outversion = []  # 列表，嵌套字典
        totalversion = []  # 列表 存储unique version信息
        mysql = Mysql(table_name="MYSQL")
        sql = "select * from login where userName=\"%s\";" % user_name
        data = mysql.fetch_one(sql)
        result = {}
        if data:
            usernameid = data[-1]
            db = Mysql(table_name="REPORT_MYSQL")
            """{title: '分析名称',key: 'analysisName'},
                {title: '样本名称',key: 'sampleName'},
                {title: '流程名称',key: 'flowName'},
                {title: '版本',key: 'version'},
                {title: '日期',key: 'date'},
                {title: '状态',key: 'status'},"""
            sql = "select * from report where userNameId=\"%s\" order by datetime desc;" % usernameid
            info = []
            data = db.fetch_all(sql)
            sql = "select * from projectName;"
            projectName_id_tmp = db.fetch_all(sql)
            projectName_id_list = {}
            cc_path_tmp = cc_path(type="dev")
            cc_url_tmp = cc_url(type="dev")
            for p in projectName_id_tmp:
                projectName_id_list[p[0]] = p
            if data:
                for tmp in data:
                    analysisName=tmp[2]
                    sampleName=tmp[3]
                    flowName=tmp[4]
                    projectid = tmp[1]
                    if projectid in projectName_id_list.keys():
                        version = projectName_id_list[projectid][3]  #添加version信息
                        author = projectName_id_list[projectid][6]   #添加author信息
                        date = tmp[5]
                        status = tmp[6]
                        oldpdfpath = tmp[-3]
                        oldpdfurl = tmp[-2]
                        pdfpath = oldpdfpath.replace(cc_path_tmp, cc_url_tmp)
                        pdfurl = oldpdfurl.replace(cc_path_tmp, cc_url_tmp)
                        sample_code = tmp[3]  # 样本编号
                        report_name = os.path.basename(oldpdfpath)
                        if version not in totalversion:
                            tmp_data = {"key": version, "value": version}
                            totalversion.append(version)
                            outversion.append(tmp_data)
                            i += 1
                        if filter and queryversion:
                            if ((filter in analysisName  or filter in sampleName) and version == queryversion):
                                aaaa = {"title": analysisName, "sampleName":sampleName ,"author":author,
                                        "reportName":report_name, "sampleCode":sample_code,
                                        "workflowName": flowName, "version": version, "date": date, "status": status,
                                        "pdfpath": pdfpath, "pdfurl": pdfurl, "uniqueId": tmp[0]}
                                info.append(aaaa)
                        elif filter and not queryversion:
                            if filter in analysisName  or filter in sampleName:
                                aaaa = {"title": analysisName, "sampleName": sampleName, "author":author,
                                        "reportName": report_name, "sampleCode": sample_code, "workflowName": flowName,
                                        "version": version, "date": date, "status": status,
                                        "pdfpath": pdfpath, "pdfurl": pdfurl, "uniqueId": tmp[0]}
                                info.append(aaaa)
                        elif not filter and queryversion:
                            if version == queryversion:
                                aaaa = {"title": analysisName, "sampleName": sampleName, "author":author,
                                        "reportName": report_name, "sampleCode": sample_code,
                                        "workflowName": flowName, "version": version, "date": date,
                                        "status": status,
                                        "pdfpath": pdfpath, "pdfurl": pdfurl, "uniqueId": tmp[0]}
                                info.append(aaaa)
                        elif not filter and not queryversion:
                            aaaa = {"title": analysisName, "sampleName": sampleName,"author":author,
                                    "reportName": report_name, "sampleCode": sample_code,
                                    "workflowName": flowName, "version": version, "date": date, "status": status,
                                    "pdfpath": pdfpath, "pdfurl": pdfurl, "uniqueId": tmp[0]}
                            info.append(aaaa)
                    else:
                        result["success"] = False
                        result["info"] = "Report failure!"
                        # resp.body = json.dumps(result, ensure_ascii=False)
                range_tmp = range(len(info))
                mod = len(info) % size  # 取余
                reminder = int(len(info) / size)
                if mod != 0:
                    if page == (reminder + 1):
                        range_id = range_tmp[(size * (page - 1)):len(info)]
                    else:
                        range_id = range_tmp[(size * (page - 1)):(size * (page))]
                else:
                    range_id = range_tmp[(size * (page - 1)):(size * page)]
                out_json = []
                for index in range_id:
                    out_json.append(info[index])
                result["success"] = True
                result["length"] = str(len(out_json))
                result["total"] = str(len(info))
                result["totalVersion"] = outversion
                result["info"] = out_json
                # resp.body = json.dumps(result, ensure_ascii=False)
            else:
                result["success"] = True
                result["info"] = []
            return json.dumps(result, ensure_ascii=False)

@app_flask.route('/delete', methods=['POST'])
def deleteWorkflow():
        data = request.form
        uniqueid = data.get("id")
        result={}
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        db = Mysql(table_name="REPORT_MYSQL")
        sql = "select * from report where ID=\"%s\";" % uniqueid
        data = db.fetch_one(sql)
        if data:
            sql = "delete from report where ID=\"%s\"" % uniqueid
            try:
                db.execute(sql)
                db.commit()
                result["success"]=True
                result["info"]="删除成功"
            except Exception:
                result["success"] = False
                result["info"] = "删除失败!"
        else:
            result["success"] = True
            result["info"] = "删除成功"
        return json.dumps(result, ensure_ascii=False)

@app_flask.route('/analysis', methods=['POST'])
def analysis():
        data = request.form
        result = {}
        user_name = data.get("userName")
        size = int(data.get("size"))
        page = int(data.get('page'))
        queryversion = data.get("version")
        filter = data.get("filter")
        ngs_type = data.get("type")  # 添加过滤参数  all ngs noNgs
        db = Mysql(table_name="REPORT_MYSQL")
        sql = "select * from projectName;"
        outversion = []  # 列表，嵌套字典
        totalversion = []  # 列表 存储unique version信息
        i = 0
        data=db.fetch_all(sql)
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        if data:
            result["success"] = True
            info = []
            for d in data:
                description = d[1]
                application = d[1]
                version = d[3]
                date = d[2]
                author = d[6]
                tmp_url = d[7]
                word_template_path = cc_word_template()
                cc_word_url_tmp = cc_word_url(type="dev")
                if tmp_url:
                    url = tmp_url.replace(word_template_path, cc_word_url_tmp)
                else:
                    url = None
                if version not in totalversion:
                    if ngs_type == "ngs" or ngs_type == "noNgs":
                        if d[5] == ngs_type:
                            tmp = {"key":version,"value":version}
                            totalversion.append(version)
                            outversion.append(tmp)
                            i += 1
                        else:
                            continue
                    else:
                        tmp = {"key": version, "value": version}
                        totalversion.append(version)
                        outversion.append(tmp)
                        i += 1
                if filter and queryversion:
                    if filter in application and version == queryversion:
                        if ngs_type == "ngs" or ngs_type == "noNgs":
                            if ngs_type == d[5]:
                                info_tmp = {"description":description,"application":application,
                                    "version":version,"date":date, 'author': author, 'url':url}
                                info.append(info_tmp)
                            else:
                                continue
                        else:
                            info_tmp = {"description": description, "application": application,
                                        "version": version, "date": date, 'author':author, 'url':url}
                            info.append(info_tmp)
                elif filter and not queryversion:
                    if filter in application:
                        if ngs_type == "ngs" or ngs_type == "noNgs":
                            if ngs_type == d[5]:
                                info_tmp = {"description": description, "application": application,
                                            "version": version, "date": date, 'author':author, 'url':url}
                                info.append(info_tmp)
                            else:
                                continue
                        else:
                            info_tmp = {"description": description, "application": application,
                                        "version": version, "date": date, 'author':author, 'url':url}
                            info.append(info_tmp)
                elif not filter and queryversion:
                    if version == queryversion:
                        if ngs_type == "ngs" or ngs_type == "noNgs":
                            if ngs_type == d[5]:
                                info_tmp = {"description": description, "application": application,
                                            "version": version, "date": date, 'author':author, 'url':url}
                                info.append(info_tmp)
                            else:
                                continue
                        else:
                            info_tmp = {"description": description, "application": application,
                                        "version": version, "date": date, 'author':author, 'url':url}
                            info.append(info_tmp)
                elif not filter and not queryversion:
                    if ngs_type == "ngs" or ngs_type == "noNgs":
                        if ngs_type == d[5]:
                            info_tmp = {"description": description, "application": application,
                                        "version": version, "date": date, 'author':author, 'url':url}
                            info.append(info_tmp)
                        else:
                            continue
                    else:
                        info_tmp = {"description": description, "application": application,
                                    "version": version, "date": date, 'author':author, 'url':url}
                        info.append(info_tmp)
            range_tmp = range(len(info))
            mod = len(info) % size  # 取余  8
            reminder = int(len(info) / size)   # 3
            if mod != 0:
                if page == (reminder+1):
                    range_id = range_tmp[(size * (page - 1)):len(info)]
                else:
                    range_id = range_tmp[(size * (page - 1)):(size * (page))]
            else:
                range_id = range_tmp[(size * (page - 1)):(size * page)]
            out_json = []
            for index in range_id:
                out_json.append(info[index])
            result["info"] = out_json
            result["length"] = str(len(out_json))
            result["total"] = str(len(info))
            result["totalVersion"] = outversion
            # resp.body = json.dumps(result, ensure_ascii=False)
        else:
            result["success"] = False
            result["info"] = "Report failure!"
            # resp.body = json.dumps(result, ensure_ascii=False)
        return json.dumps(result, ensure_ascii=False)

@app_flask.route('/cc_analysis', methods=['POST'])
def cc_analysis():
        data = request.form
        result = {}
        user_name = data.get("userName")
        size = int(data.get("size"))
        page = int(data.get('page'))
        version = data.get("version")
        filter = data.get("filter")
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        db = Mysql(table_name="PC_SAMPLE")
        sql = """select * from pipelineName;"""
        data_total = db.fetch_all(sql)
        if data_total:
            info = []
            totalversion = []
            totalversionlist = []
            for data in data_total:
                if data[3] not in totalversionlist:
                    totalversionlist.append(data[3])
                    totalversion.append({"key":data[3],"value":data[3]})
                if filter and version:
                    if filter in applicationName and version == data[3]:
                        tmp_info = {"applicationName":data[1],"applicationDescription":data[1],
                                    "author":"","version":data[3],"datetime":data[6]}
                        info.append(tmp_info)
                if filter and not version:
                    if filter in applicationName:
                        tmp_info = {"applicationName": data[1], "applicationDescription": data[1],
                                    "author": "", "version": data[3], "datetime": data[6]}
                        info.append(tmp_info)
                if not filter and version:
                    if version == data[3]:
                        tmp_info = {"applicationName": data[1], "applicationDescription": data[1],
                                    "author": "", "version": data[3], "datetime": data[6]}
                        info.append(tmp_info)
                if not filter and not version:
                    tmp_info = {"applicationName": data[1], "applicationDescription": data[1],
                                "author": "", "version": data[3], "datetime": data[6]}
                    info.append(tmp_info)
            range_tmp = range(len(info))
            mod = len(info) % size  # 取余  8
            reminder = int(len(info) / size)  # 3
            if mod != 0:
                if page == (reminder + 1):
                    range_id = range_tmp[(size * (page - 1)):len(info)]
                else:
                    range_id = range_tmp[(size * (page - 1)):(size * (page))]
            else:
                range_id = range_tmp[(size * (page - 1)):(size * page)]
            out_json = []
            for index in range_id:
                out_json.append(info[index])
            # print('out_json', len(out_json))
            # print('range_id', size * page, size * (page + 1), range_id)
            print(out_json)
            print(str(len(info)))
            result["info"] = out_json
            result["length"] = str(len(out_json))
            result["total"] = str(len(info))
            result["totalVersion"] = totalversion
            result["success"] = True
            # resp.body = json.dumps(result, ensure_ascii=False)
        else:
            result["success"] = False
            result["info"] = "Report failure!"
            # resp.body = json.dumps(result, ensure_ascii=False)
        return json.dumps(result, ensure_ascii=False)

@app_flask.route('/analysisquery', methods=['POST'])
def analysisquery():
        data = request.form
        result = {}
        user_name = data.get("userName")
        size = int(data.get("size"))
        page = int(data.get('page'))
        queryversion = data.get("version")
        filter = data.get("filter")
        db = Mysql(table_name="REPORT_MYSQL")
        sql = "select * from projectName;"
        outversion = []  # 列表，嵌套字典
        totalversion = []  # 列表 存储unique version信息
        i = 0
        data=db.fetch_all(sql)
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        if data:
            result["success"] = True
            info = []
            for d in data:
                description = d[1]
                application = d[1]
                version = d[3]
                date = d[2]
                if version not in totalversion:
                    tmp = {}
                    tmp[str(i)] = version
                    outversion.append(tmp)
                    i += 1
                if filter and queryversion:
                    if filter in application and version == queryversion:
                        info_tmp = {"description":description,"application":application,
                            "version":version,"date":date}
                        info.append(info_tmp)
                elif filter and not queryversion:
                    if filter in application:
                        info_tmp = {"description": description, "application": application,
                                    "version": version, "date": date}
                        info.append(info_tmp)
                elif not filter and queryversion:
                    if version == queryversion:
                        info_tmp = {"description": description, "application": application,
                                    "version": version, "date": date}
                        info.append(info_tmp)
                elif not filter and not queryversion:
                    info_tmp = {"description": description, "application": application,
                                "version": version, "date": date}
                    info.append(info_tmp)
            range_tmp = range(len(info))
            mod = len(info) % size  # 取余
            reminder = int(len(info) / size)
            if mod != 0:
                if page == 1:
                    range_id = range_tmp[0:size]
                elif page == (reminder - 1):
                    range_id = range_tmp[(size * (page - 1)):len(info)]
                else:
                    range_id = range_tmp[(size*page):mod]
                    #range_id = range_tmp[(size * (page - 1)):(size * page)]
            else:
                range_id = range_tmp[(size * (page - 1)):(size * page)]
            out_json = []
            for index in range_id:
                out_json.append(info[index])
            result["info"] = out_json
            result["length"] = str(len(out_json))
            result["total"] = str(len(info))
            result["totalVersion"] = outversion
            # resp.body = json.dumps(result, ensure_ascii=False)
        else:
            result["success"] = False
            result["info"] = "Report failure!"
            # resp.body = json.dumps(result, ensure_ascii=False)
        return json.dumps(result, ensure_ascii=False)

@app_flask.route('/sampleinfo', methods=['POST'])
def GetSampleInfo():
        """根据样本的编写获得样本的其他信息"""
        data = request.form
        samplename = data.get("sampleName")
        db = Mysql(table_name="GLORIA_MYSQL")
        sql = """select * from sample_mx where S_MCODE = \"%s\";""" % samplename
        data = db.fetch_all(sql)
        result={}
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        if data:
            result["success"]=True
            result["info"]="样本存在!"
            # result = '{"success":true, "info": "样本存在!" }'
        else:
            result["success"]=False
            result["info"]="样本不存在!"
            # result = '{"success":false, "info": "样本不存在!" }'
        # resp.body = result
        return json.dumps(result, ensure_ascii=False)

@app_flask.route('/sample_name', methods=['POST'])
def sample_name():
        data = request.form
        project_name = data.get("projectName")
        db = Mysql(table_name="PC_SAMPLE")
        sql = """SELECT * FROM serverSampleName a,pipelineName AS p WHERE a.pipelineId=p.ID AND p.pipeline=\"%s\";""" % project_name
        tmp_info = db.fetch_all(sql)
        project_info = []
        sample_id = []
        result={}
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        if tmp_info:
            for i in tmp_info:
                if i[3] not in sample_id:
                    sample_id.append(i[3])
                    project_info.append({"key":i[3],"value":i[3]})
            result["success"]=True
            result["info"]=project_info
            # return_info = {"success": True, "info": project_info}
        else:
            result["success"] = False
            result["info"] = "数据返回失败!"
            # return_info = {"success": False, "info": "数据返回失败!"}
        #拉出来所有的样本信息
        return json.dumps(result, ensure_ascii=False)

@app_flask.route('/define_sample', methods=['POST'])
def define_sample_name():
        """定义样本信息 保存并运行"""
        # return_json = {"sampleName": sample_id, "sampleDetail": sample_detail, "project": project,
        #                "sampleType": sample_type, "role": role, "importedBy": imported_by,
        #                "importedOn": imported_on}
        data = request.form
        panel_type = data.get("panelType")
        data_r1_id = os.path.split(data.get("dataR1Id"))[0]
        data_r2_id = os.path.split(data.get("dataR2Id"))[0]
        data_r1_name = data.get('dataR1Name')
        data_r2_name = data.get('dataR2Name')
        sample_type = data.get("sampleType")
        sample_name = data.get("sampleName")
        userName = data.get("userName")
        sample_num = data.get("sampleNum")
        id = data.get("id")
        sample_mysql = Mysql(table_name="PC_SAMPLE")
        register_mysql = Mysql(table_name="MYSQL")
        sql = "select * from login where userName=\"%s\";" % userName
        out = register_mysql.fetch_one(sql)
        login_id = out[2]
        result = {}
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        if login_id:
            if not id:
                # id为空，暂定保存第一条信息
                sql = """select * from serverSampleNameNew where path=\'%s\' and sample_detail=\'%s\' and sample_detail_1=\'%s\';""" % (data_r1_id,data_r1_name,data_r2_name)
                data1 = sample_mysql.fetch_all(sql)
                if data1:
                    #向sample 数据库插入样本信息
                    tmp_sql = """insert into sample values(UUID(),\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\","",now(),\"%s\")"""
                    sql = tmp_sql % (login_id,sample_name,data_r1_name,data_r2_name,data_r1_id,panel_type,sample_type,"",sample_num)
                    sample_mysql.execute(sql)
                    result["success"] = True
                    result["info"] = "success!"
                else:
                    result["success"] = False
                    result["info"] = "fail!"
            else:
                tmp_sql = """update sample set sample_type=\"%s\",panelType=\"%s\",sample_name=\"%s\",sample_detail=\"%s\",sample_detail_1=\"%s\",path=\"%s\", datetime=\"%s\",sample_num=\"%s\" where ID=\"%s\";"""
                path = os.path.split(data_r1_id)[0]
                print(sample_type,panel_type,sample_name,sample_num,data_r1_name)
                sql = tmp_sql % (sample_type,panel_type,sample_name,data_r1_name,data_r2_name,path,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),id)
                sample_mysql.execute(sql)
                sample_mysql.commit()
                result["success"] = True
                result["info"] = "success!"
        else:
            result["success"] = False
            result["info"] = "fail"
        return json.dumps(result, ensure_ascii=False)

@app_flask.route('/pipeline_analysis', methods=['POST'])
def pipeline_analysis():
        data = request.form
        filter = data.get("filter")
        size = int(data.get("size"))
        page = int(data.get("page"))
        userName = data.get("userName")
        status = data.get("status")
        ### 研究应用 工作流名称 版本 参考 样本组 日期
        mysql = Mysql(table_name="MYSQL")
        pipeline_mysql = Mysql(table_name="PC_SAMPLE")
        sql = """select * from login where userName=\"%s\";""" % userName
        d = mysql.fetch_one(sql)
        info = []
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        result = {}
        if d:
            usernameId = d[2]
            sql = """select * from pipelineWorkflow where usernameId=\"%s\" order by datetime desc;""" % usernameId
            d1 = pipeline_mysql.fetch_all(sql)
            if d1:
                for l in d1:
                    if filter and status:
                        if filter in l[3] and status ==  l[8]:
                            tmp_info = {"application":l[2],"workflowName":l[3],"version":l[4],"reference":l[5],
                                        "sampleGroup":l[6],"datetime":l[7],'status':l[8],"id":l[0]}
                            info.append(tmp_info)
                    elif not filter and status:
                        if status == l[8]:
                            tmp_info = {"application": l[2], "workflowName": l[3], "version": l[4], "reference": l[5],
                                        "sampleGroup": l[6], "datetime": l[7], 'status': l[8],"id":l[0]}
                            info.append(tmp_info)
                    elif filter and not status:
                        if filter in l[3]:
                            tmp_info = {"application": l[2], "workflowName": l[3], "version": l[4], "reference": l[5],
                                        "sampleGroup": l[6], "datetime": l[7], 'status': l[8],"id":l[0]}
                            info.append(tmp_info)
                    elif not filter and not status:
                        tmp_info = {"application": l[2], "workflowName": l[3], "version": l[4], "reference": l[5],
                                    "sampleGroup": l[6], "datetime": l[7], 'status': l[8],"id":l[0]}
                        info.append(tmp_info)
                range_tmp = range(len(info))
                mod = len(info) % size  # 取余
                reminder = int(len(info) / size)
                if mod != 0:
                    if page == (reminder + 1):
                        range_id = range_tmp[(size * (page - 1)):len(info)]
                    else:
                        range_id = range_tmp[(size * (page - 1)):(size * (page))]
                else:
                    range_id = range_tmp[(size * (page - 1)):(size * page)]
                out_json = []
                for index in range_id:
                    out_json.append(info[index])
                result["success"] = True
                result["length"] = str(len(out_json))
                result["total"] = str(len(info))
                result["info"] = out_json
            else:
                result["success"] = False
                result["info"] = "Failure!"
        else:
            result["success"] = False
            result["info"] = "Failure!"
        return json.dumps(result, ensure_ascii=False)

@app_flask.route('/workflow_name', methods=['POST'])
def workflow_name():
        data = request.form
        # project_name = params["projectName"]
        db = Mysql(table_name="PC_SAMPLE")
        sql = """select * from pipelineName;"""
        data = db.fetch_all(sql)
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        project_info = []
        result = {}
        out = []
        if data:
            for l in data:
                if l[1] not in out:
                    out.append(l[1])
                    tmp_info = {"key":l[1],"value":l[1]}
                    project_info.append(tmp_info)
                else:
                    continue
            result["success"] = True
            result["info"] = project_info
        else:
            result["success"] = False
            result["info"] = "Failure!"
        return json.dumps(result, ensure_ascii=False)

@app_flask.route('/sample_code', methods=['POST'])
def sample_code():
        data = request.form
        project_name = data.get("projectName")
        db = Mysql(table_name="PC_SAMPLE")
        sql = """SELECT * FROM pipelineName p, serverSampleName s WHERE p.ID=s.pipelineId AND p.pipeline=\"%s\";""" % project_name
        data = db.fetch_all(sql)
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        result = {}
        tumor = []
        normal = []
        if data:
            for l in data:
                if l[13] == "tumor":
                    tmp_tumor = {"key":l[10], "value": l[10]}
                    tumor.append(tmp_tumor)
                if l[13] == "normal":
                    tmp_normal = {"key":l[10], "value": l[10]}
                    normal.append(tmp_normal)
            result["success"] = True
            result["info"] = {"tumor":tumor,"normal":normal}
        else:
            result["success"] = False
            result["info"] = "Failure!"
        return json.dumps(result, ensure_ascii=False)

@app_flask.route('/config_json', methods=['POST'])
def config_json():
        data = request.form
        project_name = data.get("projectName")
        db = Mysql(table_name="PC_SAMPLE")
        sql = """select jsonPath from pipelineName where pipeline=\"%s\";""" % project_name
        data = db.fetch_all(sql)
        result = {}
        info = []
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        if data:
            for l in data:
                tmp_info = {"key":os.path.basename(l[0]),'value':os.path.basename(l[0])}
                info.append(tmp_info)
                result["success"] = True
                result["info"] = info
        else:
            result["success"] = False
            result["info"] = "Failure!"
        return json.dumps(result, ensure_ascii=False)

@app_flask.route('/run_pipeline', methods=['POST'])
def run_pipeline():
        data = request.form
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        project_name = data.get("projectName")
        user_name = data.get("userName")
        tumor_id = data.get("tumorId")
        normal_id = data.get("normalId")
        workflow_name = data.get("workflowName")
        save_run = data.get("saveRun")
        result = {}
        login_mysql = Mysql(table_name="MYSQL")
        sql = """select * from login where userName=\"%s\";""" % user_name
        data = login_mysql.fetch_one(sql)
        usernameId = data[2]
        sample_mysql = Mysql(table_name="PC_SAMPLE")
        sql = """select sample_name, sample_detail,sample_detail_1, path from sample where ID=\"%s\";""" % tumor_id
        tumor_data = sample_mysql.fetch_one(sql)
        if tumor_data:
            tumor_name = tumor_data[0]
            tumor_r1_data = os.path.join(tumor_data[3], tumor_data[1])
            tumor_r2_data = os.path.join(tumor_data[3], tumor_data[2])
        if normal_id:
            sql = """select sample_name, sample_detail,sample_detail_1, path from sample where ID=\"%s\";""" % normal_id
            normal_data = sample_mysql.fetch_one(sql)
            if normal_data:
                normal_name = normal_data[0]
                normal_r1_data = os.path.join(normal_data[3], normal_data[1])
                normal_r2_data = os.path.join(normal_data[3], normal_data[2])
        tumor_unique_name = os.path.basename(tumor_r1_data).split('.fastq.gz')[0]
        config_sql = """select * from pipelineName where pipeline=\"%s\";""" % project_name
        config_data = sample_mysql.fetch_one(config_sql)
        if config_data:
            config_json = config_data[2]
        else:
            # 备注 此处地方会报错!
            pass
        out_path = os.path.join(cc_pipeline_out_path(), "%s_%s" % (tumor_unique_name,datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')))
        if not os.path.exists(out_path):
            os.mkdir(out_path)
        """python3 /home/khl/dna/script/change2_pipeline.py  
        -tfq1 /home/khl/dna_data/raw_data/somatic/small/1720080_gDNA_S3_R1_001.fastq.gz 
        -tfq2 /home/khl/dna_data/raw_data/somatic/small/1720080_gDNA_S3_R2_001.fastq.gz 
        -tumor 1720080 -nfq1 /home/khl/dna_data/raw_data/somatic/small/1720076_gDNA_S1_R1_001.fastq.gz 
        -nfq2 /home/khl/dna_data/raw_data/somatic/small/1720076_gDNA_S1_R2_001.fastq.gz 
        -normal 1720076 -O /home/khl/dna/script/Pair_somatic_16gene.json 
        -outdir /home/khl/dna_data/somatic/pipeline1"""
        # try:
        cmd_tmp = "nohup python3 /home/khl/dna/script/change2_pipeline.py -tfq1 %s -tfq2 %s -tumor %s -nfq1 %s "
        cmd_tmp += "-nfq2 %s -normal %s -O %s -outdir %s > %s 2>&1 &"
        cmd = cmd_tmp % (tumor_r1_data, tumor_r2_data, tumor_name, normal_r1_data, normal_r2_data, normal_name, config_json, out_path,os.path.join(out_path, "%s_logger" % datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')))
        os.system(cmd)
        tmp_sql = """insert into pipelineWorkflow values(UUID(),\"%s\",\"%s\",\"%s\","1.0","hg19","",now(),"doing",\"%s\")"""
        sql = tmp_sql % (usernameId, project_name, workflow_name, out_path)
        sample_mysql.execute(sql)
        # sample_mysql.commit()
        sql = """select * from pipelineWorkflow where usernameId=\"%s\" and application=\"%s\" and workflowName=\"%s\" order by datetime desc;""" % (usernameId,project_name,workflow_name)
        data = sample_mysql.fetch_all(sql)
        sample_mysql.commit()
        # path = out_path
        if data:
            id = data[0][0]
            cmd = "nohup python %s -id %s -path %s > %s 2>&1 &" % ("/home/khl/web/dev_web/update_pipeline_info.py",id,out_path,out_path+"/insert.info")
            p = subprocess.Popen(cmd, shell=True)
        result["success"] = True
        result["info"] = "程序提交成功!"
        return json.dumps(result, ensure_ascii=False)

@app_flask.route('/delete_sample', methods=['POST'])
def delete_sample():
        data = request.form
        id = data.get("id")
        db = Mysql(table_name="PC_SAMPLE")
        result = {}
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        try:
            sql = """delete from sample where ID=\"%s\";""" % id
            db.execute(sql)
            db.commit()
            result["success"] = True
            result["info"] = "删除成功!"
        except Exception as e:
            print(e)
            result["success"] = False
            result["info"] = e
        return json.dumps(result, ensure_ascii=False)

@app_flask.route('/hierarchy_catalogues', methods=['POST'])
def hierarchy_catalogues():
        data = request.form
        panel_type = data.get("panelType")
        result = {}
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        info = []
        path = "/home/khl/dna_data/raw_data"
        def get_file(fpath, level=0, mfile_list=None):
            if mfile_list == None:
                mfile_list = []
            parent = os.listdir(fpath)
            for child in parent:
                child_path = os.path.join(fpath, child)
                data = {}
                data["title"] = child
                data["id"] = child_path
                level += 1
                if os.path.isdir(child_path):
                    if os.listdir(child_path):
                        info = get_file(child_path, level + 1)
                        data["children"] = info
                        data["isDir"] = True
                        mfile_list.append(data)
                    else:
                        continue
                else:
                    data["isDir"] = False
                    mfile_list.append(data)
            return mfile_list

        info = [{"title":"raw_data","children":get_file(fpath=path),"isDir":True}]
        # result["children"] = get_file(fpath=path)
        result["success"] = True
        result["info"] = info
        return json.dumps(result, ensure_ascii=False)

@app_flask.route('/edit_sample', methods=['POST'])
def edit_sample():
        data = request.form
        id = data.get("id")
        db = Mysql(table_name="PC_SAMPLE")
        result = {}
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        sql = """select * from sample where ID=\"%s\";""" % id
        try:
            data = db.fetch_one(sql)
            if data:
                # panelType, sampleType,sampleName,dataR1Name,dataR2Name
                info = {"sampleName":data[2],"dataR1Name":data[3],"dataR2Name":data[4],
                        "panelType":data[6],"dataR1Id":os.path.join(data[5],data[3]),
                        "dataR2Id":os.path.join(data[5],data[4]),"sampleNum":data[11],
                        "sampleType":data[7]}
                result["info"] = info
                result["success"] = True
            else:
                result["info"] = "字段不存在"
                result["success"] = False
        except Exception as e:
            result["success"] = False
            result["info"] = e
            print(e)
        return json.dumps(result, ensure_ascii=False)

@app_flask.route('/delete_pipeline_analysis', methods=['POST'])
def delete_pipeline_analysis():
        data = request.form
        id = data.get("id")
        # log file bam 分别对应删除文件+日志 删除文件  删除bam文件
        delete_name_info = data.get("deleteName")
        print(">>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<")
        print(delete_name_info)
        db = Mysql(table_name="PC_SAMPLE")
        if delete_name_info == "log":
            sql = """delete from pipelineWorkflow where ID=\"%s\";""" % id
            db.execute(sql)
            db.commit()
        result = {}
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        result["success"] = True
        result["info"] = "info!"
        return json.dumps(result, ensure_ascii=False)


if __name__=="__main__":
    #运行app
    app.run(host="0.0.0.0",port=8093)

# app.add_route("/login", Login())
# app.add_route("/register", Register())
# app.add_route("/sample", query_sample())
# # app.add_route("/download", Download())
# app.add_route("/project", project_name())
# app.add_route("/sampleinfo", GetSampleInfo())
# app.add_route("/reportinfo", reportInfo())
# # app.add_route("/upload", upload())
# app.add_route("/workflow", workflow())
# app.add_route("/delete", deleteWorkflow())
# app.add_route("/analysis", analysis())
# app.add_route("/analysisquery", analysisquery())
# app.add_route("/taskOverview", taskOverview())
# ###添加样本名称
# app.add_route("/sample_name", sample_name())
# app.add_route("/define_sample", define_sample_name())
# app.add_route("/pipeline_analysis", pipeline_analysis())
# app.add_route("/workflow_name", workflow_name())
# app.add_route("/sample_code", sample_code())
# app.add_route("/config_json", config_json())
# # 运行工作流程序
# app.add_route("/run_pipeline", run_pipeline())
# # 删除定义的样本信息 delete_sample
# app.add_route("/delete_sample", delete_sample())
# app.add_route("/hierarchy_catalogues", hierarchy_catalogues())
# app.add_route("/edit_sample", edit_sample())
# app.add_route("/cc_analysis", cc_analysis())
# # delete_pipeline_analysis
# app.add_route("/delete_pipeline_analysis", delete_pipeline_analysis())

# app.add_route("/samplefilter", query_sample_filter())

# httpd = simple_server.make_server("192.168.1.144", 8099, app)
# httpd.serve_forever()
