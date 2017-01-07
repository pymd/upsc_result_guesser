import requests
import shutil
import sys

irctc_login_page_captcha = 'https://www.irctc.co.in/eticketing/captchaImage?0.5059193031336786'
catpcha_url_prefix = 'http://upsconline.nic.in/eadmitcard/upsc_ac2/csp_premark_2015/include/captcha_code_file.php?rand='

CAPTCHA_FILENAME = 'training_data/captcha'
CLEANED_CAPTCHA_FILENAME = 'clean_captcha.jpg'

def get_page(url, request_type = 'GET', data = dict(), headers = dict(), stream=False):
	try:
		if stream == True and headers == dict():
			# For captcha image
			response = requests.get(url, stream = True)
		elif request_type == 'POST':
			# For submitting login form
			response = requests.post(url, data=data, headers=headers)
		else:
			# For fetching html pages
			response = requests.get(url)
		return response
	except Exception as e:
		print "Error during fetching page: ",url,"Error:",e
		return None

def fetch_and_save_captcha_image(url_prefix, captcha_random_number,index):
	response = get_page(url_prefix+str(captcha_random_number), stream=True)
	try:
		with open(CAPTCHA_FILENAME+str(index)+".jpg", 'wb') as out_file:
			shutil.copyfileobj(response.raw, out_file)
		del response
	except Exception as e:
		print "Error during saving captcha image: ", e

captcha_random_number = 909599504

for i in range(100):
    print 'fetching captcha image:',i
    fetch_and_save_captcha_image(catpcha_url_prefix, captcha_random_number,i)
