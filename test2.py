import pytesseract
import argparse
import sys
import re
import os
import requests
import cv2
import json 
import numpy as np
from time import sleep
try:
    import Image
except ImportError:
    from PIL import Image, ImageEnhance
from bs4 import BeautifulSoup, SoupStrainer
from urllib.request import urlretrieve
from io import BytesIO

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
home_url = 'https://parivahan.gov.in/rcdlstatus/'
post_url = 'https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml'
# Everything before the last four digits: MH02CL
first = sys.argv[1]
# The last four digits: 0555
second = sys.argv[2]

r = requests.get(url=home_url)
cookies = r.cookies
soup = BeautifulSoup(r.text, 'html.parser')
viewstate = soup.select('input[name="javax.faces.ViewState"]')[0]['value']
# MARK: Identifying Submit Button which will be responsible to make POST Request
button = soup.find("button",{"type": "submit"})	
img_test=soup.find("img",{"id": "form_rcdl:j_idt34:j_idt41"})
#MARK: Get Request to get Captcha Image from URL
## Captcha Image Changes each time the URL is fired
iresponse = requests.get("https://parivahan.gov.in"+img_test['src'])
img = Image.open(BytesIO(iresponse.content))
img.save("downloadedpng.png")

print('Resolving Captcha')
captcha_text = pytesseract.image_to_string(Image.open('downloadedpng.png'))
extracted_text = captcha_text.replace(" ", "").replace("\n", "")
print("OCR Result => ", extracted_text)
print(extracted_text)
extracted_text=input("Enter Captcha: ")

data = {
    'javax.faces.partial.ajax':'true',
    'javax.faces.source': button['id'],
    'javax.faces.partial.execute':'@all',
    'javax.faces.partial.render': 'form_rcdl:pnl_show form_rcdl:pg_show form_rcdl:rcdl_pnl',
    button['id']:button['id'],
    'form_rcdl':'form_rcdl',
    'form_rcdl:tf_reg_no1': first,
    'form_rcdl:tf_reg_no2': second,
	'form_rcdl:j_idt34:CaptchaID':extracted_text,
    'javax.faces.ViewState': viewstate
}



# MARK: Request Headers which may or may not needed to be passed in POST Request
# Verify in debugger
headers = {
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'Accept': 'application/xml, text/xml, */*; q=0.01',
	'Accept-Language': 'en-us',
	'Accept-Encoding': 'gzip, deflate, br',
	'Host': 'parivahan.gov.in',
	'DNT': '1',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15',
	'Cookie': 'JSESSIONID=%s; has_js=1' % cookies['JSESSIONID'],
	'X-Requested-With':'XMLHttpRequest',
	'Faces-Request':'partial/ajax',
	'Origin':'https://parivahan.gov.in',
	'Referer':'https://parivahan.gov.in/rcdlstatus/',
    'Connection':'keep-alive'
    # 'User-Agent': 'python-requests/0.8.0',
    # 'Access-Control-Allow-Origin':'*',
}

# MARK: Added delay
sleep(2.0)

r = requests.post(url=post_url, data=data, headers=headers, cookies=cookies)
soup = BeautifulSoup(r.text, 'html.parser')
table = SoupStrainer('tr')
soup = BeautifulSoup(soup.get_text(), 'html.parser', parse_only=table)
print(soup.get_text())