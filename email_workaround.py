#  pip install --allow-external mysql-connector-python mysql-connector-python

import psycopg2
import math
import smtplib
import random
import string
from email.mime.text import MIMEText
from email.header import Header

def send_email(to_address, msg):
	msg = MIMEText(msg)
	msg['Subject'] = "EasyDjango!"
	msg['From']    = 'admin@easydjango.com'
	msg['To']      = to_address

  	s = smtplib.SMTP('smtp.mailgun.org', 587)

	s.login('postmaster@easydjango.com', 'b1fab8d9b2706d58fd23e547a6135cc7')
  	s.sendmail(msg['From'], msg['To'], msg.as_string())
  	s.quit()

records = []
try:
	conn_string = "host='localhost' dbname='learn_django' user='postgres' password='postgres'"
	cnx = psycopg2.connect(conn_string)
	cursor = cnx.cursor()
	cursor2 = cnx.cursor()


	cursor.execute("select au.id, au.email, tk.value from  auth_user au inner join blog_tokenusersignin tk on au.id = tk.user_id where tk.is_used = true")
	records = cursor.fetchall()
except Exception as e:
	print("Ocorreu um ERRO: {0}".format(e))

for (id, email, value) in records:
	print("{0} - {1} - {2}").format(id, email, value)
	msg = """Ola, clique no link abaixo para confirmar sua conta no EasyDjago:

                """
	link = "{0}/account_confirmation?token={1}".format('http://www.easydjango.com', value)
	try:
		send_email(email, msg+link)	
	except:
		print("Error to send email: {0}".format(email))

	cursor2.execute("UPDATE blog_tokenusersignin set is_used = true where user_id = {0}".format(id))
	

cnx.commit()
cursor.close()
cursor2.close()
cnx.close()
