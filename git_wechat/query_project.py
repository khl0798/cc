# -*- coding: utf-8 -*-
from query_project import *
import json
from project_conf import *
import time

def queryProject(username,useridcard,usertel):
    db = Mysql(table_name="GLORIA_MYSQL")
    ret = True
    sql = """SELECT mx.id, mx.STORAGE_STAGE, hp.h_chinese_name, hp.CHECK_PLATFORM, mx.SUBJECT_SEX FROM sample_mx mx, h_clinic_project hp ,H_SAMPLE_ITEM item WHERE mx.SUBJECT_NAME=\"%s\" AND mx.id=item.sample_id AND item.item_id=hp.ID;""" % username
    data = db.fetch_all(sql)
    data_list = {}
    data_project_list = {}
    for d in data:
        if d[0] not in data_list.keys():
            data_list[d[0]] = [d]
            data_project_list[d[0]] = [d[2]]
        else:
            tmp_value = data_list[d[0]]
            tmp_project_value = data_project_list[d[0]]
            tmp_value.append(d)
            tmp_project_value.append(d[2])
            data_list[d[0]] = tmp_value
            data_project_list[d[0]] = tmp_project_value
    sql_1 = """SELECT mx.id, rp.id, rp.RP_WORD_FILE, rp.RP_FILE, hp.h_chinese_name,hp.CHECK_PLATFORM ,mx.SUBJECT_SEX FROM SAMPLE_MX mx,REPORT_INFO rp, H_CLINIC_PROJECT hp WHERE mx.ID = rp.RP_SAMPLE_ID AND rp.CHECK_ITEM_ID=hp.ID AND mx.SUBJECT_NAME =\"%s\";""" % username
    data1 = db.fetch_all(sql_1)
    data_1 = {}
    project_list = []
    print("data_list")
    print(data_list)
    print("data_1")
    print(data_1)
    for d in data1:
        if d[0] not in project_list:
            project_list.append(d[0])
            data_1[d[0]] = [d]
        else:
            tmp_value = data_1[d[0]]
            tmp_value.append(d)
            data_1[d[0]] = tmp_value
    project_info = {}
    project_info[username] = {}
    project_info[username]["project"] = []
    project_info[username]["reportId"] = []
    project_info[username]["type"] = []
    # project_info[username]["main_id"] = []
    #data_list = {'648963e4-1376-453e-aadc-58d24d6dd45e': [('648963e4-1376-453e-aadc-58d24d6dd45e', '收样', '普晟惠-PD-L1及CD8蛋白表达检测', '外包', '男'), ('648963e4-1376-453e-aadc-58d24d6dd45e', '收样', '普益康-肿瘤个体化诊疗620基因检测-cfDNA', 'NGS', '男'), ('648963e4-1376-453e-aadc-58d24d6dd45e', '收样', '普晟惠-MSI微卫星不稳定性检测', '外包', '男')], 'bb9f990c-7385-4239-bc97-49143662e016': [('bb9f990c-7385-4239-bc97-49143662e016', '收样', '普晟惠-MSI微卫星不稳定性检测', '外包', '男'), ('bb9f990c-7385-4239-bc97-49143662e016', '收样', '普益康-肿瘤个体化诊疗620基因检测-gDNA', 'NGS', '男'), ('bb9f990c-7385-4239-bc97-49143662e016', '收样', '普晟惠-PD-L1及CD8蛋白表达检测', '外包', '男')], 'abb150e5-4282-48af-ab1a-cc5a23702506': [('abb150e5-4282-48af-ab1a-cc5a23702506', None, '普晟惠-PD-L1及CD8蛋白表达检测', '外包', '男'), ('abb150e5-4282-48af-ab1a-cc5a23702506', None, '普晟惠-MSI微卫星不稳定性检测', '外包', '男'), ('abb150e5-4282-48af-ab1a-cc5a23702506', None, '普益康-肿瘤个体化诊疗620基因检测-gDNA', 'NGS', '男')], '6fd17428-366d-416e-a753-5c837be473eb': [('6fd17428-366d-416e-a753-5c837be473eb', '收样', '普益康-肿瘤个体化诊疗620基因检测-gDNA', 'NGS', '男'), ('6fd17428-366d-416e-a753-5c837be473eb', '收样', '普晟惠-PD-L1及CD8蛋白表达检测', '外包', '男'), ('6fd17428-366d-416e-a753-5c837be473eb', '收样', '普晟惠-MSI微卫星不稳定性检测', '外包', '男')], 'bae41be0-6661-410d-bd5c-5fc6f97727fa': [('bae41be0-6661-410d-bd5c-5fc6f97727fa', None, '普晟惠-MSI微卫星不稳定性检测', '外包', '男'), ('bae41be0-6661-410d-bd5c-5fc6f97727fa', None, '普晟惠-PD-L1及CD8蛋白表达检测', '外包', '男'), ('bae41be0-6661-410d-bd5c-5fc6f97727fa', None, '普益康-肿瘤个体化诊疗620基因检测-gDNA', 'NGS', '男')]}
    #data_1 = {'bae41be0-6661-410d-bd5c-5fc6f97727fa': [('bae41be0-6661-410d-bd5c-5fc6f97727fa', '2e6e0ef2-10ba-4d8b-9408-2e05e64e3757', 'YHF1810078-王宏超-普益康-肿瘤个体化诊疗620基因检测-gDNA-20180403.doc', None, '普益康-肿瘤个体化诊疗620基因检测-gDNA', 'NGS', '男')], '6fd17428-366d-416e-a753-5c837be473eb': [('6fd17428-366d-416e-a753-5c837be473eb', '4fbfd89f-eedb-4a6b-a033-e1048172915c', 'YHF1810078-王宏超-普晟惠-MSI微卫星不稳定性检测-20180323_20180327095821124.doc', 'YHF1810078-王宏超-普晟惠-MSI微卫星不稳定性检测-20180323_20180327095814359.pdf', '普晟惠-MSI微卫星不稳定性检测', '外包', '男'), ('6fd17428-366d-416e-a753-5c837be473eb', 'ea10bebf-11a5-4972-a413-8810f6b12098', 'YHF1810078-王宏超-普晟惠-PD-L1及CD8蛋白表达检测-20180326_20180327044311261.doc', 'YHF1810078-王宏超-普晟惠-PD-L1及CD8蛋白表达检测-20180326_20180327044305605.pdf', '普晟惠-PD-L1及CD8蛋白表达检测', '外包', '男')]}
    print("hahahah现在开始数据库记录信息")
    #提取出所有sample_mx中对应的样本信息
    extract_total_project_info = {}
    for keys, values in data_list.items():
        extract_tmp_project_info = {"project": [], "reportId": [], "type": []}
        for tmp_value in values:
            subject_sex = tmp_value[4]
            if "-cfDNA" in tmp_value[2]:
                project = tmp_value[2].replace("-cfDNA", "")
            elif "-gDNA" in tmp_value[2]:
                project = tmp_value[2].replace("-gDNA", "")
            else:
                project = tmp_value[2]
            extract_tmp_project_info["project"].append(project)
            extract_tmp_project_info["type"].append(tmp_value[3])
            extract_tmp_project_info["reportId"].append("")
        extract_total_project_info[keys] = extract_tmp_project_info

    print("提取出全部的信息")
    print(extract_total_project_info)
    print("heiheihei现在开始查询报告信息及id")
    # id_name = {"project":[],"type":[],"reportId":[],"main_id":[],"subject_sex":[]}
    project_list = []
    for keys,values in data_list.items():
        if keys in data_1.keys():
            for value in data_1[keys]:
                subject_sex = value[6]
                if "-cfDNA" in value[4]:
                    project = value[4].replace("-cfDNA","")
                elif "-gDNA" in value[4]:
                    project = value[4].replace("-gDNA","")
                else:
                    project = value[4]
                project_info[username]["project"].append(project)
                project_info[username]["type"].append(value[5])
                # id_name["subject_sex"].append(value[6])
                project_info[username]["reportId"].append(value[1])
                # id_name["main_id"].append(keys)
                if value[4] not in project_list:
                    project_list.append(project)
    for keys,values in data_list.items():
        if len(project_list) != len(extract_total_project_info[keys]["project"]):
            for i in range(len(extract_total_project_info[keys]["project"])):
                if extract_total_project_info[keys]["project"][i] not in project_list:
                    project_info[username]["project"].append(extract_total_project_info[keys]["project"][i])
                    project_info[username]["type"].append(extract_total_project_info[keys]["type"][i])
                    project_info[username]["reportId"].append(extract_total_project_info[keys]["reportId"][i])
                    project_list.append(extract_total_project_info[keys]["project"][i])
        else:
            print('haha')
    if project_info:
        return project_info, ret
    else:
        ret = False
        return "",ret

class Analysis:
    def __init__(self, username,project):
        self.db = Mysql(table_name="GLORIA_MYSQL")
        import time
        self.username = username
        self.project = project
        self.project_conf = new_wechat_project()
    #入库时间
    def library(self):
        """SELECT mx.id, rp.RP_WORD_FILE, rp.RP_FILE, hp.h_chinese_name,hp.CHECK_PLATFORM ,mx.SUBJECT_SEX FROM SAMPLE_MX mx,REPORT_INFO rp, H_CLINIC_PROJECT hp WHERE mx.ID = rp.RP_SAMPLE_ID AND rp.CHECK_ITEM_ID=hp.ID AND mx.SUBJECT_NAME ="杨景云";"""
        sql = """select mx.S_SYDATE from sample_mx mx, h_clinic_project hp, H_SAMPLE_ITEM item WHERE mx.SUBJECT_NAME=\"%s\" AND mx.id=item.sample_id AND item.item_id=hp.ID and hp.h_chinese_name like \"%%%s%%\" AND mx.`STORAGE_STAGE` LIKE "收样";""" % (self.username,self.project)
        # print("library",sql)
        data = self.db.fetch_one(sql)
        # print("library_data",data)
        if data:
            if data[0]:
                try:
                    return data[0].strftime("%Y-%m-%d"), True
                except Exception as e:
                    return "",False
            else:
                return "", False
        else:
            return "", False

    def report(self):
        # 关于样本是否走到最后report这一步 是否出报告还需要进行最后一步的检查
        # sql= """SELECT s.RP_DATE FROM report_info s,sample_mx mx, h_clinic_project hp, H_SAMPLE_ITEM item WHERE s.RP_SAMPLE_ID=mx.id AND mx.SUBJECT_NAME=\"%s\" AND mx.id=item.sample_id AND item.item_id=hp.ID AND hp.h_chinese_name LIKE \"%%%s%%\" AND s.RP_FILE IS NOT NULL;""" % (self.username,self.project)
        sql = """SELECT r.RP_DATE FROM REPORT_INFO r LEFT JOIN sample_mx bmx ON r.RP_SAMPLE_ID = bmx.id LEFT JOIN H_CLINIC_PROJECT p ON r.CHECK_ITEM_ID = p.ID WHERE bmx.SUBJECT_NAME =\"%s\" AND p.h_chinese_name LIKE \"%%%s%%\" ORDER BY DEAD_TIME ASC""" % (self.username,self.project)
        out1 = self.db.fetch_one(sql)
        # print(sql,out1)
        print("report查询")
        if out1:
            if out1[0]:
                return out1[0].strftime("%Y-%m-%d"), True
            else:
                sql = """select mx.DEAD_TIME from sample_mx mx,h_clinic_project hp,H_SAMPLE_ITEM item  where mx.SUBJECT_NAME=\"%s\" and mx.id=item.sample_id and item.item_id=hp.ID AND hp.h_chinese_name LIKE \"%%%s%%\";""" % (self.username,self.project)
                print("查询dead_line信息", sql)
                data = self.db.fetch_one(sql)
                try:
                    dead_time = "-".join(data[0].split("/"))
                    return dead_time + "(预估)", False
                except Exception as e:
                    for keys,values in self.project_conf.items():
                        if values in self.project:
                            sql = """select mx.DEAD_TIME from sample_mx mx,h_clinic_project hp, H_SAMPLE_ITEM item where mx.SUBJECT_NAME=\"%s\" and mx.id=item.sample_id and item.item_id=hp.ID AND hp.h_chinese_name LIKE \"%%%s%%\";""" % (self.username, values)
                            data = self.db.fetch_one(sql)
                            try:
                                dead_time = "-".join(data[0].split("/"))
                                return dead_time + "(预估)", False
                            except Exception as e:
                                return "", False
        else:
            sql = """select mx.DEAD_TIME from sample_mx mx,h_clinic_project hp,H_SAMPLE_ITEM item  where mx.SUBJECT_NAME=\"%s\" and mx.id=item.sample_id and item.item_id=hp.ID AND hp.h_chinese_name LIKE \"%%%s%%\";""" % (self.username,self.project)
            data = self.db.fetch_one(sql)
            try:
                dead_time = "-".join(data[0].split("/"))
                return dead_time + "(预估)", False
            except Exception as e:
                for keys,values in self.project_conf.items():
                    if values in self.project:
                        sql = """select mx.DEAD_TIME from sample_mx mx,h_clinic_project hp, H_SAMPLE_ITEM item where mx.SUBJECT_NAME=\"%s\" and mx.id=item.sample_id and item.item_id=hp.ID AND hp.h_chinese_name LIKE \"%%%s%%\";""" % (self.username, values)
                        data = self.db.fetch_one(sql)
                        try:
                            dead_time = "-".join(data[0].split("/"))
                            return dead_time + "(预估)", False
                        except Exception as e:
                            return "", False

    def analysis(self):
        sql = """select k.SYS_INSERTTIME from k_infoanalysis_mx k, sample_mx mx, h_clinic_project hp where mx.id=k.SAMPLE_ID and mx.SUBJECT_NAME=\"%s\"and k.CHECK_ITEM_ID=hp.ID AND hp.h_chinese_name LIKE \"%%%s%%\";""" % (self.username,self.project)
        out = self.db.fetch_one(sql)
        print("analysis分析")
        if out:
            try:
                return out[0].strftime("%Y-%m-%d"), True
            except Exception as e:
                return "", True
        else:
            return "", False

    def outmanager(self):
        sql1 = """select k.SYS_INSERTTIME from k_epiboly_manage_mx k, sample_mx mx, h_clinic_project hp where k.SAMPLE_MX_ID=mx.id and mx.SUBJECT_NAME=\"%s\" and k.CHECK_ITEM_ID=hp.ID AND hp.h_chinese_name like \"%%%s%%\";""" % (self.username,self.project)
        out1 = self.db.fetch_one(sql1)
        sql2 = """SELECT rp.SYS_INSERTTIME FROM EXP_RESULT_MX rp,sample_mx mx,h_clinic_project hp WHERE rp.EX_SAMPLE_ID=mx.id AND mx.SUBJECT_NAME=\"%s\" AND rp.EX_JCXM_ID=hp.ID AND hp.h_chinese_name LIKE \"%%%s%%\";""" % (self.username,self.project)
        out2 = self.db.fetch_one(sql2)
        result_out = []
        print("outmanager")
        try:
            if out1[0]:
                result_out.append(out1[0].strftime("%Y-%m-%d"))
        except Exception as e:
            print(e)
        try:
            if out2[0]:
                result_out.append(out2[0].strftime("%Y-%m-%d"))
        except Exception as e:
            print(e)
        try:
            out = max(result_out)
            return out, True
        except Exception as e:
            return "",True

    def datapcr(self):
        sql = """SELECT e.SYS_INSERTTIME FROM expresult_mx e,sample_mx mx, h_clinic_project hp WHERE mx.id=e.SAMPLE_MX_ID and mx.SUBJECT_NAME=\"%s\" and e.CHECK_ITEM_ID=hp.ID AND hp.h_chinese_name like \"%%%s%%\";""" % (self.username,self.project)
        out1 = self.db.fetch_one(sql)
        # rp_numpcr_result 表里面没有时间记录
        sql = """select * from rp_numpcr_result rp,sample_mx mx,h_clinic_project hp where rp.SAMPLE_ID=mx.id and mx.SUBJECT_NAME=\"%s\" and rp.CHECK_ITEM_ID=hp.ID AND hp.h_chinese_name like \"%%%s%%\";""" % (self.username,self.project)
        out2 = self.db.fetch_all(sql)
        print("datapcr")
        if out1:
            try:
                return out1[0].strftime("%Y-%m-%d"), True
            except Exception as e:
                return "", True
        elif out2:
            return "", True
        else:
            return "", False

    def ngs(self):
        #sql = "select * from sample_index where MY_SAMPLE_ID=\"%s\";" % self.id
        sql = """SELECT s.SYS_INSERTTIME FROM sample_index s ,sample_mx mx, h_clinic_project hp WHERE s.MY_SAMPLE_ID=mx.id AND mx.SUBJECT_NAME=\"%s\" and s.CHECK_ITEM_ID=hp.ID AND hp.h_chinese_name like \"%%%s%%\";""" % (self.username,self.project)
        out1 = self.db.fetch_one(sql)
        # 外包管理ngs确认
        sql2 = """SELECT k.SYS_INSERTTIME FROM k_epiboly_return_mx k ,sample_mx mx,h_clinic_project hp WHERE k.SAMPLE_MX_ID=mx.id AND mx.SUBJECT_NAME=\"%s\" and k.CHECK_ITEM_ID=hp.ID AND hp.h_chinese_name like \"%%%s%%\";""" % (self.username,self.project)
        out2 = self.db.fetch_one(sql2)
        out_data = []
        # print("ngs_Data",out1,out2)
        if out1:
            try:
                out_data.append(out1[0].strftime("%Y-%m-%d"))
            except Exception as e:
                print(e)
        if out2:
            try:
                out_data.append(out2[0].strftime("%Y-%m-%d"))
            except Exception as e:
                print(e)
        try:
            return max(out_data),True
        except Exception as e:
            return "",False

    def extractrqc(self):
        #sql = """SELECT s.SYS_INSERTTIME FROM sample_separate_mx s,sample_mx mx, h_clinic_project hp, H_SAMPLE_ITEM item WHERE s.SAMPLE_MX_ID=mx.id AND mx.SUBJECT_NAME=\"%s\" and mx.id=item.sample_id and item.item_id=hp.ID and hp.h_chinese_name like \"%%%s%%\";""" % (self.username,self.project)
        #out1 = self.db.fetch_one(sql)
        #sql2 = """SELECT s.SYS_INSERTTIME FROM k_sample_tq_mx s,sample_mx mx,h_clinic_project hp, H_SAMPLE_ITEM item WHERE s.SAMPLE_ID=mx.id AND mx.SUBJECT_NAME=\"%s\" and mx.id=item.sample_id and item.item_id=hp.ID AND hp.h_chinese_name like \"%%%s%%\";""" % (self.username,self.project)
        #out2 = self.db.fetch_one(sql2)
        sql1 = """SELECT s.sys_inserttime FROM sample_qc s ,sample_mx mx,h_clinic_project hp, H_SAMPLE_ITEM item WHERE s.OLD_SAMPLE_MX_ID=mx.id AND mx.SUBJECT_NAME=\"%s\" and mx.id=item.sample_id and item.item_id=hp.ID AND hp.h_chinese_name like \"%%%s%%\";""" % (self.username,self.project)
        out1 = self.db.fetch_one(sql1)
        sql2 = """SELECT s.k_extracting_date FROM k_sample_tq_pool s,sample_mx mx,h_clinic_project hp, H_SAMPLE_ITEM item WHERE s.K_SAMPLE_ID=mx.id AND mx.SUBJECT_NAME=\"%s\" and mx.id=item.sample_id and item.item_id=hp.ID AND hp.h_chinese_name like \"%%%s%%\";""" % (self.username,self.project)
        out2 = self.db.fetch_one(sql2)
        #sql5 = """SELECT s.SYS_INSERTTIME FROM quacontrol_sample_mx s ,sample_mx mx,h_clinic_project hp WHERE s.QCS_SAMPLE_ID=mx.id AND mx.SUBJECT_NAME=\"%s\" and s.CHECK_ITEM_ID=hp.ID AND hp.h_chinese_name like \"%%%s%%\";""" % (self.username, self.project)
        #out5 = self.db.fetch_one(sql5)
        result_out = []
        try:
            if out1[0]:
                result_out.append(out1[0].strftime("%Y-%m-%d"))
        except Exception as e:
            print(e)
        try:
            if out2[0]:
                result_out.append(out2[0].strftime("%Y-%m-%d"))
        except Exception as e:
            print(e)
        # try:
        #     if out3[0]:
        #         result_out.append(out3[0].strftime("%Y-%m-%d"))
        # except Exception as e:
        #     print(e)
        # try:
        #     if out4[0]:
        #         result_out.append(out4[0].strftime("%Y-%m-%d"))
        # except Exception as e:
        #     print(e)
        # try:
        #     if out5[0]:
        #         result_out.append(out5[0].strftime("%Y-%m-%d"))
        # except Exception as e:
        #     print(e)
        print("外包实验信息",result_out)
        if result_out:
            out = max(result_out)
            return out, True
        # else:
        #     sql = """SELECT k.SYS_INSERTTIME,k.OPERATE_TIME,k.OUT_RETURN_FLAG FROM K_EPIBOLY_MANAGE k LEFT JOIN K_EPIBOLY_MANAGE_MX kmx ON kmx.main_id=k.id LEFT JOIN sample_mx mx ON kmx.SAMPLE_MX_ID=mx.id LEFT JOIN h_clinic_project hp ON hp.id=kmx.CHECK_ITEM_ID WHERE mx.SUBJECT_NAME=\"%s\" AND hp.h_chinese_name LIKE \"%%%s%%\";""" % (self.username,self.project)
        #     out = self.db.fetch_one(sql)
        #     try:
        #         result_out.append(out[0].strftime("%Y-%m-%d"))
        #         return out[0].strftime("%Y-%m-%d"),True
        #     except Exception as e:
        #         pass
        else:
                return "",False

    def pcr(self):
        #sql = "select * from k_lgc_sample_mx where SAMPLE_MX_ID=\"%s\"" % self.id
        sql = """SELECT s.sys_inserttime FROM k_lgc_sample_mx s,sample_mx mx,h_clinic_project hp, H_SAMPLE_ITEM item WHERE s.SAMPLE_MX_ID=mx.id AND mx.SUBJECT_NAME=\"%s\" and mx.id=item.sample_id and item.item_id=hp.ID AND hp.h_chinese_name like \"%%%s%%\";""" % (self.username,self.project)
        out1 = self.db.fetch_one(sql)
        #sql = """select * from k_result_summary k,sample_mx mx, h_clinic_project hp, H_SAMPLE_ITEM item where k.SAMPLE_MX_ID=mx.id and mx.SUBJECT_NAME=\"%s\" and mx.id=item.sample_id and item.item_id=hp.ID AND hp.h_chinese_name like \"%%%s%%\";""" % (self.username,self.project)
        #out2 = self.db.fetch_all(sql)
        out=[]
        try:
            out.append(out1[0].strftime("%Y-%m-%d"))
            return out1[0].strftime("%Y-%m-%d"),True
        except Exception as e:
            pass
        if not out:
            return "",False

    def close(self):
        self.db.commit()

def get_project_info(projectInfo,username):
    get_project_info_result = {}
    for keys, values in projectInfo.items():
        start=time.time()
        # mainId = values["main_id"]
        project = values["project"]
        type = values["type"]
        reportid = values["reportId"]
        get_project_info_result[keys] = []
        for index in range(len(project)):
            queryInfoOut = queryinfo(username,project[index])
            get_project_info_result[keys].append({"project": project[index], "info": queryInfoOut, "type": type[index], "reportId":reportid[index]})
        end=time.time()
        print("查询一次信息耗时",str(end-time))
    return get_project_info_result

def queryinfo(username,project):
    data = Analysis(username,project)
    start1=time.time()
    report_info, report = data.report()
    report_time=time.time()
    print("report耗时",str(report_time-start1))
    analysis_info, analysis = data.analysis()
    analysis_time=time.time()
    print("analysis耗时",str(analysis_time-report_time))
    outmanager_info, outmanager = data.outmanager()
    outmanager_time=time.time()
    print("outmanager耗时",str(outmanager_time-analysis_time))
    datapcr_info, datapcr = data.datapcr()
    datapcr_time=time.time()
    print("datapcr耗时",str(datapcr_time-outmanager_time))
    ngs_info, ngs = data.ngs()
    ngs_time=time.time()
    print("ngs耗时",str(ngs_time-datapcr_time))
    extractrqc_info, extractrqc = data.extractrqc()
    extractrqc_time=time.time()
    print("extractrqc耗时",str(time.time()-ngs_time))
    pcr_info, pcr = data.pcr()
    pcr_time=time.time()
    print("pcr耗时",str(pcr_time-extractrqc_time))
    library_info, library = data.library()
    library_time=time.time()
    print("libaray耗时",str(library_time-pcr_time))
    data.close()
    return_info = {"report": {"ret": report, "time": report_info}, "analysis":{'ret': analysis, "time": analysis_info},
                    "outmanager":{"ret": outmanager, "time": outmanager_info},
                   "datapcr":{"time": datapcr_info, "ret": datapcr}, "ngs": {"time": ngs_info, "ret": ngs},
                    "extractrqc": {"time": extractrqc_info, "ret": extractrqc}, "pcr": {"time": pcr_info,"ret": pcr},
                   "library":{"time": library_info, "ret": library}}
    return return_info

def QUERY(username, useridcard, usertel):
    Queryinfo, ret = queryProject(username,useridcard,usertel)
    out = get_project_info(projectInfo=Queryinfo,username=username)
    return out, ret

if __name__ =="__main__":
    username = "苏伟华"
    useridcard = 123456789123456789
    usertel = 124
    project = "普晟惠（Personal-Benefit）-靶向药物伴随检测"
    import time
    print(time.time())
    a,b=QUERY(username,useridcard,usertel)
    print(time.time())
    print(a)
    print(b)
    # d = Analysis(username, project)
    # a=d.extractrqc()
    # print(a)
    # aaa=d.report()
    # print(aaa)
    # xx=queryProject(username, useridcard, usertel)
    # print(xx)
    # a,b=QUERY(username,useridcard,usertel)
    # print("查询信息的结果如下")
    # print(a)
    # print(b)
