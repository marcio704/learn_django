import math
import smtplib

#Utililty/ reusable functions:

def divide_list_by_two (whole_list):
    half_size_ceil = int(math.ceil(len(whole_list)/2))  
    half_size_floor = int(math.floor(len(whole_list)/2))
    list_1 = whole_list [:half_size_ceil]
    list_2 = whole_list [len(whole_list) - half_size_floor:]

    return {"list_1": list_1, "list_2": list_2}


def send_email(to_address, msg):

	from_address = 'marcioacsantiago@gmail.com'
	# Credentials (if needed)
	username = 'marcioacsantiago@gmail.com'
	password = 'mgderune2k'

	# The actual mail send
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username,password)
	server.sendmail(from_address, to_address, msg)
	server.quit()