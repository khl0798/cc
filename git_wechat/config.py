#-*- coding: utf-8 -*-

import configparser, os

class Config(object):
    def __init__(self, table_name):
        self.CONF_FILE = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "main.conf"))
        self.rcf = configparser.RawConfigParser()
        self.rcf.read(self.CONF_FILE)
        self.db_name = self.rcf.get(table_name, "table")
        self.port = self.rcf.get(table_name, "port")
        self.host = self.rcf.get(table_name, "ip")
        self.user = self.rcf.get(table_name, "account")
        self.password = self.rcf.get(table_name, "password")

def cc_download_path(type="test"):
    """下载文件路径"""
    if type == "dev":
        path = "/home/khl/web/cc_dist_test/downloads/tmp"
    if type == "test":
        path = "/home/khl/web/dist/downloads/tmp"
    return path

def cc_path(type="test"):
    if type == "test":
        path = "/home/khl/web/dist/"
    if type == "dev":
        path = "/home/khl/web/cc_dist_test/"
    return path

def cc_url(type="test"):
    """生成报告下载"""
    if type == "test":
        url = "http://116.228.83.74:8090"
    if type == "dev":
        url = "http://192.168.1.144:8091/"
    return url

def cc_word_url(type="test"):
    """word模板下载"""
    if type=="test":
        url = "http://192.168.1.144:8094"
    if type=="dev":
        url = "http://192.168.1.144:9094/"
    return url

def cc_upload_path(type="test"):
    if type=="test":
        path = "/home/khl/web/dist/upload"
    if type == "dev":
        path="/home/khl/web/cc_dist_test/upload"
    # 大文件fastq分片上传
    if type == "15gene":
        path = "/home/khl/dna_data/15gene"
    if type == "12gene":
        path = "/home/khl/dna_data/12gene"
    return path

def cc_upload_url(type="test"):
    if type == "test":
        url = "http://116.228.83.74:8090"
    if type == "dev":
        url = "http://192.168.1.144:8091/"
    return url

def cc_word_template():
    """word模板路径"""
    path = '/home/khl/web/word'
    return path

def cc_pipeline_out_path():
    """cc端 pipeline工作流生成结果文件的路径"""
    path = "/data/pipeline"
    return path

if __name__ == "__main__":
     # conf = Config(table_name="PC_SAMPLE")
     # print(conf.db_name, conf.port, conf.host, conf.user, conf.password)
     aa=cc_download_path(type="dev")
     print('aa',aa)