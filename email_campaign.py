#  Alternative script to send random/campaign emails such as a Email-Marketing

import psycopg2
import math
import smtplib
import random
import string
from email.mime.text import MIMEText
from email.header import Header

SMTP_EMAIL_SENDER = 'admin@domain.com'
SMTP_SERVER_LOGIN = 'postmaster@mailgun.com'
SMTP_SERVER_PASSWORD = 'YOUR_PASSWORD'
SMTP_HOST = 'smtp.mailgun.org'
SMTP_HOST_PORT = 587

def send_email(to_address, msg):
	msg = MIMEText(msg)
	msg['Subject'] = "EasyDjango!"
	msg['From']    = SMTP_EMAIL_SENDER
	msg['To']      = to_address

  	s = smtplib.SMTP(SMTP_HOST, SMTP_HOST_PORT)

	s.login(SMTP_SERVER_LOGIN, SMTP_SERVER_PASSWORD)
  	s.sendmail(msg['From'], msg['To'], msg.as_string())
  	s.quit()

conn_string = "host='localhost' dbname='learn_django' user='postgres' password='postgres'"
cnx = psycopg2.connect(conn_string)
cursor = cnx.cursor()
cursor2 = cnx.cursor()

cursor.execute("select au.id, au.email from auth_user au")
records = cursor.fetchall()

for (id, email, value) in records:
	print("{0} - {1} - {2}").format(id, email, value)
	msg = """O EasyDjango acabou de lançar um novo post:

			"Construção de templates HTML dinâmicos (tags): Como utilizar template tags (ou TagLibs) no Django"

			Confira o conteúdo completo em:
                """.encode('utf-8')
	link = "{0}/posts/template_tags".format('http://www.easydjango.com').encode('utf-8')
	try:
		send_email(email, msg+link)	
	except Exception as e:
		print("Error to send email: {0} {1}".format(email, e))

	#cursor2.execute("UPDATE blog_tokenusersignin set is_used = true where user_id = {0}".format(id))
	

cnx.commit()
cursor.close()
cursor2.close()
cnx.close()
