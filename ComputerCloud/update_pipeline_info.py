# -*-coding: utf-8-*-

import os
import time
from collections import deque as dq
from random import Random
import threading
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-id', '--id', required=True, help="插入数据库的id信息")
    parser.add_argument('-path', '--out_path', required=False, help="生成文件的路径")
    args = parser.parse_args()
    id = os.path.abspath(args.id)
    out_path = os.path.abspath(args.out_path)
    return id, out_path

def update_function(id,out_path):
    info = False
    try:
        vcf_path = os.path.join(out_path,"3.variant_calling/total.mutect.vcf.xls")
        while True:
            try:
                if os.path.getsize(vcf_path) > 0:
                    sample_mysql = Mysql(table_name="PC_SAMPLE")
                    sql = """update pipelineWorkflow set status=\"%s\" where ID=\"%s\";""" % ("done", id)
                    sample_mysql.execute(sql)
                    sample_mysql.commit()
                    info=True
                else:
                    continue
            except Exception as e:
                print(e)
    except  Exception:
        pass
    return info

def main():
    id, out_path = parse_args()
    info = update_function(id, out_path)

class deque(dq):
    sign = set()
    def append(self,*args,**kwargs):
        dq.append(self,*args,**kwargs)
        self.sign_set()
    def appendleft(self,*args,**kwargs):
        dq.appendleft(self,*args,**kwargs)
        self.sign_set()
    def extend(self,*args,**kwargs):
        dq.extend(self,*args,**kwargs)
    def extendleft(self,*args,**kwargs):
        dq.extendleft(self,*args,**kwargs)
    def sing_set(self):
        for s in self.sign:
            s.set()
    def add_sign(self,s):
        self.sign.add(s)

class Example():
    def __init__(self):
        self.r = Random(time.time())
    def work_run(self,name,q):
        sign = threading.Event()
        q.add_sign(sign)
        while True:
            if q:
                print("%s pop number: %s, %s numbers left" % (name, q.pop(), len(q)))
            else:
                sign.wait()
                sign.clear()
    def manager_run(self,worker_num):
        queue_list = [deque() for i in range(worker_num)]
        work_list = [threading.Thread(target=self.worker_run,args=["Threading-%s" % i,queue_list[i]])
                     for i in range(worker_num)]
        for worker in worker_list:
            work.start()
        while True:
            i = 0
            while i < self.r.randint(0,20):
                queue_list[self.r.randint(0, worker_num - 1)].appendleft(
                    self.r.randint(1, 100)
                )
                i += 1
            time.sleep(self.r.random())

def man(event):
    if not event.is_set() :
        print("Hello Lancy, nice to meet you.")
        event.wait()
        print("How about to watch a movie together?")
    else:
        event.clear()

def woman(event):
    if not event.is_set() :
        print("Hello Mike, today is a nice day!")
        event.wait()
        print("Let's go!")
    else:
        event.clear()

if __name__ == "__main__":
    # main()
    man_talk_event = threading.Event()
    woman_talk_event = threading.Event()
    t1=threading.Thread(target=man,args=(man_talk_event,),name="man")
    t2=threading.Thread(target=woman,args=(woman_talk_event,),name="woman")
    t1.start()
    time.sleep(1)
    t2.start()
    time.sleep(1)





