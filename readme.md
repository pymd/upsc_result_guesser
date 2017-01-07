## Scripts to guess my friends UPSC roll no

My friend needed to know his UPSC prelims marks but forgot his roll no.
Made these scripts to guess his roll no using his DOB. In the process, the script also segregates the valid UPSC roll nos from the invalid ones.   
It fetches captcha images, extract the text out of the captcha using _tesseract_ and calls the login API.

#### Update:

UPSC have updated the login URL to use SSL. The script isn't updated for HTTPs.
