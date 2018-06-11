# -*-coding: utf-8-*-

import falcon, json
from wsgiref import simple_server
import pymysql
from login_api import *
from config import *
import gunicorn
from query_project import *
from docx import Document
from docx.shared import Inches
from project_conf import *
import datetime
from datetime import *
global project_name
import base64
import re

project_name = project_conf()
project_name_dict = new_wechat_project()

def query_sample_filter(sample_code, project=None):
    """['1', '1', '79岁', '88岁', '65岁', '68岁', '1', '1', '79岁', '88岁', '65岁', '68岁', '无', '无', '无', '无', '无', '无', '无', '无', '无', '无', '无', '68岁', '68岁', '69岁', '69岁', '61岁', '61岁', '61岁', '61岁', '68岁', '68岁', '68岁', '85岁', '85岁', '85岁', '85岁', '85岁', '85岁', '69岁', '61岁', '69岁', '61岁', '69岁', '61岁', '69岁', '61岁', '52岁', '52岁', '52岁', '61岁', '52岁', '52岁', '52岁', '无', '无']
    """
    db = Mysql(table_name="GLORIA_MYSQL")
    sql = "select * from sample_mx where S_CODE=\"%s\" and STORAGE_STAGE=\"%s\";" % (sample_code,"收样")
    out_data = db.fetch_all(sql)  # 一个样本可能做多个项目
    print(len(out_data))
    out_data_list = []

    def get_info(input_info):
        try:
            if input_info:
                return input_info
            else:
                return ""
        except Exception:
            return ""
    if out_data:
        project_id = []
        for temp in out_data:
            sql = "select * from h_sample_item where SAMPLE_ID=\"%s\" ;" % temp[0]
            sampleIdInfo = db.fetch_one(sql)
            sql = 'select * from h_clinic_project where ID=\"%s\"' % sampleIdInfo[6]
            sampleProjectInfo = db.fetch_one(sql)

            for keys, values in project_name_dict.items():
                if sampleProjectInfo[1] not in project_id:
                    # if values in project and values in sampleProjectInfo[1]:
                    if values in project:
                        print("客户做的样本检测项目是:", sampleProjectInfo[1])
                        project_id.append(sampleProjectInfo[1])
                        out_data_list.append(temp)
                    else:
                        pass
        if len(out_data_list) == 1:
                data = out_data_list[0]
                sample_name = data[2]  # 样本名称
                patient_name = data[59]  # 患者姓名
                print("病人的名字是",patient_name)
                patient_tel = data[8]  # 电话号码
                patient_email = data[9]  # 邮箱
                sample_type = data[15]  # 样本类型
                patient_address = data[39]  # 居住地址
                patient_sex = data[40]  # 性别
                patient_treatment = data[62]  # 治疗史

                # 样本接受日期
                try:
                    receive_time1 = data[43].strftime('%x').split("/")
                    receive_year = "20%s" % receive_time1[2]
                    receive_month = receive_time1[0]
                    receive_day = receive_time1[1]
                    receive_time = "%s-%s-%s" % (receive_year, receive_month, receive_day)
                except Exception:
                    receive_time = "/"

                patient_useridcard = data[52]  # 身份证号码
                patient_age = data[63]   # 病人年龄
                if not patient_age:
                    patient_age = "/"

                patient_clinical = data[56]  # 临床信息
                hospital = data[61]  # 送检医院
                # 样本采样日期
                try:
                    sample_time1 = data[5].strftime('%x').split("/")
                    sample_year = "20%s" % sample_time1[2]
                    sample_month = sample_time1[0]
                    sample_day = sample_time1[1]
                    sample_time = "%s-%s-%s" % (sample_year, sample_month, sample_day)
                except Exception:
                    sample_time = "/"

                # sample_time = data[5]   #样本采样时间
                # try:
                #     total_sample = data[-6]+data[-5]  # 样本总量
                # except Exception:
                #     total_sample = ""
                sql = """SELECT * FROM sample_qc qc,sample_mx mx WHERE qc.old_sample_mx_id=mx.id AND mx.S_MCODE=\"%s\";""" % sample_code
                if db.fetch_one(sql):
                    total_sample = str('%.2f' % db.fetch_one(sql)[14])
                else:
                    total_sample = "/"
                print("total_sample数据结果", total_sample)
                sample_type = data[15]  # 组织类型

                sql = "select * from h_sample_item where SAMPLE_ID=\"%s\"" % data[0]
                h_sample_id = db.fetch_one(sql)[6]
                sql = 'select * from h_clinic_project where ID=\"%s\"' % h_sample_id
                project_id = db.fetch_one(sql)[1]
                data = db.fetch_one(sql)
                time_tmp = date.today()
                time_tmp1 = [str(i) for i in time_tmp.timetuple()[0:3]]
                time = "%s-%s-%s" % (time_tmp1[0], time_tmp1[1], time_tmp1[2])

                result = {"ClientName": patient_name, "ReportNo": sample_code, "SampleHospital": hospital,
                          "ReportDate": time,  "ClientSex": patient_sex,
                          "ClientID": patient_useridcard, "ClientAge": patient_age, "ClientPhone": patient_tel,
                          "ClientInfo": patient_clinical, "ClientHistory": patient_treatment,
                          "SampleNo": sample_code, "SampleType": sample_type, "SampleTime": sample_time,
                          "SampleDNA": total_sample, "DateRecieved": receive_time}
                return result
        else:
            return None

def get_tumor_infiltrating(tumorInfiltrating, pd28Tumor,pd28Lymph,pd142Tumor,pd142Lymph,cd8, tumorPercent, tumorLevel):
    pdl128 = "肿瘤细胞%s,间质淋巴细胞%s"  % (pd28Tumor, pd28Lymph)
    pdl1142 = "肿瘤细胞%s,间质淋巴细胞%s" % (pd142Tumor, pd142Lymph)
    cd8 = "淋巴细胞%s" % cd8
    tmp_reportsummary = "肿瘤成分占比%s,淋巴细胞浸润%s;肿瘤细胞中PD-L1 表达%s。以此判断对免疫治疗响应的可能性"
    if "阳性" in pd28Tumor or "阳性" in pd28Lymph or "阳性" in pd142Tumor or "阳性" in pd142Lymph:
        pdl1Express="阳性"
    else:
        pdl1Express="阴性"
    # with open(atlas,'rb') as f1:
    #     figure = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
    if re.search(r'(\d+)', str(tumorPercent)):
        reportsummary = tmp_reportsummary % (str(tumorPercent)+"%", tumorInfiltrating, pdl1Express)
    else:
        reportsummary = tmp_reportsummary % (str(tumorPercent), tumorInfiltrating, pdl1Express)
    # ReportSummary
    print('reportsummary',reportsummary)
    information = {"TumorInfiltrating": tumorInfiltrating, "CD8":cd8, "TumorLevel":tumorLevel,
                   "PDL128":pdl128 , "PDL1142":pdl1142, "ReportSummary": reportsummary}
    return information

def get_msi_info(NR21,NR24,NR27,BAT25,BAT26,MONO27,PentaC,PentaD,reportStable):
    information = {"NR21":NR21, "NR24":NR24, "NR27":NR27, "BAT25":BAT25,
                   "BAT26":BAT26, "MONO27":MONO27, "PentaC":PentaC, "PentaD":PentaD,
                   "reportStable":reportStable}
    return information

# def get_msi_fiter(msiStable, reportStable):

if __name__ == "__main__":
    # sample_code = "YHB1720537"
    # data = query_sample_filter(sample_code, project="普晟朗（Personal-Lung）-肺癌靶向用药15基因检测-组织版")
    # sample_code = "YHB1720517"
    # data = query_sample_filter(sample_code, project="普晟和-肿瘤靶向化疗用药83基因检测")
    # sample_code = "YHF1810005"
    # project_name = "普晟惠-MSI微卫星不稳定性检测"
    sample_code= "YHB6660189"
    project_name = "普晟朗 - 肺癌靶向用药15基因检测"
    data = query_sample_filter(sample_code, project_name)
    print(data)
    # sample_code = "YHB1720312"
    # data = query_sample_filter(sample_code, project="普晟畅（Personal-CRC）-结直肠癌靶向用药12基因检测-组织版")
    # print(data)
    # db = Mysql(table_name="GLORIA_MYSQL")
    # sql = "select SUBJECT_SFZ from sample_mx;"
    # data = db.fetch_all(sql)
    # print(data)
    # info = []
    # import re
    # for i in data:
    #     if len(i[0]) == 18 or i[0] == '/':
    #         continue
    #     else:
    #         info.append(i[0])
    # print(info)
    # 该客户的project名字和数据库列表对应不起来
    # db = Mysql(table_name="GLORIA_MYSQL")
    # sql = "select h_chinese_name from h_clinic_project"
    # data = db.fetch_all(sql)
    # info = []
    # with open("D:/cc/lims_project.txt",'w') as f1:
    #     for d in data:
    #         if d[0] not in info:
    #             f1.write(d[0]+"\n")
    #             info.append(d[0])

