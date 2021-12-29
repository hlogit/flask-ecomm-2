# pip install Flask
# c:\pypy2.7-v7.0.0-win32\bin\pip.exe install suds requests pyVmomi pyodbc flask werkzeug pyinstaller
import sys
import os
import time
from flask import Flask 
from flask import request
from flask import send_file
from flask import flash, redirect, url_for
from flask import session
import io
import flask
#from subprocess32 import check_output, check_call, Popen, PIPE
import shlex
#import subprocess32
from werkzeug.utils import secure_filename
import logging
import traceback

app = Flask(__name__)
_os = "Neil's door"
logging.basicConfig(filename='0door.log', level=logging.DEBUG)


from flask import Flask, request, render_template, jsonify
import requests
from urllib import parse
import hashlib
import pprint
import collections
import urllib
import urllib.parse
import datetime, sys

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

#currentDT = datetime.datetime.now()
#dt=currentDT.strftime("%Y%m%d%H%M%S")
#MerchantTradeNo ="ecPay"+dt
#print(MerchantTradeNo)
this_server_ip= "34.220.128.74"
this_server_port= "55555"
PaymentInfoURL= "http://%s:%s/getData1"%(this_server_ip,this_server_port)
ReturnURL= "http://%s:%s/getData1"%(this_server_ip,this_server_port)
print(PaymentInfoURL)
print(ReturnURL)
    
form_html="<form action=\"https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5\" method=\"post\">\n"


def to_pay2(TotalAmount):
    #正式環境：https://payment.ecpay.com.tw/Cashier/QueryTradeInfo/V5
    #測試環境：https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5
    url_real = "https://payment.ecpay.com.tw/Cashier/QueryTradeInfo/V5"   # v5
    url = "https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5"   # v5
    form_html0 =""
    form_html0="<form   target=\"_blank\" action=\"%s\" method=\"POST\">\n"%(url)

    print( "==into_pay==")
    currentDT = datetime.datetime.now()
    dt=currentDT.strftime("%Y%m%d%H%M%S")
    MerchantTradeNo ="ecPay"+dt
    print(MerchantTradeNo)
    #sys.exhttps://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5  <base href="https://payment-stage.ecpay.com.tw/">
    #stt ='HashIV=5294y06JbISpM5x9&ChoosePayment=Credit&EncryptType=1&ItemName= nnntesst7&MerchantID=2000132&MerchantTradeDate=2021/10/20 01:03:18&MerchantTradeNo=ecPay1234&PaymentType=aio&ReturnURL=http://your.web.site/receive.php&TotalAmount=97&TradeDesc=nnnpay&HashIV=v77hoKGq4kWxNNIS'
    #stt = stt.encode('utf-8')
    #CheckMacValue = hashlib.sha256(stt).hexdigest()
    header = {"content-type": "application/x-www-form-urlencoded;charset=utf-8"}
    #'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
    FormData = {"ChoosePayment": 'Credit',
    "EncryptType": 1,
    "MerchantTradeDate": '2021/10/20 04:35:18',
    "PaymentType": 'aio',
    "ItemName": 'nnntesst6a#nnntesst2#nnntesst3',
    "MerchantTradeNo": MerchantTradeNo,
    "PaymentInfoURL":PaymentInfoURL,
    "ReturnURL": ReturnURL, 
    "TotalAmount": TotalAmount,
    "TradeDesc": 'nnnpay', 
    "MerchantID": '2000132',
    }
    #"CheckMacValue": CheckMacValue,
    # 字典转换k1=v1 & k2=v2 模式   content
    print( "====")
    od = collections.OrderedDict(sorted(FormData.items()))
    data = parse.urlencode(FormData)
    #print( "==od==")
    o_sorted_vars = ""
    for key in sorted(FormData):
        #print( "==sorted od==")
        vars = "%s=%s&" %(key,FormData[key])
        print ("%s=%s" %(key,FormData[key]))
        o_sorted_vars += vars
    #pprint.pprint( od)
    print(FormData)

    new_vars = "HashKey=%s%sHashIV=%s" % ("5294y06JbISpM5x9&",o_sorted_vars, "v77hoKGq4kWxNNIS")
    vars_str_urlencode = urllib.parse.quote_plus(new_vars)
    vars_str_urlencode_lower = vars_str_urlencode.lower()
    CheckMacValue = (hashlib.sha256(vars_str_urlencode_lower.encode('utf-8')).hexdigest())

    FormData.update({'CheckMacValue': CheckMacValue.upper()})
    for key in sorted(FormData):
        v = FormData[key]
        form_html0+="   <input type=\"hidden\" name=\"%s\" value=\"%s\">\n" %(key,v)
    form_html0+="   <input type=\"text\"  value=\"%s\"  readonly>\n" %(TotalAmount)
    form_html0+="   <input type=\"submit\" value=\"Submit\">\n</form>"
    print(form_html0)
        
    return form_html0

def to_pay(TotalAmount):
    print( "==into_pay==")
    currentDT = datetime.datetime.now()
    dt=currentDT.strftime("%Y%m%d%H%M%S")
    MerchantTradeNo ="ecPay"+dt
    print(MerchantTradeNo)
    #sys.exhttps://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5  <base href="https://payment-stage.ecpay.com.tw/">
    url = "https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5"   # v5
    #stt ='HashIV=5294y06JbISpM5x9&ChoosePayment=Credit&EncryptType=1&ItemName= nnntesst&MerchantID=2000132&MerchantTradeDate=2021/10/20 01:03:18&MerchantTradeNo=ecPay1234&PaymentType=aio&ReturnURL=http://your.web.site/receive.php&TotalAmount=97&TradeDesc=nnnpay&HashIV=v77hoKGq4kWxNNIS'
    #stt = stt.encode('utf-8')
    #CheckMacValue = hashlib.sha256(stt).hexdigest()
    header = {"content-type": "application/x-www-form-urlencoded;charset=utf-8"}
    #'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
    FormData = {"ChoosePayment": 'Credit',
    "EncryptType": 1,
    "MerchantTradeDate": '2021/10/20 04:35:18',
    "PaymentType": 'aio',
    "ItemName": 'nnntesst1#nnntesst2#nnntesst3',
    "MerchantTradeNo": MerchantTradeNo,
    "PaymentInfoURL":PaymentInfoURL,
    "ReturnURL": ReturnURL, 
    "TotalAmount": TotalAmount,
    "TradeDesc": 'nnnpay', 
    "MerchantID": '2000132',
    }
    #"CheckMacValue": CheckMacValue,
    # 字典转换k1=v1 & k2=v2 模式   content
    print( "====")
    od = collections.OrderedDict(sorted(FormData.items()))
    data = parse.urlencode(FormData)
    #print( "==od==")
    o_sorted_vars = ""
    for key in sorted(FormData):
        #print( "==sorted od==")
        vars = "%s=%s&" %(key,FormData[key])
        print ("%s=%s" %(key,FormData[key]))
        o_sorted_vars += vars
    #pprint.pprint( od)
    for key,v in sorted(FormData):
        form_html0+= "<input type=\"text\" name=\"%s\" value=\"%s\">" %( key,v)
    print(form_html0)
    print( "==o_sorted_vars==")
    #print(o_sorted_vars)
    new_vars = "HashKey=%s%sHashIV=%s" % ("5294y06JbISpM5x9&",o_sorted_vars, "v77hoKGq4kWxNNIS")
    #newod = new_vars.encode('utf-8')
    #print( "==new_vars==")
    #print(new_vars)
    #vars_urlencode = urllib.urlencode(new_vars)
    vars_str_urlencode = urllib.parse.quote_plus(new_vars)
    #vars_str_urlencode = urllib.parse.urlencode(new_vars)
    #vars_str_urlencode = parse.urlencode(new_vars)
    vars_str_urlencode_lower = vars_str_urlencode.lower()
    #print( "==vars_str_urlencode_lower==")
    #print(vars_str_urlencode_lower)
    CheckMacValue = (hashlib.sha256(vars_str_urlencode_lower.encode('utf-8')).hexdigest())
    #print( "==CheckMacValue==")
    #print(CheckMacValue)
    CheckMacValue = (hashlib.sha256(new_vars.encode('utf-8')).hexdigest())
    #CheckMacValue = (hashlib.sha256(new_vars.encode('utf-8')).hexdigest())
    FormData.update({'CheckMacValue':CheckMacValue[:-3]})
    FormData2  = FormData.update({'CheckMacValue': CheckMacValue.upper()})
    #FormData2 = FormData['CheckMacValue'] = CheckMacValue
    #print( "==CheckMacValue==")
    #print( CheckMacValue)
    #print( "====")
    pprint.pprint( FormData)
    #print( "====")
    #pprint.pprint( FormData2)
    #print( "====")
    #print( data)
    #print( "====")
    data = parse.urlencode(FormData)
    response= requests.post(url,  headers=header, data=data, verify=False).text
    print( FormData)
    print( "=======response from requests.post==")
    print( response)
    with open(r'./u2.html', 'w', encoding='UTF-8') as f:
        f.write(response)
    return(response)


def add_base(response):
	currentDT = datetime.datetime.now()
	dt=currentDT.strftime("%Y%m%d%H%M%S")
	inf =r"./u3.html" %()
	inf4 =r"./u4.html" %()
	bb1 = "\t<base href=\"https://payment-stage.ecpay.com.tw\">\n\t<!-- SiteMap -->\n\">"
	with open(inf, 'w', encoding='UTF-8') as f:
		f.write(response)
	with open(inf, 'r', encoding='UTF-8') as f:
		fls = f.readlines()
	with open(inf4, 'w', encoding='UTF-8') as nf:
		for L in fls:
			if "<!-- SiteMap -->" in L:
				L = bb1
			nf.write(L)
			
	with open(inf4, 'r', encoding='UTF-8') as nf:
		text = nf.read()
	#print("==add_base(response==")
	#from bs4 import BeautifulSoup
	#soup = BeautifulSoup(response, 'html.parser')
    
	#print( "======soup.head bf==")
	#print(soup.head)
	#bb1 = "<base href=\"https://payment-stage.ecpay.com.tw/\">"
	#soup.head.insert(1,bb1)
	#print( "======soup.head aft==")
	#print(soup.head)
	#print(soup.getText())
	#type(response)
	#print( "==================soup.head aft==")
	#bb = '<base href="https://payment-stage.ecpay.com.tw/">\n<!-- SiteMap -->\n'
	#print( "==soup==")
	#print(type(soup))
	#print( "==response==")
	#print( text[:200])
	###input('===========1')
	#response.replace("<head>\n\n", bb1, 1)
	#response.replace("<!-- SiteMap -->", bb1, 1)
	#print( "==response2==")
	#print( text[:200])
	###input('===========2')
	return text
    
@app.route("/getData1", methods=['POST', 'GET'])
def getInfo():
	print( "==getInfo==")
	print(request.__dict__)
	text_input = request.__dict__
	with open('data.txt', 'a') as data_file:
		data_file.write(text_input)
	#textInput = request.form["data"]
	#print(textInput)
	#return render_template("text.html",text=textInput)
	print( "==getInfo==")
	return jsonify({'message': 'Data saved sucessfully!'}), 200
	
@app.route("/getData2", methods=['POST', 'GET'])
def getInfo2():
    print( "==getInfo2==")
    #if request.method == 'POST':
    text_input = request.form["data"]
    with open('data.txt', 'a') as data_file:
            data_file.write(text_input)
    return jsonify({'message': 'Data saved sucessfully!'}), 200
    print( "==getInfo2==")
    return 0

@app.route('/eee', methods=['POST', 'GET'])
def testform():
    html="""
    <html">\n <head></head>
    <body> <h1>漂亮官網</h1>
    <a href="http://127.0.0.1:55555/rrr">產品紹網頁</a>
    </head>
    </head>
    """
    return html 

@app.route('/rrr', methods=['POST', 'GET'])
def testform2():
    html="""
    <html">\n <head></head>
    <body> <h1>漂亮產品紹網頁</h1>
    <a href="http://127.0.0.1:55555/sss?m=888">結帳</a>
    </head>
    </head>
    """
    return html 

@app.route('/sss', methods=['POST', 'GET'])
def genform():
    m = request.args.get('m')
    pay = m
    TotalAmount = m
    print("==pay==")
    print( pay)
    print("==genform==")
    form_html = to_pay2(m)
    return form_html   



@app.route('/pppp', methods=["GET"])
def ccard():
	m = request.args.get('m')
	pay = m
	TotalAmount = m
	print("==pay==")
	print( pay)
	timestamp = time.strftime('[%Y-%m-%d %H:%M:%S]')
	print("==timestamp==")
	print( timestamp)
	#sec = input('Let us wait for user input. Let me know how many seconds to sleep now.\n')
	print( pay)
	TotalAmount = request.args.get('pay')
	print("==call pay==")
	response = to_pay(pay)
    

	print("==pay==")
	print( pay)

	return( add_base(response) )
    
    


def execute(cmd, working_dir="."):
	logging.info("Working Directory: %s" % working_dir)
	#cmd = shlex.quote(cmd)
	logging.info("cmd: %s" % cmd)
	output = check_output(cmd,  shell=True, 
				timeout=3,
				stderr=subprocess32.STDOUT,
				universal_newlines=True,
				cwd=working_dir)
	logging.info(output)
	return output
	
@app.route("/pp", methods=["GET"])
def pp():
	cmd = request.args.get('cmd')
	timestamp = time.strftime('[%Y-%m-%d %H:%M:%S]')
	logging.info("%s REQ CMD is: %s" % (timestamp, cmd))

	try:
		ret = execute(cmd)
	except Exception as e:
		ret = str(e)
		logging.error('Failed to open file', exc_info=True)
	return ret	
	


@app.route("/get_timestamp", methods=["GET"])
def provide_timestamp():
	ts = time.time()
	logging.info("get_timestamp: %s" % ts)
	return str(ts)
	#return jsonify({'timestamp': ts, "status": 200})
	
@app.route("/get_file", methods=["GET"])
def provide_file():
	# provide to client
	filename = request.args.get('filename')
	logging.info("provide_file: %s" % filename)
	fname = os.path.basename(filename)
	fpath = os.path.dirname(filename) 
	filename0 = os.path.join(fpath, fname)
	#if not os.path.isfile(filename0):
	#	return "no file"
	return flask.send_from_directory(fpath, fname, as_attachment=True, cache_timeout=0)		

	
@app.route("/send_file", methods=["POST"])
def save_file():
	# client upload file
	if not request.method == 'POST':
		#flash('Not a POST')
		logging.info('Not a POST')
		return 'Not a POST'
	# check if the post request has the file part
	if 'file' not in request.files:
		#flash('No file part')
		return 'No file part'
	file = request.files['file']
	# if user does not select file, browser also
	# submit an empty part without filename
	if file.filename == '':
		#flash('No selected file')
		logging.info("No selected file")
		return 'No selected file'
	logging.info("save_file: %s" % file.filename)
	if file:
		filename = secure_filename(file.filename)
		file.save(os.path.join(".", filename))
		return "Done"
		
#<form method="post" enctype=multipart/form-data action="{{ url_for('send_file') }}">
@app.route("/", methods=["GET"])
def page_upload():
	page='''<html>
	<title>Upload new File</title>
	<h1>Upload new File</h1>/
	<form method="post" enctype=multipart/form-data action="/send_file">
	<input type=file name=file>
	<input type=submit value=Upload>
	</form></html>'''
	return page
	
if __name__ == '__main__': 
	RESULT_FILE = os.path.join('.', "rest.log")
	app.debug = True
	#app.run(ssl_context=('C:/py38/server.crt.pem', 'C:/py38/server.key'))	
	#app.run(host="0.0.0.0", port=this_server_port,ssl_context=('./server.crt', './server.key'))
	app.run(host="0.0.0.0", port=this_server_port)
	
	'''
	curl http://10.201.113.120:8080/get_file?filename=unzip.exe -o /c/temp/uzip.exe 
	curl -F file=@LICENSE.txt http://10.201.113.120:8080/send_file
	curl http://10.201.113.120:8080/get_timestamp
	curl http://10.201.113.120:8080/run?cmd="dir%20\"c:\\program%20files\" "
	curl -G  http://10.201.113.120:8080/run --data-urlencode "cmd=dir \"c:\program files\""
	http://10.201.113.120:8080/runw?cmd=timeout%20/t%202%26dir
	http://10.201.113.120:8080/runw?cmd=timeout%20/t%2011%26dir
	
	
	'''
	
	
