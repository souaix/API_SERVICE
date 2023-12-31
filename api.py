#!/usr/bin/env python
# coding: utf-8
from flask import Flask, jsonify, request

from gevent import monkey
monkey.patch_all()

from gevent.pywsgi import WSGIServer
from multiprocessing import cpu_count, Process
from bottle import Bottle

import json
import sys
import os
from ftplib import FTP
import datetime
import pandas as pd
#app = Bottle()

sys.path.append('/home/cim')
# connector
import connect.connect as cc

eng_mes = cc.connect('MES', 'MES_Production')
eng_cim = cc.connect('CIM_ubuntu', 'mapcheck')

def downloadfile(ftp, remotepath, localpath):
    bufsize = 1024  # 设置缓冲块大小
    fp = open(localpath, 'wb')  # 以写模式在本地打开文件
    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)  # 接收服务器上文件并写入本地文件
    ftp.set_debuglevel(0)  # 关闭调试
    fp.close()  # 关闭文件
    ftp.quit()

def create_date_trans(create_date):    
    create_date = create_date.replace("__"," ")
    if "/" in create_date and ":" in create_date:
        create_date = "20"+create_date
    else:
        create_date="_"
    return create_date

        
app = Flask(__name__)

@app.route('/die_count/', methods=['POST'],strict_slashes=False)

def die_count():
    try:
        parm = request.get_json()[0]
        sublot = parm['sublot']
        barcode = parm['barcode']
        mo = sublot[0:12]
        mo_body = mo[4:12]+".CSV"
        path_body = "Count_CSV/"+mo[4:12]+".CSV"

    except:
        result = [{'Message':'Wrong Parameter','Qty':'None'}]
        return jsonify(result)

    yy = str(datetime.datetime.now().year)
    try:

        ip_ = '10.21.225.91'
        pp = os.popen("ping -c 2 -w 1 "  + ip_ )
        msg = pp.read()
        if '0 received' not in msg:

            ftp = FTP('10.21.225.91', 'ghost', '123456')
            ftp.cwd('WAFERTRAN6B')

            if (mo_body in ftp.nlst()) == True:
                downloadfile(ftp, "/WAFERTRAN6B/"+mo_body, path_body)
                df_6B = pd.read_csv(path_body)
                df_6B = df_6B[["Data create","Op id","Mo #","Frame barcode", "Qty"]]
                df_6B.replace('\s', '', regex=True, inplace=True)
            else:
                ftp.cwd(yy)
                if (mo_body in ftp.nlst()) == True:
                    downloadfile(ftp, "/WAFERTRAN6B/"+yy+"/"+mo_body, path_body)
                    df_6B = pd.read_csv(path_body)
                    df_6B = df_6B[["Data create","Op id","Mo #","Frame barcode", "Qty"]]
                    df_6B.replace('\s', '', regex=True, inplace=True)
                else:
                    df_6B = pd.DataFrame(columns=["Data create","Op id","Mo #","Frame barcode", "Qty"])
            print(ip_+" OK!")
        else :
            print(ip_ + ' connect failed')
            df_6B = pd.DataFrame(columns=["Data create","Op id","Mo #","Frame barcode", "Qty"])
    except:
        print("10.21.225.91 connect failed")
        df_6B = pd.DataFrame(columns=["Data create","Op id","Mo #","Frame barcode", "Qty"])
    ###

    try:

        ip_ = '10.21.225.92'
        pp = os.popen("ping -c 2 -w 1 "  + ip_ )
        msg = pp.read()
        if '0 received' not in msg:


            ftp = FTP('10.21.225.92', 'ghost', '123456')
            ftp.cwd('WAFERTRAN8A')

            if (mo_body in ftp.nlst()) == True:
                downloadfile(ftp, "/WAFERTRAN8A/"+mo_body, path_body)
                df_8A = pd.read_csv(path_body)
                df_8A = df_8A[["Data create","Op id","Mo #","Frame barcode", "Qty"]]
                df_8A.replace('\s', '', regex=True, inplace=True)
            else:
                ftp.cwd(yy)
                if (mo_body in ftp.nlst()) == True:
                    downloadfile(ftp, "/WAFERTRAN8A/"+yy+"/"+mo_body, path_body)
                    df_8A = pd.read_csv(path_body)
                    df_8A = df_8A[["Data create","Op id","Mo #","Frame barcode", "Qty"]]
                    df_8A.replace('\s', '', regex=True, inplace=True)
                else:
                    df_8A = pd.DataFrame(columns=["Data create","Op id","Mo #","Frame barcode", "Qty"])
            print(ip_+" OK!")
        else :
            print(ip_ + ' connect failed')    
            df_8A = pd.DataFrame(columns=["Data create","Op id","Mo #","Frame barcode", "Qty"])                
    except:
        print("10.21.225.92 connect failed")
        df_8A = pd.DataFrame(columns=["Data create","Op id","Mo #","Frame barcode", "Qty"])
    ###

    try:

        ip_ = '10.21.225.94'
        pp = os.popen("ping -c 2 -w 1 "  + ip_ )
        msg = pp.read()
        if '0 received' not in msg:

            ftp = FTP('10.21.225.94', 'ghost', '123456')
            ftp.cwd('WAFERTRAN8B')

            if (mo_body in ftp.nlst()) == True:
                downloadfile(ftp, "/WAFERTRAN8B/"+mo_body, path_body)
                df_8B = pd.read_csv(path_body)
                df_8B = df_8B[["Data create","Op id","Mo #","Frame barcode", "Qty"]]
                df_8B.replace('\s', '', regex=True, inplace=True)
            else:
                ftp.cwd(yy)
                if (mo_body in ftp.nlst()) == True:
                    downloadfile(ftp, "/WAFERTRAN8B/"+yy+"/"+mo_body, path_body)
                    df_8B = pd.read_csv(path_body)
                    df_8B = df_8B[["Data create","Op id","Mo #","Frame barcode", "Qty"]]
                    df_8B.replace('\s', '', regex=True, inplace=True)
                else:
                    df_8B = pd.DataFrame(columns=["Data create","Op id","Mo #","Frame barcode", "Qty"])
            print(ip_+" OK!")                    
        else :
            print(ip_ + ' connect failed')                    
            df_8B = pd.DataFrame(columns=["Data create","Op id","Mo #","Frame barcode", "Qty"])

    except:
        print("10.21.225.94 connect failed")            
        df_8B = pd.DataFrame(columns=["Data create","Op id","Mo #","Frame barcode", "Qty"])


    df_count = pd.concat([df_6B, df_8A, df_8B])        



#     #將data create改為日期格式
    df_count["Data create"] = df_count["Data create"].fillna("")
    df_count["Data create"] = df_count["Data create"].map(create_date_trans)
    df_count = df_count[df_count["Data create"]!='_']
    df_count['Data create'] = pd.to_datetime(df_count['Data create'])
    df_count = df_count.sort_values(by=['Data create'], ascending=False)
    df_count = df_count.drop_duplicates(subset=['Frame barcode'], keep='first')        

    df_count[df_count['Frame barcode']==barcode]
    df_count=df_count[df_count["Frame barcode"]!='']
    df_count = df_count.rename(columns={"Data create":"CREATETIME","Op id":"OP_ID","Mo #":"MO","Frame barcode":"BARCODE"})
    df_count=df_count[df_count["BARCODE"]==barcode]        

    
    if len(df_count)>0:
        # sql = "DELETE FROM TH_DIECOUNT WHERE BARCODE ='"+barcode+"'"
        # con.execute(sql)
        # df_count["LOTNO"] = sublot
        # df_count.to_sql('TH_DIECOUNT',con=con,if_exists='append',index=False)
        df_count.reset_index(inplace=True,drop=True)
        qty = df_count["Qty"][0]
        try:
          qty = int(qty)        
          qty = str(qty)        
        except:
          qty = str(qty)          
            
        result = [{'Message':'Success','Qty':qty}]
        return jsonify(result)

        try:
            os.remove(sublot+".CSV")
        except:
            print("del failed")        

        print("REPLACE OK!")

    else:        
        result = [{'Message':'Not found data','Qty':'None'}]
        return jsonify(result)
    
        try:
            os.remove(sublot+".CSV")
        except:
            print("del failed")


server_dc = WSGIServer(('10.21.98.21',9990),app,log=None)
server_dc.start()

@app.route('/mapcheck/', methods=['POST'],strict_slashes=False)

def mapcheck():

    mo = request.get_json()[0]['mo']

    sql ='''
        select BASELOTNO,BARCODE,FILE_TYPE,AVIMAP_FILENAME from
        (SELECT PRODUCTNO,BASELOTNO FROM TBLWIPLOTBASIS WHERE MONO =\''''+mo+'''\') as WIPBS
        INNER JOIN
        (select * from TBLPRDOP where opno ='S093_RW') as PRDOP
        ON WIPBS.PRODUCTNO=PRDOP.PRODUCTNO
        INNER JOIN
        (select * from TBLPRDOPATTRIB where ATTRIBNO ='EXEFORXML' and ATTRIBVALUE='Y') as ATTR
        on PRDOP.serialno = ATTR.SERIALNO
        INNER JOIN
        (select * from TBLPRDOPATTRIB where attribno = 'EQP_AUTOPROGRAM_CO' AND ATTRIBVALUE ='PROG00012') AS ATTCO
        ON PRDOP.SERIALNO=ATTCO.SERIALNO    
        LEFT JOIN
        (select * from OPENQUERY(ERP,'select * from MES.VIEW_AVIMAP_FILE WHERE MO_NO =\'\''''+mo+'''''\') ) AS avimap
        ON WIPBS.BASELOTNO COLLATE Chinese_Taiwan_Stroke_CI_AS = avimap.LOTNO
        '''

    df_PROG00012 = pd.read_sql(sql,eng_mes)
    df_PROG00012.to_sql('PROG0012', con=eng_cim, if_exists='replace', index=False)
    result = [{'Message':'OK','Qty':'None'}]
    return jsonify(result)

server_mc = WSGIServer(('10.21.98.21',9991),app,log=None)
server_mc.start()


def server_forever():
	server_dc.start_accepting()
	server_dc.start_accepting()
	server_mc._stop_event.wait()
	server_mc._stop_event.wait()


if __name__ == '__main__':

	print('----')
	for i in range(cpu_count()):
		p = Process(target=server_forever)
		p.start()

	
